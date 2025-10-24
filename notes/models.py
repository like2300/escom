from django.db import models
from database.models import *
from transactions.models import *
# Create your models here.

class Notes(models.Model):
    annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    etudiant=models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    semestre=models.ForeignKey(Semestre, on_delete=models.CASCADE)
    evaluation=models.CharField(
        max_length=50,
        choices=[('devoir', 'devoir'), ('session', 'session')],
        help_text="notes du devoir ou de la session",
        default=None
    )
    matiere=models.ForeignKey(Matiere_Programmer, on_delete=models.CASCADE)
    classe=models.ForeignKey(Classe, on_delete=models.CASCADE)
    note = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.etudiant} - {self.evaluation} - {self.matiere} : {str(self.note)}'
    class Meta:
        verbose_name = "Note"
        verbose_name_plural = " Notes"

    