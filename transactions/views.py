from django.shortcuts import render,redirect,get_object_or_404
from database.models import *
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime,date,time
# from emploieDutemps.models import EmploieDuTemps,Jour
# from django.db.models import Q
# from heures_cours.models import PresenceCours
# from django.db.models import Count, Sum, Avg,F, FloatField, ExpressionWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login,logout
from django.http import HttpResponseForbidden

from .utils import *

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
def recrutement(request):
    if request.method == 'POST':
        random="composition random"
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        lieu_naissance = request.POST.get('lieu_naissance')
        niveau_etude = request.POST.get('niveau_etude')
        diplome = request.POST.get('diplome')
        specialite = request.POST.get('specialite')
        adresse = request.POST.get('adresse')
        nationalite = request.POST.get('nationalite')
        telephone = request.POST.get('telephone')
        annee_id = request.POST.get('annee_id')

        # Vérification des documents fournis (cases cochées dans le formulaire)
        cv = 'cv' in request.POST
        diplomes_copies = 'diplomes_copies' in request.POST
        lettre_motivation = 'lettre_motivation' in request.POST
        pieces_identite = 'pieces_identite' in request.POST
        attestations_travail = 'attestations_travail' in request.POST
        autres_documents= 'autres_documents' in request.POST

        # année académique     
        annee = get_object_or_404(AnneeAcademique, pk=annee_id)
        
        verifications = EnseignantProfile.objects.filter(nom=nom,prenom=prenom).first()
        print(verifications)

        if Utilisateur.objects.filter(username=f'{nom}_{prenom}@prof').exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('inscription')


        if verifications:
            messages.error(request,"cette enregistrement a deja ete fait")
            return redirect('recrutement')

        else:
            prof=f'{nom}_{prenom}@prof'
            enseignant=Enseignant.objects.create(username=prof)
            profile,created=EnseignantProfile.objects.get_or_create(utilisateur=enseignant)
            profile.nom=nom
            profile.prenom=prenom
            profile.date_naissance=date_naissance
            profile.lieu_naissance=lieu_naissance
            profile.adresse=adresse
            profile.nationalite=nationalite
            profile.numero_telephone=telephone
            slug=slugify(f'{nom}_{prenom}')
            profile.cree_par=f'{request.user}'
            profile.save()
            contrat=Contrat.objects.create(
                enseignant=enseignant,
                annee_academique=annee,
                description=specialite
            )
            context={ 
                'url':contrat
            }
            return render(request,'pages/transaction/recrutement_success.html',context)


    context={
        'annee':AnneeAcademique.objects.all()
    }
    return render(request,'pages/transaction/recrutement.html',context)

@admin_decorators
def transaction_invalid(request):
    return render(request,"pages/transaction/transaction_bloquer.html") 
@admin_decorators
def success(request,id):
    context={
        'element':Transaction.objects.get(id=id)
    }
    return render(request,"pages/transaction/succes.html",context)


# verification(datetime.now())




@admin_decorators
def reinscription(request):
    return render(request,"pages/transaction/redirection_reinscription.html")    


@admin_decorators
def inscription(request):
    if request.user.role != Utilisateur.Role.ADMIN:
        return redirect('/ecole/login/admin')
    else:
        if request.method == 'POST': # verification de la methode 
            if True:   # verification du jour 
                
                #Information sur l'etudiant :

                nom = request.POST.get('nom')
                prenom = request.POST.get('prenom')
                date_naissance = request.POST.get('date_naissance')
                lieu_naissance = request.POST.get('lieu_naissance')
                adresse = request.POST.get('adresse')
                nationalite = request.POST.get('nationalite')
                telephone = request.POST.get('telephone')
                # Récupération des champs liés à l'inscription :
                classe_id = request.POST.get('classe_id')
                annee_id = request.POST.get('annee_id')
                nature = "inscription"  # 'inscription' ou 'reinscription'
                montant = float(request.POST.get('montant'))
                # Vérification des documents fournis (cases cochées dans le formulaire)
                ram = 'ram' in request.POST
                marqueur = 'marqueur' in request.POST
                dossier = 'dossier_inscription' in request.POST
                bulletin = 'bulletin' in request.POST
                # Récupération des objets de classe et année académique     
                classe = get_object_or_404(Classe, pk=classe_id)
                annee = get_object_or_404(AnneeAcademique, pk=annee_id)
                #verification de l'existence de l'etudiant
                if Utilisateur.objects.filter(username=f'{nom}_{prenom}').exists():
                    messages.error(request, "Ce nom d'utilisateur est déjà pris.")
                    return redirect('inscription')
                verifications = EtudiantProfile.objects.filter(nom=nom,prenom=prenom).first()
                if verifications:
                    utilisateur = get_object_or_404( Etudiant, username=verifications.utilisateur)
                    # utilisateur.delete()
                    if Transaction.objects.filter(etudiant=utilisateur, annee_academique=annee).exists():
                        messages.error(request, "Cet étudiant est déjà inscrit pour cette année académique.")
                        return redirect('inscription')
                    else :
                        utilisateur.delete()
                        messages.error(request, " Veuiller ressayer ")
                        return redirect('inscription')
                else:
                #Creation de l'etudiant 
                    etu=f'{nom}_{prenom}'
                    etudiantuser=Etudiant.objects.create(username=etu)
                    profile,created=EtudiantProfile.objects.get_or_create(utilisateur=etudiantuser)
                    profile.nom=nom
                    profile.prenom=prenom
                    profile.date_naissance=date_naissance
                    profile.lieu_naissance=lieu_naissance
                    profile.adresse=adresse
                    profile.nationalite=nationalite
                    profile.numero_telephone=telephone
                    profile.cree_par=f'{request.user}'
                    profile.save()
                    recu = Recu.objects.create(
                        date=datetime.now().date(),
                        heure=datetime.now().time(),
                        montant=montant,
                        description=f'Frais de {nature}',
                        nature=nature
                        )
                    transaction = Transaction.objects.create(
                    etudiant=etudiantuser,
                    classe=classe,
                    annee_academique=annee,
                    nature=nature,
                    montant=montant,
                    recu=recu,
                    ram=ram,
                    marqueur=marqueur,
                    dossier_inscription=dossier
                    )
                    return redirect('succes',id=transaction.id)
            else:
                # messages.error(request, f"{datetime.now().date()} ou {datetime.now().time().hour}h ,la date ou l'heure pose probleme")
                # return redirect('inscription')
                return transaction_invalid(request=request)

    context = {
                    'classes': Classe.objects.all(),
                    'annees': AnneeAcademique.objects.all()
                }
    return render(request,"pages/transaction/inscription.html",context)

# impression recu
# def get_recu(request,el):
#     recu=get_object_or_404(Transaction,recu=el)
#     context={
#         'transaction':recu
#     }

#     return render(request,'recu/recu_inscription.html', context) 










