from django.urls import path
from . import views


urlpatterns = [    
    # path("",views.presentation, name = "logiciel"),
    path('logout/', views.logout_view, name='logout'),
    path('out/', views.logout_views2, name='out'),
    path("",views.ecole, name = "ecole"),
    path("login/",views.login_pages, name = "login"),
    path("escom/connexion/etudiant",views.etudiant_login, name = "login_etudiant"),
    path('etudiant/', views.etudiant_dashboard, name='etudiant_dashboard'),
    path("escom/connexion/prof",views.prof_login, name = "login_prof"),
    path('prof/', views.prof_dashboard, name='prof_dashboard'),
    path("escom/connexion/administration",views.admin_login, name = "login_admin"),
    path('administration/', views.admin_dashboard, name='admin_dashboard'),
    path('administration/transactions', views.transactions, name='transactions'),
    path('administration/liste_etudiant/menu', views.liste_etudiant, name='liste_etudiants'),
    path('administration/liste_etudiant/menu/<str:classe>', views.etudiant_by_classe, name='etudiant_by_classe'),
    path('administration/details/etudiants/<int:id>', views.details_etudiant, name='etudiant_details'),
    path('administration/ecolage/<int:id>', views.payement_ecolage, name='ecolage'),
    path('administration/soutenance/<int:id>', views.payement_soutenance, name='soutenance'),
    path('administration/reinscription/etudiant/<int:id>', views.payement_reinscription, name='reinscription_etu'),
    path('impression/pdf/ecolage/<uuid:id>', views.impression, name='pdf'),
    path('impression/pdf/transaction/<uuid:id>', views.impression_inscription, name='pdf_trans'),
    path('impression/pdf/contrat/<uuid:id>', views.impression_contrat, name='pdf_contrat'),
    path('administration/prof/presences', views.presence, name='presence'),
    path('administration/prof/presences/<int:id>', views.enregistrement_presence, name='enregistrement_presence'),
    path('generer-matricules/<int:classe_id>/', views.generer_matricules_classe, name='generer_matricules'),
#statistique
    path('stats/', views.stats, name='stats'),
    path('honoraire/', views.honoraire, name='honoraire'),





    



]
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Tableaux de bord par rôle


    # path("",views.logiciel, name = "logiciel"),
    # path("login/",views.login, name = "login"),
    # path('logout/', views.logout_view, name='logout'),
    # path("dashboard/",views.dashboard, name = "dash"),
    # path("parametres/",views.tools, name = "tools"),
    # path('dashboard/', views.dashboard, name='admin_dashboard'),
    # path('etudiant/', views.student_dashboard, name='student_dashboard'),
    # path('professeur/', views.teacher_dashboard, name='teacher_dashboard'),