from django.contrib import admin 
from unfold.admin import ModelAdmin
from .models import *
# from unfold import ModelAdmin  confi import 
from unfold.admin import ModelAdmin

class NotesAdmin(ModelAdmin):
    list_display = ('id', 'etudiant', 'classe', 'matiere', 'semestre', 'evaluation', 'note', 'annee_academique')
    list_display_links = ('id',)
    list_filter = ('etudiant', 'classe', 'annee_academique', 'semestre', 'evaluation', 'matiere')
    search_fields = ('etudiant__username', 'etudiant__first_name', 'etudiant__last_name', 'matiere__nom', 'classe__nom')
    ordering = ('etudiant', 'classe', 'semestre', 'matiere')
    
    # Configuration pour le regroupement
    def changelist_view(self, request, extra_context=None):
        # Personnalisation supplémentaire si nécessaire
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_queryset(self, request):
        # Préchargement des relations pour optimiser les performances
        return super().get_queryset(request).select_related(
            'etudiant', 'matiere', 'classe', 'semestre', 'annee_academique'
        )

# Register your models here.
admin.site.register(Notes, NotesAdmin)

































# from django.contrib import admin 
from unfold.admin import ModelAdmin
# from .models import *

# class NotesAdmin(ModelAdmin):
#     list_display = ('id', 'etudiant', 'matiere', 'classe', 'semestre', 'evaluation', 'note', 'annee_academique')
#     list_display_links = ('id',)
#     list_filter = ('etudiant', 'annee_academique', 'semestre', 'classe', 'evaluation', 'matiere')
#     search_fields = ('etudiant__username', 'etudiant__first_name', 'etudiant__last_name', 'matiere__nom', 'classe__nom')
#     ordering = ('etudiant', 'semestre', 'matiere')
    
#     def get_queryset(self, request):
#         # Préchargement des relations pour optimiser les performances
#         return super().get_queryset(request).select_related(
#             'etudiant', 'matiere', 'classe', 'semestre', 'annee_academique'
#         )

# # Register your models here.
# admin.site.register(Notes, NotesAdmin)