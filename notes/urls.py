from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    #INSCRIPTION/REINSCRIPTION -> etudiant 
    path("notes/", views.menu, name="menu_notes"),
    path("notes/voir/<int:classe_id>/", views.menu_classe, name="notes_classe"),
    path("notes/saisie/<int:classe_id>", views.menu_saisie, name="notes_saisie"),
    path("bulletin/pdf/<int:etudiant_id>/<uuid:semestre_id>/", views.telecharger_bulletin_pdf, name="telecharger_bulletin_pdf"),
    path("classe/<int:classe_id>/pdf/", views.telecharger_notes_classe_pdf, name="telecharger_notes_classe_pdf"),
    path("classe/<int:classe_id>/excel/", views.telecharger_notes_classe_excel, name="telecharger_notes_classe_excel"),
    path("matiere/<int:classe_id>/<int:matiere_id>/pdf/", views.telecharger_notes_matiere_pdf, name="telecharger_notes_matiere_pdf"),
    path("matiere/<int:classe_id>/<int:matiere_id>/excel/", views.telecharger_notes_matiere_excel, name="telecharger_notes_matiere_excel"),
]


#ECOLAGE -> par classe etudiant
# path("menu/ecolages",views.ecolages_menu, name = "ecoalge"),

#SOUTENANCE -> par classe etudiant
# path("menu/ecolages",views.ecolages_menu, name = "ecoalge"),

#HONORAIRE -> prof
# path("menu/ecolages",views.ecolages_menu, name = "ecoalge"),