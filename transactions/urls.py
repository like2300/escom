from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    #INSCRIPTION/REINSCRIPTION -> etudiant 
    path("inscription/",views.inscription, name = "inscription"),
    path("succes/<uuid:id>",views.success, name = "succes"),

    path('reinscription/', views.reinscription, name="reinscription"),
    path('recrutement/', views.recrutement, name="recrutement")


    #ECOLAGE -> par classe etudiant
    # path("menu/ecolages",views.ecolages_menu, name = "ecoalge"),

    #SOUTENANCE -> par classe etudiant
    # path("menu/ecolages",views.ecolages_menu, name = "ecoalge"),

    #HONORAIRE -> prof
    # path("menu/ecolages",views.ecolages_menu, name = "ecoalge"),

]