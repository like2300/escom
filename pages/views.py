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
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
# from datetime import datetime,date,time
from transactions.utils import *
from notes.models import *
from datetime import datetime, timedelta,date
from .forms import *
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
from io import BytesIO
from xhtml2pdf import pisa
# from .models import PaiementEcolage, Etudiant, Classe, AnneeAcademique, Mois

# def get_impayes(classe_id=None, annee_id=None, mois_id=None):
#     # Récupérer tous les étudiants
#     etudiants = Transaction.objects.all()
    
#     # Appliquer les filtres
#     if classe_id:
#         etudiants = etudiants.filter(classe_id=classe_id)
    
#     impayes = []
    
#     for etudiant in etudiants:
#         # Vérifier si l'étudiant a payé pour les critères donnés
#         paiements_query = PaiementEcolage.objects.filter(etudiant=etudiant.etudiant)
        
#         if annee_id:
#             paiements_query = paiements_query.filter(annee_academique_id=annee_id)
#         if mois_id:
#             paiements_query = paiements_query.filter(mois_id=mois_id)
        
#         if not paiements_query.exists():
#             impayes.append({
#                 'etudiant': etudiant,
#                 'classe': etudiant.classe,
#                 'annee_academique': AnneeAcademique.objects.get(id=annee_id) if annee_id else None,
#                 'mois': Mois.objects.get(id=mois_id) if mois_id else None,
#             })
    
#     return impayes

# def stats(request):
#     classe_id = request.GET.get('classe')
#     annee_id = request.GET.get('annee_academique')
#     mois_id = request.GET.get('mois')
    
#     # Récupérer toutes les options pour les filtres
#     classes = Classe.objects.all()
#     annees_academiques = AnneeAcademique.objects.all()
#     mois = Mois.objects.all()
    
#     # Filtrer les paiements
#     paiements = PaiementEcolage.objects.all().order_by('etudiant__utilisateur__nom','etudiant__utilisateur__prenom')
    
#     if classe_id:
#         paiements = paiements.filter(classe_id=classe_id)
#     if annee_id:
#         paiements = paiements.filter(annee_academique_id=annee_id)
#     if mois_id:
#         paiements = paiements.filter(mois_id=mois_id)
    
#     # Séparer les payés et impayés
#     payes = paiements
#     impayes = get_impayes(classe_id, annee_id, mois_id)
    
#     context = {
#         'payes': payes,
#         'impayes': impayes,
#         'classes': classes,
#         'annees_academiques': annees_academiques,
#         'mois': mois,
#         'classe_selected': classe_id,
#         'annee_selected': annee_id,
#         'mois_selected': mois_id,
#     }
#     return render(request,'pages/transaction/statistique.html',context)





@admin_decorators
def honoraire(request):
    # Récupérer le mois actuel
    mois_actuel = datetime.now().date().month
    print(mois_actuel)
    # Agrégation des honoraires par enseignant pour le mois en cours
    # Utilisation de la somme des durées au lieu du compte des IDs
    presence = PresenceCours.objects.filter(
        date_cours__month=mois_actuel
    ).values(
        'enseignant',
        'enseignant__enseignant_utilisateur__nom',
        'enseignant__enseignant_utilisateur__prenom'
    ).annotate(
        total_duree=Sum('nombre_heure'),  # Somme de toutes les durées
        count=Count('id'),  # Garder le compte pour information
        price=Sum('nombre_heure') * 1500  # 500 FCFA par heure (si duree est en heures)
    )
    
    # Alternative si la durée est stockée en minutes :
    # presence = PresenceCours.objects.filter(
    #     date_cours__month=mois_actuel
    # ).values(
    #     'enseignant'
    # ).annotate(
    #     total_duree_minutes=Sum('duree'),
    #     total_duree_heures=Sum('duree') / 60.0,
    #     count=Count('id'),
    #     price=(Sum('duree') / 60.0) * 500  # Conversion minutes -> heures
    # )
    
    # Détails des cours pour l'affichage
    presence1 = PresenceCours.objects.filter(
        date_cours__month=mois_actuel
    ).values(
        'enseignant',
        'matiere__nom',
        'classe__nom', 
        'salle__nom',
        'date_cours',
        'nombre_heure'  # Ajouter la durée pour l'affichage
    ).order_by('date_cours')

    total=0

    print(f"Honoraires trouvés: {presence.count()}")
    for honoraire in presence:
        print(f"Enseignant: {honoraire['enseignant']}, Durée totale: {honoraire['total_duree']}, Prix: {honoraire['price']}")
        total+=honoraire['price']

    print(total)
    context = {
        'total':total,
        'details': presence1,
        'honoraire': presence,
        'datetime': datetime.now()
    }

    return render(request, 'pages/transaction/honoraire.html', context)


@admin_decorators
def regler(request, enseignant_id, price):
    # Vue pour régler les honoraires d'un enseignant
    enseignant = get_object_or_404(Enseignant, id=enseignant_id)
    
    # Ici vous pouvez implémenter la logique de paiement
    # Par exemple, marquer les honoraires comme payés
    # ou enregistrer une transaction de paiement
    
    print(f"Règlement des honoraires pour {enseignant} - Montant: {price} FCFA")
    
    # Rediriger vers la page des honoraires après paiement
    return redirect('prof')









































def get_impayes(classe_id=None, annee_id=None, mois_id=None):
    # Récupérer tous les étudiants
    etudiants = Transaction.objects.all().order_by('etudiant__utilisateur__nom','etudiant__utilisateur__prenom')
    
    # Appliquer les filtres
    if classe_id:
        etudiants = etudiants.filter(classe_id=classe_id)
    
    impayes = []
    
    for etudiant in etudiants:
        # Vérifier si l'étudiant a payé pour les critères donnés
        paiements_query = PaiementEcolage.objects.filter(etudiant=etudiant.etudiant).order_by('etudiant__utilisateur__nom','etudiant__utilisateur__prenom')
        
        if annee_id:
            paiements_query = paiements_query.filter(annee_academique_id=annee_id)
        if mois_id:
            paiements_query = paiements_query.filter(mois_id=mois_id)
        
        if not paiements_query.exists():
            impayes.append({
                'etudiant': etudiant,
                'classe': etudiant.classe,
                'annee_academique': AnneeAcademique.objects.get(id=annee_id) if annee_id else None,
                'mois': Mois.objects.get(id=mois_id) if mois_id else None,
            })
    
    return impayes

def stats(request):
    classe_id = request.GET.get('classe')
    annee_id = request.GET.get('annee_academique')
    mois_id = request.GET.get('mois')
    
    # Récupérer toutes les options pour les filtres
    classes = Classe.objects.all()
    annees_academiques = AnneeAcademique.objects.all()
    mois = Mois.objects.all()
    
    # Filtrer les paiements
    paiements = PaiementEcolage.objects.all().order_by('etudiant__utilisateur__nom','etudiant__utilisateur__prenom')
    
    if classe_id:
        paiements = paiements.filter(classe_id=classe_id)
    if annee_id:
        paiements = paiements.filter(annee_academique_id=annee_id)
    if mois_id:
        paiements = paiements.filter(mois_id=mois_id)
    
    # Séparer les payés et impayés
    payes = paiements
    impayes = get_impayes(classe_id, annee_id, mois_id)
    
    context = {
        'payes': payes,
        'impayes': impayes,
        'classes': classes,
        'annees_academiques': annees_academiques,
        'mois': mois,
        'classe_selected': classe_id,
        'annee_selected': annee_id,
        'mois_selected': mois_id,
    }
    return render(request,'pages/transaction/statistique.html',context)
































@admin_decorators
def generer_matricules_classe(request, classe_id):
    """
    Réinitialise et génère les matricules avec update individuel
    """
    try:
        # Récupérer la classe
        classe = get_object_or_404(Classe, id=classe_id)
        
        # Récupérer l'année académique (courante ou spécifiée)
        if True:
            annee_academique = get_object_or_404(AnneeAcademique, id=1)
        else:
            annee_academique = AnneeAcademique.objects.filter(courante=True).first()
            if not annee_academique:
                messages.error(request, "Aucune année académique courante trouvée")
                return redirect('etudiant_by_classe', classe=classe.id)
        
        # Récupérer tous les étudiants de la classe pour l'année académique donnée
        transactions = Transaction.objects.filter(
            classe=classe,
            annee_academique=annee_academique
        ).select_related('etudiant__utilisateur').order_by('etudiant__utilisateur__nom', 'etudiant__utilisateur__prenom')
        
        nombre_etudiants = transactions.count()
        
        if nombre_etudiants == 0:
            messages.warning(request, f"Aucun étudiant trouvé pour la classe {classe.code}")
            return redirect('etudiant_by_classe', classe=classe.id)
        
        code_classe = classe.nom.upper()
        compteur_mis_a_jour = 0
        
        with transaction.atomic():
            for index, trans in enumerate(transactions, 1):
                try:
                    profile = trans.etudiant.utilisateur
                    
                    # Générer le nouveau matricule
                    numero_etudiant = str(index).zfill(4)
                    nouveau_matricule = f"{code_classe}-{numero_etudiant}"
                    
                    # Mettre à jour directement
                    EtudiantProfile.objects.filter(id=profile.id).update(matricule=nouveau_matricule)
                    compteur_mis_a_jour += 1
                    
                except EtudiantProfile.DoesNotExist:
                    continue
        
        messages.success(
            request, 
            f"Matricules générés pour {classe.nom} : {compteur_mis_a_jour} étudiants mis à jour"
        )
        return redirect('etudiant_by_classe', classe=classe.id)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la génération des matricules: {str(e)}")
        return redirect('etudiant_by_classe', classe=classe.id)



@admin_decorators
def presence(request):
    jour=datetime.now().date().isoweekday()
    print(jour)
    
    # emploie=EmploieDuTemps.objects.filter(Q(jour=datetime.now().date().isoweekday())|Q(annee_academique=annee))
    # emploie=EmploieDuTemps.objects.filter(jour=jour)
    emploie=EmploieDuTemps.objects.filter(jour=jour).order_by('heure_debut')
    print(emploie)
    #Notification pour voir si le cours a ette deja va
    print(len(PresenceCours.objects.all()))
    
    annee = get_object_or_404(AnneeAcademique, id=1)

    # COMPTAGE DES INTERVENANTS DU JOUR
    total_count = emploie.count()
    
    # DATE D'AUJOURD'HUI POUR FILTRER LES PRÉSENCES
    aujourdhui = date.today()
    
    # COMPTAGE DES PRÉSENCES ENREGISTRÉES AUJOURD'HUI
    presence_count = PresenceCours.objects.filter(
        date_cours=aujourdhui,
        # emploie__jour=jour
    ).count()
    
    # CALCUL DU POURCENTAGE
    presence_percentage = 0
    if total_count > 0:
        presence_percentage = round((presence_count / total_count) * 100)
    
    print(f"Total intervenants: {total_count}")
    print(f"Présences enregistrées: {presence_count}")
    print(f"Pourcentage: {presence_percentage}%")
    
    emploie1 = {}
    for i in emploie:
        # VÉRIFIER SI LA PRÉSENCE A ÉTÉ ENREGISTRÉE AUJOURD'HUI
        presence_aujourdhui = PresenceCours.objects.filter(
            emploie_id=i.id,
            date_cours=aujourdhui
        ).first()
        
        present = presence_aujourdhui is not None
        Id = presence_aujourdhui if present else None

        emploie1[i.id] = {
            'Xid': i.id,
            'nom': i.enseignant.enseignant_utilisateur.nom,
            'prenom': i.enseignant.enseignant_utilisateur.prenom,
            'matiere': i.matiere,
            'salle': i.salle,
            'heure_debut': i.heure_debut.strftime('%H:%M'),
            'heure_fin': i.heure_fin.strftime('%H:%M'),
            'present': present,
            'Id': Id
        }


    # presence=PresenceCours.objects.filter(jour=jour,traitement=False)
    emploie1={}
    for i in emploie :
        j=0,
        if len(PresenceCours.objects.all())!=0 and PresenceCours.objects.filter(emploie_id=i.id).exists() :
            Id=PresenceCours.objects.get(emploie_id=int(i.id))
            present=True
        else :
            present=False
            Id=None

        emploie1[i.id]={
            'Xid':i.id,
            'id':len(emploie),
            'nom':i.enseignant.enseignant_utilisateur.nom ,
            'prenom':i.enseignant.enseignant_utilisateur.prenom,
            'matiere': i.matiere,
            'salle':i.salle,
            'heure_debut':i.heure_debut.strftime('%H:%M'),
            'heure_fin':i.heure_fin.strftime('%H:%M'),
            'present':present,
            'Id':Id
        }
    print(emploie1)
    


    context={
        'emploie':emploie1,
        'jour': get_object_or_404(Jour,numero=jour).nom,
        'time':datetime.now().time(),
        'total_count': total_count,
        'presence_count': presence_count,
        'presence_percentage': presence_percentage,
        'time': datetime.now().time()
    }
    return render(request,'pages/dashboard/prof/pres.html',context)

 
##################


@admin_decorators
def enregistrement_presence(request, id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        intervenant_id = request.POST.get('intervenant_id')
        heure_debut1 = request.POST.get('heure_debut')
        heure_fin1 = request.POST.get('heure_fin')
        remarques = request.POST.get('remarques', '')
        print(remarques)
        
        # Récupérer l'emploi du temps
        emploie = get_object_or_404(EmploieDuTemps, id=intervenant_id)
        
        # Convertir les heures de string en time objects
        heure_debut = datetime.strptime(heure_debut1, '%H:%M').time()
        heure_fin = datetime.strptime(heure_fin1, '%H:%M').time()
        
        # Calculer le nombre d'heures
        # Créer l'enregistrement de présence
        enregistrement = PresenceCours.objects.create(
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            enseignant=emploie.enseignant,
            annee_academique=get_object_or_404(AnneeAcademique, id=1),
            classe=emploie.classe,
            jour=emploie.jour,
            matiere=emploie.matiere,
            salle=emploie.salle,
            emploie_id=emploie.id,
            nombre_heure=(datetime.combine(datetime.today(), emploie.heure_fin) - datetime.combine(datetime.today(), emploie.heure_debut)).total_seconds() / 3600,
            date_cours=timezone.now().date()
        )
        
        return redirect('presence')
    
    # Si méthode GET, rediriger vers la page principale
    return redirect('presence')

 ############


def handler404(request, exception):
    return render(request, 'pages/message/404.html', status=404)


@admin_decorators
def transactions(request):
    transactions=Transaction.objects.all().order_by('date')
    ecolage=PaiementEcolage.objects.all().order_by('mois')
    soutenance=Paiement_soutenance.objects.all().order_by('etudiant')
    total=0
    total2=0
    #Entree d'argent:
    if ecolage:
        for i in ecolage:
            total+=int(i.montant)
    if transactions:
        for j in transactions:
            total+=int(j.montant)
    if soutenance:
        for k in soutenance:
            total+=int(k.montant)
    #Sortie d'argent:
    # if honoraire:
    #     for n in honoraire:
    #         total2 += int(n.montant)


    final=total-total2
    # totat_entree=
    # print(totat_entree)
    print(total)
    l1=Niveau.objects.get(libelle='L1')
    l2=Niveau.objects.get(libelle='L2')
    l3=Niveau.objects.get(libelle='L3')
    annee=AnneeAcademique.objects.get(id=1)
    tarif=Tarif.objects.get(annee_academique=annee)
    print(tarif)
    print(annee)
    context={
        'total':final,
        'total_sortie':total2,
        'total_entree':total,
        'paiement':ecolage,
        'transaction':transactions,
        # 'tarif':Tarif.objects.get(annee_academique=annee)
        'l1':Tarif.objects.get(annee_academique=annee,niveau=l1),
        # 'l2':Tarif.objects.get(annee_academique=annee,niveau=l2),
        # 'l3':Tarif.objects.get(annee_academique=annee,niveau=l3),
        'tarif':tarif,
        'soutenance':soutenance

    }
    return render(request,"pages/transaction/transactions.html",context)


@admin_decorators
def etudiant_by_classe(request, classe):


        # Récupérer les matières programmées pour cette année et classe
    # matieres_s1 = Matiere_Programmer.objects.filter(
    #     annee_academique=annee_courante,
    #     classe=etudiant.classe_actuelle, 
    #     semestre__libelle="S1"
    # ).select_related('matiere', 'enseignant')
    
    # matieres_s2 = Matiere_Programmer.objects.filter(
    #     annee_academique=annee_courante,
    #     classe=etudiant.classe_actuelle, 
    #     semestre__libelle="S2"
    # ).select_related('matiere', 'enseignant')
    
    # # Récupérer les notes existantes
    # notes_s1 = Notes.objects.filter(
    #     etudiant=etudiant,
    #     annee_academique=annee_courante,
    #     semestre__libelle="S1"
    # ).select_related('matiere__matiere')
    
    # notes_s2 = Notes.objects.filter(
    #     etudiant=etudiant,
    #     annee_academique=annee_courante,
    #     semestre__libelle="S2"
    # ).select_related('matiere__matiere')
    
    # # Calcul des statistiques
    # total_matieres = matieres_s1.count() + matieres_s2.count()
    # matieres_avec_notes = notes_s1.count() + notes_s2.count()
    # matieres_sans_notes = total_matieres - matieres_avec_notes
    
    # context = {
    #     'etudiant': etudiant,
    #     'matieres_s1': matieres_s1,
    #     'matieres_s2': matieres_s2,
    #     'notes_s1': notes_s1,
    #     'notes_s2': notes_s2,
    #     'total_matieres': total_matieres,
    #     'matieres_avec_notes': matieres_avec_notes,
    #     'matieres_sans_notes': matieres_sans_notes,
    #     # ... autres contextes existants
    # }
    print(classe)
    classe_id = get_object_or_404(Classe, id=classe)
    print(classe_id)
    liste = Transaction.objects.filter(classe=classe_id).order_by('etudiant__utilisateur__nom')
    
    # Définir les semestres selon le niveau
    if classe_id.niveau.libelle == "L1":
        premier_semestre = Semestre.objects.get(nom_semestre='S1')
        second_semestre = Semestre.objects.get(nom_semestre='S2')
    elif classe_id.niveau.libelle == "L2":
        premier_semestre = Semestre.objects.get(nom_semestre='S3')
        second_semestre = Semestre.objects.get(nom_semestre='S4')
    elif classe_id.niveau.libelle == "L3":
        premier_semestre = Semestre.objects.get(nom_semestre='S5')
        second_semestre = Semestre.objects.get(nom_semestre='S6')


    ense = Enseignant.objects.filter(
    emploiedutemps__semestre_id=premier_semestre,
    emploiedutemps__classe_id=classe_id
    ).distinct()
    ense1 = Enseignant.objects.filter(
    emploiedutemps__semestre_id=second_semestre,
    emploiedutemps__classe_id=classe_id
    ).distinct()
    m1 =matieres = Matiere_Programmer.objects.filter(
    emploiedutemps__semestre_id=premier_semestre,
    emploiedutemps__classe_id=classe_id
    ).distinct()
    m2 =matieres = Matiere_Programmer.objects.filter(
    emploiedutemps__semestre_id=second_semestre,
    emploiedutemps__classe_id=classe_id
    ).distinct()
    # Récupérer toutes les matières, enseignants et salles pour les formulaires  # Importez vos modèles
    matieresS1 = Matiere_Programmer.objects.filter(semestre=premier_semestre,classe=classe)
    matieresS2 = Matiere_Programmer.objects.filter(semestre=second_semestre,classe=classe)

    
    salles = Salle.objects.all()
    # print(f'{enseignants} {matieres}')
    # Récupérer l'emploi du temps complet pour le premier semestre
    jours_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']

    #Semestre 1
    emploi_global = {}
    em=EmploieDuTemps.objects.filter(
            classe=classe_id,
            semestre=premier_semestre,
        ).select_related('matiere', 'enseignant', 'salle')
    
    
    for jour_nom in jours_semaine:
        emploi_global[jour_nom] = {
            'premier': {'horaire': '', 'details': ['Aucun', 'Aucun', 'Aucun'], 'existe': False},
            'deuxieme': {'horaire': '', 'details': ['Aucun', 'Aucun', 'Aucun'], 'existe': False}
        }
        
        # Requête pour le jour
        creneaux = EmploieDuTemps.objects.filter(
            classe=classe_id,
            semestre=premier_semestre,
            jour__nom=jour_nom
        ).select_related('matiere', 'enseignant', 'salle')
        
        # Premier créneau
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
        
        # Deuxième créneau
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

    print(emploi_global)
    #Semestre 2
    emploi_global1 = {}

    
    for jour_nom in jours_semaine:
        emploi_global1[jour_nom] = {
            'premier': {'horaire': '', 'details': ['Aucun', 'Aucun', 'Aucun'], 'existe': False},
            'deuxieme': {'horaire': '', 'details': ['Aucun', 'Aucun', 'Aucun'], 'existe': False}
        }
        
        # Requête pour le jour
        creneaux = EmploieDuTemps.objects.filter(
            classe=classe_id,
            semestre=second_semestre,
            jour__nom=jour_nom
        ).select_related('matiere', 'enseignant', 'salle')
        
        # Premier créneau
        premier = creneaux.filter(nature='1er').first()
        if premier:
            horaire = f"{premier.heure_debut.strftime('%H:%M')} - {premier.heure_fin.strftime('%H:%M')}"
            emploi_global1[jour_nom]['premier'] = {
                'horaire': horaire,
                'details': [
                    premier.matiere.nom if premier.matiere else 'Aucun',
                    f"{premier.enseignant.enseignant_utilisateur.nom} {premier.enseignant.enseignant_utilisateur.prenom}" if premier.enseignant else 'Aucun',
                    premier.salle.nom if premier.salle else 'Aucun'
                ],
                'existe': True
            }
        
        # Deuxième créneau
        deuxieme = creneaux.filter(nature='2eme').first()
        if deuxieme:
            horaire = f"{deuxieme.heure_debut.strftime('%H:%M')} - {deuxieme.heure_fin.strftime('%H:%M')}"
            emploi_global1[jour_nom]['deuxieme'] = {
                'horaire': horaire,
                'details': [
                    deuxieme.matiere.nom if deuxieme.matiere else 'Aucun',
                    f"{deuxieme.enseignant.enseignant_utilisateur.nom} {deuxieme.enseignant.enseignant_utilisateur.prenom}" if deuxieme.enseignant else 'Aucun',
                    deuxieme.salle.nom if deuxieme.salle else 'Aucun'
                ],
                'existe': True
            }


    print(emploi_global1)

    #Compter les etudiants 
    if liste.count() == 1:
        nombre = f'{liste.count()} etudiant'
    elif liste.count() == 0:
        nombre = 'Aucun etudiant'
    else:
        nombre = f'{liste.count()} etudiants'
    
    context = {
        'annee':AnneeAcademique.objects.get(id=1),
        'etudiant': liste,
        'classe': classe_id,
        'nombre': nombre,
        'S1': premier_semestre,
        'S2': second_semestre,
        'E1': emploi_global,
        'E2': emploi_global1,
        'jours_semaine': jours_semaine,
        'matieresS1': matieresS1,
        'matieresS2': matieresS2,
        'enseignants': Contrat.objects.all().order_by('enseignant'),
        'salles': salles,
        'intervenants1':ense,
        'intervenants2':ense1,
        'matiere':m1,
        'matiere1':m2,

    }
    return render(request, "pages/dashboard/admin/liste.html", context)

def logout_view(request,error):
    if error=='etudiant':
        logout(request)
        return etudiant_login(request=request,e=False)
    elif error=='prof':
        logout(request)
        return prof_login(request=request,e=False)
    elif error=='admin':
        logout(request)
        return admin_login(request=request,e=False)
        
def logout_views2(request):
    logout(request)
    return redirect('login')

def ecole(request):
    return render(request,'pages/presentation/site/ecole.html')
def presentation(request):
    return render(request,'pages/presentation/logiciel/logiciel.html')

def login_pages(request):
    return render(request,'pages/auth/login.html')

def etudiant_login(request,e=True):
    if e==True:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                # Redirection selon le rôle
                if user.role == Utilisateur.Role.ETUDIANT:
                    return redirect('etudiant_dashboard')
                else:
                    return logout_view(request=request,error='etudiant')
            else:
                return logout_view(request=request,error='etudiant')

                
        return render(request,'pages/auth/etudiant.html')
    else :
        context={'message':'veuillez verifier vos identifiants'}
        return render(request,'pages/auth/etudiant.html',context)
    
@login_required
def etudiant_dashboard(request):
    if request.user.role != Utilisateur.Role.ETUDIANT:
        return redirect('login_etudiant')
    
    # Informations de l'étudiant
    transaction = Transaction.objects.get(etudiant=request.user.id)
    classe = Classe.objects.get(id=transaction.classe.id)
    
    # Déterminer les semestres selon le niveau
    if classe.niveau.libelle == "L1":
        premier_semestre = Semestre.objects.get(nom_semestre='S1')
        second_semestre = Semestre.objects.get(nom_semestre='S2')
    if classe.niveau.libelle == "L2":
        premier_semestre = Semestre.objects.get(nom_semestre='S3')
        second_semestre = Semestre.objects.get(nom_semestre='S4')
    if classe.niveau.libelle == "L3":
        premier_semestre = Semestre.objects.get(nom_semestre='S5')
        second_semestre = Semestre.objects.get(nom_semestre='S6')
    # else:
    #     premier_semestre = Semestre.objects.first()
    #     second_semestre = Semestre.objects.last()

    # Récupérer l'emploi du temps structuré
    emplois_s1 = EmploieDuTemps.objects.filter(
        classe=classe,
        semestre=premier_semestre
    ).select_related('matiere', 'enseignant', 'salle', 'jour')

    # Structurer les données pour l'affichage
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    
    # Définir les créneaux horaires selon le niveau
    if classe.niveau.libelle == "L1":
        creneaux = {
            'premier': {'debut': '08:00', 'fin': '10:00'},
            'deuxieme': {'debut': '10:15', 'fin': '12:15'}
        }
    elif classe.niveau.libelle == "L2":
        creneaux = {
            'premier': {'debut': '12:25', 'fin': '14:25'},
            'deuxieme': {'debut': '14:35', 'fin': '16:35'}
        }
    elif classe.niveau.libelle == "L3":
        creneaux = {
            'premier': {'debut': '16:45', 'fin': '18:30'},
            'deuxieme': {'debut': '18:45', 'fin': '19:45'}
        }

    # Structure pour l'emploi du temps
    E1 = {}
    
    for jour in jours_semaine:
        E1[jour.lower()] = {
            'premier': {'existe': False, 'details': []},
            'deuxieme': {'existe': False, 'details': []}
        }

    # Remplir la structure avec les données réelles
    for emploi in emplois_s1:
        heure_debut = emploi.heure_debut.strftime('%H:%M')
        jour_nom = emploi.jour.nom
        
        # Déterminer le créneau
        creneau = None
        if heure_debut == creneaux['premier']['debut']:
            creneau = 'premier'
        elif heure_debut == creneaux['deuxieme']['debut']:
            creneau = 'deuxieme'
        
        if creneau and jour_nom.lower() in E1:
            E1[jour_nom.lower()][creneau] = {
                'existe': True,
                'details': [
                    emploi.matiere.nom,
                    f"{emploi.enseignant.enseignant_utilisateur.nom} {emploi.enseignant.enseignant_utilisateur.prenom}",
                    emploi.salle.nom
                ]
            }

    # Autres données...
    notes1 = Notes.objects.filter(etudiant=transaction.etudiant, semestre=premier_semestre).order_by('matiere','evaluation')
    
    # m1 = Matiere_Programmer.objects.filter(
    #     emploiedutemps__semestre_id=premier_semestre,
    #     emploiedutemps__classe_id=classe.id
    # ).distinct()
    
    # m2 = Matiere_Programmer.objects.filter(
    #     emploiedutemps__semestre_id=second_semestre,
    #     emploiedutemps__classe_id=classe.id
    # ).distinct()



    m1 = Matiere_Programmer.objects.filter(
        semestre=premier_semestre,
        classe=classe
    ).distinct()
    
    m2 = Matiere_Programmer.objects.filter(
        semestre=second_semestre,
        classe=classe
    ).distinct()




    aujourd_hui_numero = datetime.today().weekday()
    demain_numero = (datetime.today() + timedelta(days=1)).weekday()
    n=aujourd_hui_numero + 1
    n1=demain_numero + 1
    emploi_aujourdhui = EmploieDuTemps.objects.filter(
        classe=classe,
        semestre=premier_semestre,
        jour__numero=n
    ).order_by('heure_debut')

    print(n1)
    
    emploi_demain = EmploieDuTemps.objects.filter(
        classe=classe,
        semestre=premier_semestre,
        jour__numero=n1
    ).order_by('heure_debut')
    print(emploi_demain)
    dernieres_notes = Notes.objects.filter(
        etudiant=transaction.etudiant,
        semestre=premier_semestre
    ).order_by('matiere__nom')[:5]
# Dans la fonction etudiant_dashboard, ajoutez cette logique après la récupération des emplois du temps

# Récupérer les professeurs uniques avec leurs matières
    professeurs_data = {}
    for emploi in emplois_s1:
        enseignant_id = emploi.enseignant.id
        if enseignant_id not in professeurs_data:
            professeurs_data[enseignant_id] = {
                'enseignant': emploi.enseignant,
                'matieres': set(),
                # 'specialite':emploi.enseignant.enseignant_utilisateur.specialite,
            }
        professeurs_data[enseignant_id]['matieres'].add(emploi.matiere)

    # Convertir en liste pour le template
    professeurs_uniques = []
    for data in professeurs_data.values():
        professeurs_uniques.append({
            'enseignant': data['enseignant'],
            'matiere': list(data['matieres'])[0],  # Première matière pour le titre
            'matieres': list(data['matieres'])     # Toutes les matières pour la liste
        })

    # Ajouter au contexte
        programmes_cours = Programmes_Cour.objects.filter(
            matiere__emploiedutemps__classe=classe,
            annee=transaction.annee_academique
        ).distinct().select_related('enseignant', 'matiere', 'annee')

        programmes_cours_verifies = programmes_cours.filter(verifier=True)








    context = {
        'programmes_cours': programmes_cours,
        'programmes_cours_verifies': programmes_cours_verifies,
        'dernieres_notes': dernieres_notes,
        'notes': notes1,
        'today': emploi_aujourdhui,
        'yers': emploi_demain,
        'premier': premier_semestre,
        'second': second_semestre,
        'm1': m1,
        'm2': m2,
        'info': transaction,
        'etudiant': Etudiant.objects.get(id=request.user.id),
        'classe': classe,
        'E1': E1,
        'Em':emplois_s1,
        'professeurs_uniques': professeurs_uniques,
        'jours_semaine': jours_semaine,
    }
    return render(request, 'pages/dashboard/etudiant/etu.html', context)


def time_to_minutes(t):
    return t.hour * 60 + t.minute

def prof_login(request,e=True):
    if e==True:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                # Redirection selon le rôle
                if user.role == Utilisateur.Role.ENSEINGNANT:
                    return redirect('prof_dashboard')
                else:
                    return logout_view(request=request,error='prof')
            else:
                return logout_view(request=request,error='prof')

                
        return render(request,'pages/auth/prof.html')
    else :
        context={'message':'identifiant de ce prof est incorrect ,ressayer !'}
        return render(request,'pages/auth/prof.html',context)
@login_required
def prof_dashboard(request):
    if request.user.role != Utilisateur.Role.ENSEINGNANT:
        return redirect('login_prof')
    enseignant=Enseignant.objects.get(id=request.user.id)
    
    contrat=Contrat.objects.get(enseignant=enseignant)


    # Récupérer les cours en ligne existants
    cours_en_ligne = Programmes_Cour.objects.filter(enseignant=enseignant).order_by('-date_upload')
    
    # emploie
    emplois_du_temps = EmploieDuTemps.objects.filter(
        enseignant_id=enseignant,
        annee_academique_id=1
    ).select_related('classe')
    emplois_du_temps2 = EmploieDuTemps.objects.filter(
        enseignant_id=enseignant,
    )
    print(emplois_du_temps2)
    aujourd_hui_numero = datetime.today().weekday()
    demain_numero = (datetime.today() + timedelta(days=1)).weekday()
    n=aujourd_hui_numero + 1
    n1=demain_numero + 1
    emploi_aujourdhui = EmploieDuTemps.objects.filter(
        enseignant=enseignant,
        jour__numero=n
    ).order_by('heure_debut')

    print(n1)
    
    emploi_demain = EmploieDuTemps.objects.filter(
        enseignant=enseignant,
        jour__numero=n1
    ).order_by('heure_debut')


    # print(emploie)
    # Obtenir les classes distinctes
    classes_enseignant = set(emp.classe for emp in emplois_du_temps)
    
    # Compter les étudiants par classe
    resultats = []
    total_etudiants = 0
    
    for classe in classes_enseignant:
        # Compter les étudiants inscrits dans cette classe pour l'année académique
        nb_etudiants = Transaction.objects.filter(
            classe=classe,
            annee_academique_id=1
        ).count()
        
        resultats.append({
            'classe': classe,
            'nb_etudiants': nb_etudiants
        })
        total_etudiants += nb_etudiants

    ############################
    classes_matieres = {}
    
    for emploi in emplois_du_temps:
        classe_nom = emploi.classe.nom
        matiere_nom = emploi.matiere.nom
        
        if classe_nom not in classes_matieres:
            classes_matieres[classe_nom] = {}
        
        if matiere_nom not in classes_matieres[classe_nom]:
            # Calculer le nombre d'heures pour cette matière dans cette classe
            heures_matiere = sum(
                (time_to_minutes(emp.heure_fin) - time_to_minutes(emp.heure_debut)) / 60 
                for emp in emplois_du_temps 
                if emp.classe.nom == classe_nom and emp.matiere.nom == matiere_nom
            )
            
            classes_matieres[classe_nom][matiere_nom] = {
                'nom': matiere_nom,
                'heures_semaine': round(heures_matiere, 1),
                'classe': classe_nom
            }
    #######################################
    presences = PresenceCours.objects.filter(
        enseignant=enseignant
    ).select_related('classe', 'matiere', 'salle').order_by('-date_cours', '-heure_debut')
    
    # Statistiques des présences
    total_presences = presences.count()
    heures_enseignees = sum(presence.nombre_heure for presence in presences)
    

    
    # Calculer le total des heures
    total_heures = sum(
        matiere['heures_semaine'] 
        for classe in classes_matieres.values() 
        for matiere in classe.values()
    )
    print(len(resultats))
    print(total_etudiants)
    print(contrat)
    print(enseignant)
    #  espace_utilise = sum(cours.taille_fichier for cours in cours_en_ligne)
    context={
        'cours_en_ligne': cours_en_ligne,
        'classes_list': list(classes_enseignant),
        # 'espace_utilise': round(espace_utilise, 2),
        'total_matieres': sum(len(matieres) for matieres in classes_matieres.values()),
        'classes_matieres': classes_matieres,
        'prof':Enseignant.objects.get(id=request.user.id),
        'etudiants':total_etudiants,
        'classes':len(resultats),
        'contrat':contrat,
        'today': emploi_aujourdhui,
        'yers': emploi_demain,
        'cours':emplois_du_temps.count(),
        'lundi':emplois_du_temps2.filter(jour__numero=1).order_by('heure_debut'),
        'mardi':emplois_du_temps2.filter(jour__numero=2).order_by('heure_debut'),
        'mercredi':emplois_du_temps2.filter(jour__numero=3).order_by('heure_debut'),
        'jeudi':emplois_du_temps2.filter(jour__numero=4).order_by('heure_debut'),
        'vendredi':emplois_du_temps2.filter(jour__numero=5).order_by('heure_debut'),
        'samedi':emplois_du_temps2.filter(jour__numero=6).order_by('heure_debut'),
        'heure':round(sum((time_to_minutes(c.heure_fin) - time_to_minutes(c.heure_debut)) / 60 for c in EmploieDuTemps.objects.filter(enseignant_id=enseignant))),
        'presences': presences,
        'total_presences': total_presences,
        'heures_enseignees': heures_enseignees,
        # 'info':Contrat.objects.get(etudiant=request.user.id)
    }
    return render(request, 'pages/dashboard/prof/prof.html',context)



def admin_login(request,e=True):
    if e==True:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                # Redirection selon le rôle
                if user.role == Utilisateur.Role.ADMIN:
                    return redirect('admin_dashboard')
                else:
                    return logout_view(request=request,error='admin')
            else:
                return logout_view(request=request,error='admin')

                
        return render(request,'pages/auth/admin.html')
    else :
        context={'message':'identifiant incorrect ressayer!'}
        return render(request,'pages/auth/admin.html',context)
@login_required
def admin_dashboard(request):
    if request.user.role != Utilisateur.Role.ADMIN:
        return redirect('login_admin')
    classe=Classe.objects.all()
    transaction=PaiementEcolage.objects.all().last()
    emploie=EmploieDuTemps.objects.all().last()
    inscription=Transaction.objects.all().last()
    matiere=Matiere_Programmer.objects.all().distinct()
    matieres=Matiere_Programmer.objects.all().last()
    prof=Contrat.objects.all()
    salle=Salle.objects.all()
    inscriptions=Transaction.objects.all()
    print(inscriptions)
    
    # print(transaction.etudiant.utilisateur.nom)
    print(emploie)


    context={
        'classe':classe,
        'inscription':inscription,
        'inscriptions':inscriptions,
        'emploie':emploie,
        'transaction':transaction,
        'salle':salle,
        'matiere':matiere,
        'matieres':matieres,
        'prof':prof,

    }
    return render(request, 'pages/dashboard/admin/admin.html',context)

@admin_decorators
def details_etudiant(request,id):
    etudiant= get_object_or_404(Etudiant,id=id)
    transaction = get_object_or_404(Transaction,etudiant=etudiant,nature='inscription')
    classe_id = get_object_or_404(Classe, id=transaction.classe.id)
    print(classe_id)
    
    # Définir les semestres selon le niveau
    if classe_id.niveau.libelle == "L1":
        premier = Semestre.objects.get(nom_semestre='S1')
        second = Semestre.objects.get(nom_semestre='S2')
    elif classe_id.niveau.libelle == "L2":
        premier = Semestre.objects.get(nom_semestre='S3')
        second = Semestre.objects.get(nom_semestre='S4')
    elif classe_id.niveau.libelle == "L3":
        premier = Semestre.objects.get(nom_semestre='S5')
        second = Semestre.objects.get(nom_semestre='S6')
    soutenance=Paiement_soutenance.objects.filter(etudiant=etudiant).first()
    print(soutenance)
    m1=Matiere_Programmer.objects.filter(classe=transaction.classe,semestre=premier)
    m2=Matiere_Programmer.objects.filter(classe=transaction.classe,semestre=second)
    print(m1)
    a=m1.count()+2
    b=m2.count
    print(type(a))
    print(a)

    context={
        'info':transaction,
        'paiements':PaiementEcolage.objects.filter(etudiant=etudiant),
        'etudiant':etudiant,
        'soutenance_paid': soutenance,
        'm1':m1,
        'm2':m2,
        'total':m1.count()+m2.count(),
        'premier':premier,
        'second':second,
        'notes1':Notes.objects.filter(etudiant=etudiant,semestre=premier).order_by('matiere__nom'),
        'notes2':Notes.objects.filter(etudiant=etudiant,semestre=second).order_by('matiere__nom')

    }
    # return HttpResponse(f'etudiant {id}')
    return render(request,'pages/dashboard/etudiant/details.html',context)

@admin_decorators
def payement_ecolage(request,id):
    print(id)
    etudiant=Etudiant.objects.get(id=id)
    print(etudiant.utilisateur.nom)
    transaction=Transaction.objects.get(etudiant=etudiant)
    print(transaction)
    if request.method == 'POST':
        try:
            # Vérification préalable
            mois_id = request.POST.get('mois')
            mois= Mois.objects.get(id=mois_id)
            annee= AnneeAcademique.objects.get(id=transaction.annee_academique.id)
            classe= Classe.objects.get(id=transaction.classe.id)
            print(annee)
            print(mois)
            print(classe)
            montant= request.POST.get('montant')
            
            # CONTRÔLE 1: Vérifier si le montant d'inscription = 30000
            if transaction.montant != 30000:
                messages.error(
                    request, 
                    "Le paiement des écolages n'est autorisé que si les frais d'inscription s'élèvent à 30 000."
                )
                return redirect('ecolage',id=id)
            
            # CONTRÔLE 2: Vérifier si le mois précédent a été payé à 30000
            mois_precedent_numero = mois.numero - 1
            if mois_precedent_numero > 0:
                try:
                    mois_precedent = Mois.objects.get(numero=mois_precedent_numero)
                    paiement_mois_precedent = PaiementEcolage.objects.filter(
                        etudiant=etudiant,
                        annee_academique=annee,
                        mois=mois_precedent
                    ).first()
                    
                    # Si le mois précédent existe mais n'a pas été payé ou a été payé avec un montant différent de 30000
                    if not paiement_mois_precedent or paiement_mois_precedent.montant != 30000:
                        messages.error(
                            request, 
                            f"Le paiement du mois {mois.nom} n'est autorisé que si le mois précédent a été payé à 30 000."
                        )
                        return redirect('ecolage',id=id)
                        
                except Mois.DoesNotExist:
                    # Si le mois précédent n'existe pas dans la base (ex: janvier), on ne bloque pas
                    pass
            
            existe_deja = PaiementEcolage.objects.filter(
                    etudiant_id=etudiant,
                    annee_academique=annee,
                    mois=mois
                ).exists()
            
            if existe_deja:
                messages.error(
                    request, 
                    "Cet étudiant a déjà payé l'écolage pour ce mois de cette année académique."
                )
                return redirect('ecolage',id=id)
            
            # Création du paiement
            ecolage=PaiementEcolage.objects.create(
                etudiant=etudiant,
                annee_academique=annee,
                mois=mois,
                classe=classe,
                montant=montant,
            )
            
            context={'ecolage':ecolage}
            return render(request,'pages/transaction/paiement_reussie.html',context)
            
        except IntegrityError as e:
            if 'unique_paiement_ecolage_par_mois' in str(e):
                messages.error(request, "Cet étudiant a déjà payé l'écolage pour ce mois de cette année académique.")
            else:
                messages.error(request, f"Erreur de base de données: {str(e)}")
            
            return redirect('ecolage',id=id)
            
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('ecolage',id=id)

    context={
        'paiements':PaiementEcolage.objects.filter(etudiant=etudiant),
        'info':transaction,
        'etudiant':etudiant,
        'classes': Classe.objects.all(),
        'annees': AnneeAcademique.objects.all(),
        'annee':AnneeAcademique.objects.get(id=1),
        'mois': Mois.objects.all()
    }

    return render(request,'pages/transaction/ecolage.html',context)

@login_required
def impression_contrat(request,id):
    element=Contrat.objects.get(id=id)

    # Préparer le contexte
    context = {
        'element': element,
    }
    
    try:
        # Rendre le template HTML
        html_string = render_to_string('pages/pdf/contrat.html', context)
        
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Contrat de_{element.enseignant.enseignant_utilisateur.nom}{element.enseignant.enseignant_utilisateur.prenom}_{element.annee_academique.annee}.pdf"'
            return response
        else:
            return HttpResponse(f"Erreur lors de la génération du PDF: {pdf.err}")
            
    except Exception as e:
        # Gestion des erreurs
        return HttpResponse(f"Erreur lors de la génération du PDF: {str(e)}")


@admin_decorators
def impression_inscription(request,id):
    element=Transaction.objects.get(id=id)


    # Préparer le contexte
    context = {
        'element': element,
    }
    
    try:
        # Rendre le template HTML
        html_string = render_to_string('pages/pdf/enregistrement.html', context)
        
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{element.nature}_{element.etudiant.utilisateur.nom}{element.etudiant.utilisateur.prenom}_{element.annee_academique.annee}.pdf"'
            return response
        else:
            return HttpResponse(f"Erreur lors de la génération du PDF: {pdf.err}")
            
    except Exception as e:
        # Gestion des erreurs
        return HttpResponse(f"Erreur lors de la génération du PDF: {str(e)}")

@admin_decorators
def impression(request,id):
    ecolage=PaiementEcolage.objects.get(id=id)


    # Préparer le contexte
    context = {
        'ecolage': ecolage,
    }
    
    try:
        # Rendre le template HTML
        html_string = render_to_string('pages/pdf/scolarite.html', context)
        
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="ecolage_{ecolage.etudiant.utilisateur.nom}{ecolage.etudiant.utilisateur.prenom}_{ecolage.mois.nom}_{ecolage.annee_academique.annee}.pdf"'
            return response
        else:
            return HttpResponse(f"Erreur lors de la génération du PDF: {pdf.err}")
            
    except Exception as e:
        # Gestion des erreurs
        return HttpResponse(f"Erreur lors de la génération du PDF: {str(e)}")




@admin_decorators
def payement_soutenance(request,id):
    etudiant= get_object_or_404(Etudiant,id=id)
    transaction = get_object_or_404(Transaction,etudiant=etudiant)
    
    
    if transaction.classe.niveau.libelle != "L3":
        return HttpResponse("erreur: ....................cette etudiant n'est pas payer ces frais ci")
    

    # transaction=Transaction.objects.get(etudiant=etudiant)
    if request.method == 'POST' :
        try:
            # Vérification préalable
            # annee_id = request.POST.get('annee_academique')
            annee= AnneeAcademique.objects.get(id=transaction.annee_academique.id)
            # classe_id = request.POST.get('classe')
            classe= Classe.objects.get(id=transaction.classe.id)
            print(annee)
            print(classe)
            montant= request.POST.get('montant')
            existe_deja = Paiement_soutenance.objects.filter(
                    etudiant=etudiant,
                    annee_academique=annee,
            ).exists()
            
            
            if existe_deja:
                messages.error(
                    request, 
                    "Cet étudiant a déjà payé ses frais de soutenance pour cette année académique."
                )
                return redirect('soutenance',id=id)
            
            # Création du paiement
            # recu = Recu.objects.create(
            #             date=datetime.now().date(),
            #             heure=datetime.now().time(),
            #             montant=montant,
            #             description=f'{etudiant.utilisateur.nom}-{etudiant.utilisateur.prenom}-{mois.nom}-{annee.annee}-{classe.nom}',
            #             nature='frais de scolarite'
            #             )
            soutenance=Paiement_soutenance.objects.create(
                etudiant=etudiant,
                classe=classe,
                annee_academique=annee,
                montant=montant,
                # recu=recu
                )
            
            context={'ecolage':soutenance}
            return render(request,'pages/transaction/paiement_reussie.html',context)
            
        except IntegrityError as e:
            if 'unique_paiement_soutenance_par_an' in str(e):
                messages.error(request, "Cet étudiant a déjà payé ses frais de soutenance  de cette année académique.")
            else:
                messages.error(request, f"Erreur de base de données: {str(e)}")
            
            return redirect('soutenance',id=id)
            
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('soutenance',id=id)


    context={
        'info':transaction,
        'etudiant':etudiant,
        'classes': Classe.objects.all(),
        'annees': AnneeAcademique.objects.all()

    }

    

    return render(request,"pages/transaction/soutenance.html",context)

@admin_decorators
def payement_reinscription(request,id):
    #Fonction pour selectionner l'annee passer
    etudiant= get_object_or_404(Etudiant,id=id)
    transaction = get_object_or_404(Transaction,etudiant=etudiant)
    context={
        'info':transaction,
        'etudiant':etudiant,
        'classes': Classe.objects.all(),
        'annees': AnneeAcademique.objects.all()
    }
    print(id)
    return render(request,"pages/transaction/reinscription.html",context)


# def reinscription(request,nom):
#     # etudiantprofile=EtudiantProfile.objects.get(utilisateur=nom)
#     # etudiant=Etudiant.objects.get(username=etudiantprofile.utilisateur)
#     # transaction = Transaction.objects.get(etudiant=etudiant,nature="inscription")
#     # print(etudiant.username)
#     etudiant= get_object_or_404(Etudiant,username=nom)
#     etudiant_profile= get_object_or_404(EtudiantProfile,utilisateur=etudiant)
#     transaction = get_object_or_404(Transaction,etudiant=etudiant)
#     if request.method == 'POST': # verification de la methode 
#         if True:   # verification du jour 
            
#             #Information sur l'etudiant :

#             # nom = request.POST.get('nom')
#             # prenom = request.POST.get('prenom')
#             # date_naissance = request.POST.get('date_naissance')
#             # lieu_naissance = request.POST.get('lieu_naissance')
#             # adresse = request.POST.get('adresse')
#             # nationalite = request.POST.get('nationalite')
#             # telephone = request.POST.get('telephone')

#             # Récupération des champs liés à l'inscription :

#             classe_id = request.POST.get('classe_id')
#             annee_id = request.POST.get('annee_id')
#             nature = "reinscription"  # 'inscription' ou 'reinscription'
#             montant = float(request.POST.get('montant'))

#             # Vérification des documents fournis (cases cochées dans le formulaire)
#             ram = 'ram' in request.POST
#             marqueur = 'marqueur' in request.POST
#             dossier = 'dossier_inscription' in request.POST
#             bulletin = 'bulletin' in request.POST

#             # Récupération des objets de classe et année académique     
#             classe = get_object_or_404(Classe, pk=classe_id)
#             annee = get_object_or_404(AnneeAcademique, pk=annee_id)
            
#             #verification de l'existence de l'etudiant

#             if False:
#                 utilisateur = get_object_or_404( Etudiant, username=verification.utilisateur)
#                 # utilisateur.delete()
#                 if Transaction.objects.filter(etudiant=utilisateur, annee_academique=annee).exists():
#                     messages.error(request, "Cet étudiant est déjà inscrit pour cette année académique.")
#                     return redirect('inscription')
#                 else :
#                     utilisateur.delete()
#                     messages.error(request, " Veuiller ressayer ")
#                     return redirect('inscription')
#             else:

#                 recu = Recu.objects.create(
#                     date=datetime.now().date(),
#                     heure=datetime.now().time(),
#                     montant=montant,
#                     description=f'Frais de {nature}',
#                     nature=nature
#                     )
#                 transaction = Transaction.objects.create(
#                 etudiant=etudiant,
#                 classe=classe,
#                 annee_academique=annee,
#                 nature=nature,
#                 montant=montant,
#                 recu=recu,
#                 ram=ram,
#                 marqueur=marqueur,
#                 dossier_inscription=dossier
#                 )
                
#                 # recu_id=transaction.recu
#                 # print(recu_id)
#                 return redirect('inscription')    
#         else: return HttpResponse("le jour ou la date n'est pas favorable")



#     print(nom)
#     print(transaction.montant)

#     context={
#         'info':transaction,
#         'etudiant':etudiant_profile,
#         'classes': Classe.objects.all(),
#         'annees': AnneeAcademique.objects.all()
#     }
#     # print(transaction)
#     return render(request,"transaction/reinscription.html",context)


@admin_decorators
def liste_etudiant(request):
    option=Classe.objects.all()
    context={
        'options':option
    }
    return render(request,"pages/dashboard/admin/liste_cat.html",context)















