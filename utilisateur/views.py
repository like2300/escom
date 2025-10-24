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
from django.contrib.auth import authenticate, login as auth_login,logout
from django.http import HttpResponseForbidden

from transactions.utils import *

# from django.shortcuts import render,redirect,get_object_or_404
# # # from dataBase.models import *
from django.contrib import messages
# from django.http import HttpResponse
# from datetime import date,time,datetime
# # from django.utils import timezone
# # # from django.contrib.auth import authenticate,login,logout
# # from .utils import generate_pdf
# # from django.conf import settings
@admin_decorators
def menu_prof(request):
    enseignants = Contrat.objects.all
    print(enseignants)
    context={
        'enseignants':enseignants
    }
    return render(request,"pages/dashboard/admin/prof_liste.html",context)
@admin_decorators
def menu_details_prof(request,id):
    prof=Enseignant.objects.get(id=id)
    info=Contrat.objects.get(enseignant=prof)
    print(info)
    emploie=EmploieDuTemps.objects.filter(enseignant=prof).order_by('jour__numero','heure_debut')
    classe_ids = EmploieDuTemps.objects.filter(
    enseignant=prof
    ).values_list('classe__nom', flat=True).distinct()
    matiere_ids = EmploieDuTemps.objects.filter(
    enseignant=prof
    ).values_list('matiere__nom', flat=True).distinct()
    print(f'{classe_ids}- {matiere_ids}')
    presence=PresenceCours.objects.filter(enseignant=prof).order_by('date_cours')
    print(presence)
    context={
        'presence':presence,
        'teacher':info,
        'matiere':matiere_ids,
        'classe':classe_ids,
        'emploie':emploie
    }
    return render(request,"pages/dashboard/admin/prof_details.html",context)
