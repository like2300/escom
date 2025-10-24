from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    #INSCRIPTION/REINSCRIPTION -> etudiant 
    path("api/cree/emploie_du_temps",views.cree_emploie_du_temps, name = "cree_emploie_du_temps"),
    path("api/update/<int:id>",views.update_trans, name = "update_trans"),



]