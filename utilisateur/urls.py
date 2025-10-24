from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    #INTERFACE -> etudiant 
    # path("/",views.inscription, name = "inscription"),


    #INTERFACE -> professeur
    path("administration/prof",views.menu_prof, name = "menu_prof"),
    path("administration/prof/<int:id>/",views.menu_details_prof, name = "menu_prof_details"),

    #Pour les details juste afficher les informations du professeur et son contrat c'est tout 


]