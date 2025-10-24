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
# from django.shortcuts import render,redirect,get_object_or_404
# # # from dataBase.models import *
from django.contrib import messages




def update_trans(request,id):
    etu=Etudiant.objects.get(id=id)

    if request.method == 'POST':
        montant = request.POST.get('montant')
        print(montant)
        ram = 'ram' in request.POST
        marqueur = 'marqueur' in request.POST
        Transaction.objects.filter(etudiant=etu).update(marqueur=marqueur,ram=ram,montant=montant)

        messages.success(request,'inscription mise a jour avec succes')
        return redirect('etudiant_details',id=id)
    etu=Etudiant.objects.get(id=id)
    trans=Transaction.objects.get(etudiant=etu)
    context={
        'trans':trans
    }
    print(print)
    return render(request,'pages/transaction/trans.html',context)





# def views_trans(request,id):
#     etu=Etudiant.objects.get(id=id)
#     trans=Transaction.objects.get(etudiant=etu)
#     context={
#         'trans':trans
#     }
#     print(print)
#     return render(request,'pages/transaction/trans.html',context)

# def update_trans(request,id):
#     transaction=Transaction.objects.get(id=id)

#     if request.method == 'POST':
#         montant = request.POST.get('montant')
#         print(montant)

#         return redirect('etudiant_details',id=id)


def cree_emploie_du_temps(request):
    if request.method == 'POST':
        classe_id = request.POST.get('classe')
        semestre_id = request.POST.get('semestre')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        matiere_id = request.POST.get('matiere')
        jour_id = request.POST.get('jour')
        creneau_id = request.POST.get('creneau')
        enseignant_id = request.POST.get('enseignant')
        salle_id = request.POST.get('salle')
        #cles d'acces au different table 
        annee = get_object_or_404(AnneeAcademique, pk=1)
        classe = get_object_or_404(Classe, pk=classe_id)
        semestre = get_object_or_404(Semestre, id=semestre_id)
        matiere= get_object_or_404(Matiere_Programmer, pk=matiere_id)
        jour = get_object_or_404(Jour, nom=jour_id)
        if creneau_id == 'premier':
            creneau='1er'
        else : creneau='2eme'
        enseignant= get_object_or_404(Enseignant, pk=enseignant_id)
        salle = get_object_or_404(Salle, pk=salle_id)
        
        

        print(annee)


        print(f'{classe} {semestre} {heure_debut} {heure_fin} {matiere} {salle} {enseignant} {creneau} {jour}')
        emploie=EmploieDuTemps.objects.create(
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            enseignant=enseignant,
            annee_academique=annee,
            classe=classe,
            jour=jour,
            matiere=matiere,
            salle=salle,
            semestre=semestre,
            nature=creneau

        )
        # return HttpResponse(f'classe:{classe} ,semestre:{semestre} heure debut:{heure_debut}, heure fin:{heure_fin}, matiere:{matiere}, salle:{salle}, enseignant:{enseignant}, creneau :{creneau}, jour:{jour} <br> {str(emploie)}' )

        return redirect('etudiant_by_classe',classe=str(classe_id))
    
    