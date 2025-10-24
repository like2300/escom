from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    #INTERFACE -> etudiant 
    # path("/",views.inscription, name = "inscription"),


    #INTERFACE -> professeur

    path("emploie/<int:clas_id>/<uuid:semestre>",views.impression_emploie, name = "pdf_emp"),


    # path("liste/prof/<int:id>/",views.menu_details_prof, name = "menu_prof_details"),
    # path("liste/",views.menu_details_prof, name = "menu_prof_details"),

    # path("notes/prof/<int:id>/",views.menu_details_prof, name = "menu_prof_details"),

    #Pour les details juste afficher les informations du professeur et son contrat c'est tout 


]