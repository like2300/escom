
from django.contrib import admin 
from unfold.admin import ModelAdmin
from .models import *

# Register your models here.

class UtilisateurAdmin(ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_display_links = ('id',)
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

class EtudiantAdmin(ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_display_links = ('id',)
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

class EnseignantAdmin(ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_display_links = ('id',)
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

class EtudiantProfileAdmin(ModelAdmin):
    list_display = ('id', 'utilisateur', 'nom', 'prenom', 'matricule', 'date_naissance', 'nationalite', 'numero_telephone')
    list_display_links = ('id',)
    list_filter = ('nationalite',)
    search_fields = ('nom', 'prenom', 'matricule', 'utilisateur__username')
    raw_id_fields = ('utilisateur',)

class EnseignantProfileAdmin(ModelAdmin):
    list_display = ('id', 'utilisateur', 'nom', 'prenom', 'matricule', 'date_naissance', 'nationalite', 'numero_telephone', 'slug')
    list_display_links = ('id',)
    list_filter = ('nationalite',)
    search_fields = ('nom', 'prenom', 'matricule', 'utilisateur__username')
    raw_id_fields = ('utilisateur',)
    prepopulated_fields = {'slug': ('nom', 'prenom')}

# Enregistrement des modèles avec leurs classes admin
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(EtudiantProfile, EtudiantProfileAdmin)
admin.site.register(EnseignantProfile, EnseignantProfileAdmin)









































# from django.contrib import admin 
from unfold.admin import ModelAdmin

# # Register your models here.
# from django.contrib import admin 
from unfold.admin import ModelAdmin
# from .models import *


# # Register your models here.
# #faut penser a optimiser la partie admin pour bien voir

# admin.site.register(Utilisateur)
# admin.site.register(Enseignant)
# admin.site.register(EnseignantProfile)
# admin.site.register(Etudiant)
# admin.site.register(EtudiantProfile)