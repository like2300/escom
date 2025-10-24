# forms.py
import os
from django import forms
from transactions.models import Programmes_Cour

class CoursEnLigneForm(forms.ModelForm):
    class Meta:
        model = Programmes_Cour
        fields = ['document', 'matiere','classe']
        widgets = {
            # 'titre': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Ex: Chapitre 1 - Introduction aux algorithmes'
            # }),
            # 'description': forms.Textarea(attrs={
            #     'class': 'form-control',
            #     'rows': 3,
            #     'placeholder': 'Décrivez le contenu de ce cours...'
            # }),
            'document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.ppt,.pptx,.zip,.rar,.txt'
            }),
            'matiere': forms.Select(attrs={'class': 'form-select'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),

        }
    
    def clean_fichier(self):
        fichier = self.cleaned_data.get('document')
        if fichier:
            # Vérifier la taille du fichier (max 50MB)
            max_size = 50 * 1024 * 1024  # 50MB en bytes
            if fichier.size > max_size:
                raise forms.ValidationError("La taille du fichier ne doit pas dépasser 50MB.")
            
            # Vérifier l'extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.zip', '.rar', '.txt']
            ext = os.path.splitext(fichier.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f"Type de fichier non autorisé. Formats acceptés: {', '.join(allowed_extensions)}"
                )
        
        return fichier