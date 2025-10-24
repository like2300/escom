from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from database.models import *
from transactions.models import *
from django.http import HttpResponse,HttpResponseRedirect
# from datetime import datetime,date,time
# from emploieDutemps.models import EmploieDuTemps,Jour
# from django.db.models import Q
# from heures_cours.models import PresenceCours
# from django.db.models import Count, Sum, Avg,F, FloatField, ExpressionWrapper
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
# from database.models import Transaction,Classe,AnneeAcademique,Enseignant,Etudiant,Utilisateur,EnseignantProfile,Recu,EtudiantProfile
# from .models import *
from django.http import HttpResponse,HttpResponseRedirect
# from datetime import datetime,date,time
# from emploieDutemps.models import EmploieDuTemps,Jour
# from django.db.models import Q
# from heures_cours.models import PresenceCours
from django.db.models import Count, Sum, Avg,F, FloatField, ExpressionWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login,logout
from django.http import HttpResponseForbidden
from database.models import Utilisateur
from transactions.models import *
from django.contrib import messages
from django.db import IntegrityError
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
# from datetime import datetime,date,time
from transactions.utils import *
from notes.models import *
from datetime import datetime, timedelta,date
from notes.views import calcul_moyenne_simple

from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from .models import EtudiantProfile, Classe, Transaction, AnneeAcademique

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
# Statisque des payers et des impayers

from django.shortcuts import render
from django.db.models import Q




from xhtml2pdf import pisa
from io import BytesIO

@admin_decorators
def impression_emploie(request,clas_id,semestre):

    classe_id = get_object_or_404(Classe, id=clas_id)
    semestres=Semestre.objects.get(id=semestre)
    jours_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
    emploi_global = {}

    for jour_nom in jours_semaine:
        emploi_global[jour_nom] = {
            'premier': {'horaire': '', 'details': ['Aucun', 'Aucun', 'Aucun'], 'existe': False},
            'deuxieme': {'horaire': '', 'details': ['Aucun', 'Aucun', 'Aucun'], 'existe': False}
        }
        
        creneaux = EmploieDuTemps.objects.filter(
            classe=classe_id,
            semestre=semestres,
            jour__nom=jour_nom
        ).select_related('matiere', 'enseignant', 'salle')
        
        premier = creneaux.filter(nature='1er').first()
        if premier:
            horaire = f"{premier.heure_debut.strftime('%H:%M')} - {premier.heure_fin.strftime('%H:%M')}"
            emploi_global[jour_nom]['premier'] = {
                'horaire': horaire,
                'details': [
                    premier.matiere.nom if premier.matiere else 'Aucun',
                    f"{premier.enseignant.enseignant_utilisateur.nom} {premier.enseignant.enseignant_utilisateur.prenom}" if premier.enseignant else 'Aucun',
                    premier.salle.nom if premier.salle else 'Aucun'
                ],
                'existe': True
            }
        
        deuxieme = creneaux.filter(nature='2eme').first()
        if deuxieme:
            horaire = f"{deuxieme.heure_debut.strftime('%H:%M')} - {deuxieme.heure_fin.strftime('%H:%M')}"
            emploi_global[jour_nom]['deuxieme'] = {
                'horaire': horaire,
                'details': [
                    deuxieme.matiere.nom if deuxieme.matiere else 'Aucun',
                    f"{deuxieme.enseignant.enseignant_utilisateur.nom} {deuxieme.enseignant.enseignant_utilisateur.prenom}" if deuxieme.enseignant else 'Aucun',
                    deuxieme.salle.nom if deuxieme.salle else 'Aucun'
                ],
                'existe': True
            }

    context = {
        'semestre':semestres,
        'E1': emploi_global,
        'classe':classe_id,
        'jours_semaine': jours_semaine
    }
    
    try:
        html_string = render_to_string('pages/pdf/emploie.html', context)
        
        # Create a PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="emploie_du_temps_{classe_id.nom}.pdf"'
            return response
        else:
            return HttpResponse(f"Erreur lors de la génération du PDF: {pdf.err}")
            
    except Exception as e:
        return HttpResponse(f"Erreur inattendue: {str(e)}")

