from django.contrib import admin 
from unfold.admin import ModelAdmin
from .models import *

# Register your models here.

class AnneeAcademiqueAdmin(ModelAdmin):
    list_display = ('id', 'annee', 'debut_annee', 'fin_annee', 'est_active')
    list_display_links = ('id',)

class CycleAdmin(ModelAdmin):
    list_display = ('id', 'libelle', 'description')
    list_display_links = ('id',)

class FiliereAdmin(ModelAdmin):
    list_display = ('id', 'libelle', 'description')
    list_display_links = ('id',)

class NiveauAdmin(ModelAdmin):
    list_display = ('id', 'libelle', 'description')
    list_display_links = ('id',)

class ClasseAdmin(ModelAdmin):
    list_display = ('id', 'nom', 'cycle', 'niveau', 'option', 'description')
    list_display_links = ('id',)

class RecuAdmin(ModelAdmin):
    list_display = ('id', 'date', 'heure', 'montant', 'description', 'nature')
    list_display_links = ('id',)

class TransactionAdmin(ModelAdmin):
    list_display = ('id', 'date', 'montant', 'nature', 'classe', 'etudiant', 'annee_academique')
    list_display_links = ('id',)

class ContratAdmin(ModelAdmin):
    list_display = ('id', 'enseignant', 'annee_academique', 'date', 'description')
    list_display_links = ('id',)

class TarifAdmin(ModelAdmin):
    list_display = ('id', 'frais_inscription', 'frais_reinscription', 'frais_mensuels', 'niveau', 'annee_academique')
    list_display_links = ('id',)

class OptionAdmin(ModelAdmin):
    list_display = ('id', 'libelle', 'filiere', 'description')
    list_display_links = ('id',)

class PaiementEcolageAdmin(ModelAdmin):
    list_display = ('id', 'etudiant', 'annee_academique', 'mois', 'classe', 'montant', 'date')
    list_display_links = ('id',)

class PaiementSoutenanceAdmin(ModelAdmin):
    list_display = ('id', 'classe', 'etudiant', 'annee_academique', 'montant')
    list_display_links = ('id',)

class MoisAdmin(ModelAdmin):
    list_display = ('id', 'numero', 'nom')
    list_display_links = ('id',)

class SalleAdmin(ModelAdmin):
    list_display = ('id', 'nom', 'capacite')
    list_display_links = ('id',)

class EmploieDuTempsAdmin(ModelAdmin):
    list_display = ('id', 'heure_debut', 'heure_fin', 'enseignant', 'classe', 'jour', 'matiere', 'salle', 'semestre', 'nature')
    list_display_links = ('id',)

class MatiereProgrammerAdmin(ModelAdmin):
    list_display = ('id', 'nom', 'code', 'semestre', 'annee_academique', 'classe', 'coefficient')
    list_display_links = ('id',)

class JourAdmin(ModelAdmin):
    list_display = ('id', 'numero', 'nom')
    list_display_links = ('id',)

class SemestreAdmin(ModelAdmin):
    list_display = ('id', 'nom_semestre', 'annee_academique', 'mois_debut', 'mois_fin', 'description')
    list_display_links = ('id',)

class PresenceCoursAdmin(ModelAdmin):
    list_display = ('id', 'heure_debut', 'heure_fin', 'date_cours', 'enseignant', 'classe', 'matiere', 'salle', 'nombre_heure')
    list_display_links = ('id',)


class ProgrammesCourAdmin(ModelAdmin):
    list_display = ('id', 'nom', 'enseignant', 'matiere','classe__nom', 'annee', 'verifier', 'date_upload')
    list_display_links = ('id', 'nom')
    list_filter = ('verifier', 'annee', 'enseignant', 'matiere','classe')
    search_fields = ('nom', 'enseignant__nom', 'enseignant__prenom', 'matiere__nom','classe__nom')
    readonly_fields = ('id', 'date_upload')
    list_editable = ('verifier',)
    date_hierarchy = 'date_upload'
    
    # Optionnel : afficher le nom du fichier dans l'admin
    def document_name(self, obj):
        return obj.document.name if obj.document else "Aucun document"
    document_name.short_description = "Nom du document"

    # Si vous voulez ajouter document_name dans list_display
    # list_display = ('id', 'nom', 'enseignant', 'matiere', 'annee', 'verifier', 'date_upload', 'document_name')

# Enregistrement du modèle avec sa classe admin

# Enregistrement des modèles avec leurs classes admin
admin.site.register(AnneeAcademique, AnneeAcademiqueAdmin)
admin.site.register(Cycle, CycleAdmin)
admin.site.register(Filiere, FiliereAdmin)
admin.site.register(Niveau, NiveauAdmin)
admin.site.register(Classe, ClasseAdmin)
admin.site.register(Recu, RecuAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(Tarif, TarifAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(PaiementEcolage, PaiementEcolageAdmin)
admin.site.register(Paiement_soutenance, PaiementSoutenanceAdmin)
admin.site.register(Mois, MoisAdmin)
admin.site.register(Salle, SalleAdmin)
admin.site.register(EmploieDuTemps, EmploieDuTempsAdmin)
admin.site.register(Matiere_Programmer, MatiereProgrammerAdmin)
admin.site.register(Jour, JourAdmin)
admin.site.register(Semestre, SemestreAdmin)
admin.site.register(PresenceCours, PresenceCoursAdmin)
admin.site.register(Programmes_Cour, ProgrammesCourAdmin)









































# from django.contrib import admin 
from unfold.admin import ModelAdmin
# from .models import *


# Register your models here.
#faut penser a optimiser la partie admin pour bien voir

# admin.site.register(AnneeAcademique)
# admin.site.register(Cycle)
# admin.site.register(Filiere)
# admin.site.register(Niveau)
# admin.site.register(Classe)
# admin.site.register(Recu)
# admin.site.register(Transaction)
# admin.site.register(Contrat)
# admin.site.register(Tarif)
# admin.site.register(Option)
# admin.site.register(PaiementEcolage)
# admin.site.register(Paiement_soutenance)
# admin.site.register(Mois)
# admin.site.register(Salle)
# admin.site.register(EmploieDuTemps)
# admin.site.register(Matiere_Programmer)
# admin.site.register(Jour)
# admin.site.register(Semestre)
# admin.site.register(PresenceCours)




