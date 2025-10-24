from django.db import models
from database.models import *
import datetime
import uuid
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import os
from django.core.validators import FileExtensionValidator

# # Create your models here.

class AnneeAcademique(models.Model): #(verifier pas tester)
    annee=models.CharField(max_length=255)
    debut_annee=models.DateField()
    fin_annee=models.DateField()
    est_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        today = datetime.date.today()
        self.es_active = self.debut_annee <= today <= self.fin_annee

        if not self.annee:
            self.annee=f'{self.debut_annee.year()}-{self.fin_annee.year()}'
        if not self.slug :
            self.slug = slugify(f'{self.debut_annee.year()}-{self.fin_annee.year()}')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.annee
    class Meta:
        verbose_name = "Annee academique"
        verbose_name_plural = "Annees academique"


#class Horaire(models.Model):
#nature(matin,apres-midi,soir)
#premier-heure=models.IntegerField()
#premier-heure=models.IntegerField()
#premier-heure=models.IntegerField()

#@property premiere heure(self)
#heure={self.premier}-{self.dernier}(operation pour les minutes et les temps de repos)

# class idSemestre(models.Model):

# class semestre(models.Model):
#     nom=


# mettre en place un slug pour gerer la description
# ex: Cycle 1 (Licence – Bac+3) Cycle 2 (Master – Bac+5)Cycle 3 (Doctorat – Bac+8)


class Cycle(models.Model):#integre des horaire par rapport au cycle
    libelle=models.CharField(max_length=255)#cycle 1
    description=models.CharField(max_length=255)#licence-bac+3
    




    def __str__(self):
        return self.libelle
    

class Niveau(models.Model):
    libelle=models.CharField(max_length=255)
    description=models.CharField(max_length=255)


    def __str__(self):
        return self.libelle
    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
    

class Filiere(models.Model):
    libelle = models.CharField(max_length=255)
    description=models.CharField(max_length=255)


    def __str__(self):
        return self.libelle

class Option(models.Model):
    # code=models.CharField(max_length=255)#GI,DI ,etc........
    libelle = models.CharField(max_length=255)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    description=models.CharField(max_length=255)


    def __str__(self):
        return self.libelle
    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"


class Classe(models.Model):
    nom = models.CharField(max_length=255)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    description=models.CharField(max_length=255)


    def __str__(self):
        return f'{self.niveau}-{self.option}-{self.cycle}'
    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"





class Recu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now=True)
    heure = models.TimeField()
    montant = models.IntegerField()
    description = models.CharField(max_length=255)
    nature = models.CharField(max_length=255)
    # operation = models.CharField(
    #     max_length=50,
    #     choices=[('entree', 'E'), ('sortie', 'S')],
    #     help_text="sotie ou entree d'argent"
    # )
    # slug = models.SlugField(max_length=200, unique=True, blank=True)
    # code_operation= models.CharField(max_length=255,blank=True,null=True)
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         # Génère le slug à partir du titre si vide
    #         self.slug = slugify(self.)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = "Recu"
        verbose_name_plural = "Recus"


class Tarif(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frais_inscription = models.DecimalField(max_digits=10, decimal_places=2)
    frais_reinscription = models.DecimalField(max_digits=10, decimal_places=2)
    # frais_soutenance = models.DecimalField(max_digits=10, decimal_places=2,default=None,blank=True,null=True)
    frais_mensuels = models.DecimalField(max_digits=10, decimal_places=2)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    # slug = models.SlugField(max_length=200, unique=True, blank=True)
    

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = "Tarif "
        verbose_name_plural = "Tarifs"




class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    nature = models.CharField(
        max_length=50,
        choices=[('inscription', 'Inscription'), ('reinscription', 'Réinscription')],
        help_text="inscription ou réinscription."
    )
    

    # Documents fournis pour le dossier d'inscription
    ram = models.BooleanField(default=False)
    marqueur = models.BooleanField(default=False)
    dossier_inscription = models.BooleanField(default=False)
    bulletin = models.BooleanField(default=False)

    # Références étrangères
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE,related_name='transaction')
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    recu = models.ForeignKey(Recu,on_delete=models.CASCADE)  #,related_name='recu',  related_query_name='recus' 
    # slug = models.SlugField(max_length=200, unique=True, blank=True)

        # class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['etudiant', 'annee_academique'],
        #         name='unique_transaction_par_an_etudiant'
        #     )
        # ]
        # verbose_name = "Paiement d'écolage"
        # verbose_name_plural = "Paiements d'écolages"
    class Meta:
        unique_together = ('etudiant', 'annee_academique')  # interdit plusieurs transactions par étudiant et année
        verbose_name = "Inscription ou reinscription"
        verbose_name_plural = "Inscriptions ou reinscriptions"

    def __str__(self):
        return str(self.id)

#Voir comment peut s'integrer la table semestre et operation (demander a rock le mcd)

#Payement des frais d'ecolage
class Mois(models.Model):

    numero=models.IntegerField()
    nom=models.CharField()

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = "Mois"
        verbose_name_plural = "Mois"
    
class PaiementEcolage(models.Model):##Etudiant,classe,anneeacademique,mois
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    etudiant=models.ForeignKey(Etudiant, on_delete=models.CASCADE,)
    annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    mois=models.ForeignKey(Mois,on_delete=models.CASCADE)
    classe=models.ForeignKey(Classe,on_delete=models.CASCADE)
    montant=models.IntegerField()
    # recu=models.ForeignKey(Recu,on_delete=models.CASCADE)
    date= models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['etudiant', 'annee_academique', 'mois'], 
                name='unique_paiement_par_mois_annee'
            )
        ]
        verbose_name = "Paiement d'ecolage"
        verbose_name_plural = "Paiement d'ecolages"


    def __str__(self):
        return str(self.id)

class Paiement_soutenance(models.Model):##Etudiant,classe,anneeacademique
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classe=models.ForeignKey(Classe,on_delete=models.CASCADE)
    etudiant=models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    montant=models.IntegerField(default=0)
    # date= models.DateField(auto_now=True,default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['etudiant', 'annee_academique'],
                name='unique_paiement_soutenance_par_an'
            )
        ]
        verbose_name = "Paiement de soutenance"
        verbose_name_plural = "Paiements de soutenance"

    def __str__(self):
        return str(self.id)
    
#contrainte d'unicite

#le try and catch pour les erreurs

class Contrat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enseignant=models.ForeignKey(Enseignant, on_delete=models.CASCADE,related_name='contrat')
    annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    date= models.DateField(auto_now=True)                                      
    description=models.CharField(max_length=255)
    # specialite=models.CharField(max_length=255)
    #CV=models.Boolean(max_length=255)
    # Copiesdiplômes=models.Boolean(max_length=255)
    # LettreMotivation=models.Boolean(max_length=255)
    # PieceIdentite=models.Boolean(max_length=255)
    # AttestationTravail=models.Boolean(max_length=255)
    # AutresDocument=models.Boolean(max_length=255)

    def __str__(self):
        return str(self.id)
    class Meta:
        unique_together = ('enseignant', 'annee_academique')  
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats "

#Emploie du temps
class Semestre(models.Model):
    class NomSemestre(models.TextChoices):
        S1 = 'S1', _('Semestre 1')
        S2 = 'S2', _('Semestre 2')
        S3 = 'S3', _('Semestre 3')
        S4 = 'S4', _('Semestre 4')
        S5 = 'S5', _('Semestre 5')
        S6 = 'S6', _('Semestre 6')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_semestre = models.CharField(max_length=2,choices=NomSemestre.choices,verbose_name="Nom du semestre")
    annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    mois_debut = models.CharField(verbose_name="mois de début",default=None)
    mois_fin = models.CharField(verbose_name="mois de fin",default=None)
    description = models.TextField(blank=True,null=True,verbose_name="Description du semestre")
    # slug = models.SlugField(max_length=200, unique=True, blank=True)

    # def save(self, *args, **kwargs):
    #     today = datetime.date.today()
    #     self.es_active = self.debut_annee <= today <= self.fin_annee

    #     if not self.annee:
    #         self.annee=f'{self.debut_annee.year()}-{self.fin_annee.year()}'
    #     if not self.slug :
    #         self.slug = slugify(f'{self.debut_annee.year()}-{self.fin_annee.year()}')

    #     super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"

    
    def __str__(self):
        return self.nom_semestre
    



# 


class Jour(models.Model): #Essai de voir si c'est possible que sa soi manuellement les jours
    
    numero=models.IntegerField()
    nom=models.CharField()
    
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name = "Jour"
        verbose_name_plural = "Jours"

class Salle(models.Model):

    nom=models.CharField()
    capacite = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"


class Matiere_Programmer(models.Model):

    nom = models.CharField(max_length=200,)
    code = models.CharField(max_length=20, unique=True, )
    semestre = models.ForeignKey(Semestre,on_delete=models.CASCADE,)
    annee_academique = models.ForeignKey(AnneeAcademique,on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe,on_delete=models.CASCADE)
    coefficient = models.PositiveIntegerField(default=1)


    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        
    def __str__(self):
        return self.nom

    
class EmploieDuTemps(models.Model): #mettre une liste de duree predeterminee(1ans,2ans,3ans,4ans)

    heure_debut=models.TimeField()
    heure_fin=models.TimeField()
    enseignant=models.ForeignKey(Enseignant, on_delete=models.CASCADE,)
    annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    classe=models.ForeignKey(Classe, on_delete=models.CASCADE)
    jour=models.ForeignKey(Jour, on_delete=models.CASCADE)
    matiere=models.ForeignKey(Matiere_Programmer, on_delete=models.CASCADE)
    salle=models.ForeignKey(Salle, on_delete=models.CASCADE)
    semestre=models.ForeignKey(Semestre, on_delete=models.CASCADE,default=None)
    nature = models.CharField(
        max_length=50,
        choices=[('1er', '1er'), ('2eme', '2eme')],
        help_text="1er heure ou 2eme heure",
        default=None
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['semestre', 'classe', 'jour', 'nature', 'annee_academique'],
                name='unique_emploi_du_temps'
            )
        ]
        verbose_name = "Emploie du temps"
        verbose_name_plural = "Emploies du temps"

    # def clean(self):
    #     """
    #     Validation supplémentaire pour s'assurer qu'il n'y a pas de chevauchement
    #     pour le même enseignant dans la même période
    #     """
    #     super().clean()
        
    #     if self.pk is None:  # Only for new instances
    #         # Vérifier les conflits pour le même enseignant, même jour, même créneau horaire
    #         conflits = EmploieDuTemps.objects.filter(
    #             enseignant=self.enseignant,
    #             jour=self.jour,
    #             annee_academique=self.annee_academique,
    #             semestre=self.semestre
    #         ).exclude(pk=self.pk)  # Exclure l'instance actuelle si elle existe

    #         # Vérifier le chevauchement horaire
    #         for emploi in conflits:
    #             if (self.heure_debut < emploi.heure_fin and 
    #                 self.heure_fin > emploi.heure_debut):
    #                 raise ValidationError(
    #                     f"L'enseignant {self.enseignant} a déjà un cours programmé "
    #                     f"le {self.jour} entre {emploi.heure_debut} et {emploi.heure_fin}"
    #                 )

    #         # Vérifier les conflits de salle dans le même créneau horaire
    #         conflits_salle = EmploieDuTemps.objects.filter(
    #             salle=self.salle,
    #             jour=self.jour,
    #             annee_academique=self.annee_academique,
    #             semestre=self.semestre
    #         ).exclude(pk=self.pk)

    #         for emploi in conflits_salle:
    #             if (self.heure_debut < emploi.heure_fin and 
    #                 self.heure_fin > emploi.heure_debut):
    #                 raise ValidationError(
    #                     f"La salle {self.salle} est déjà occupée le {self.jour} "
    #                     f"entre {emploi.heure_debut} et {emploi.heure_fin}"
    #                 )

    # def save(self, *args, **kwargs):
    #     """
    #     Surcharge de la méthode save pour appeler la validation
    #     """
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f' {self.jour.nom}:{self.heure_debut.hour}h-{self.heure_fin.hour}h {self.matiere.nom} {self.enseignant} {self.salle.nom}'



# Faut cree une table moyenne _________________________________________________________________-


class PresenceCours(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    heure_debut=models.TimeField() # celui de l'emploi du temps
    heure_fin=models.TimeField() # celui de l'emploie du temps
    date_cours=models.DateField( auto_now=True,)
    enseignant=models.ForeignKey(Enseignant, on_delete=models.CASCADE,)
    annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    classe=models.ForeignKey(Classe, on_delete=models.CASCADE)
    jour=models.ForeignKey(Jour, on_delete=models.CASCADE)
    matiere=models.ForeignKey(Matiere_Programmer, on_delete=models.CASCADE)
    salle=models.ForeignKey(Salle, on_delete=models.CASCADE)
    emploie_id=models.IntegerField(blank=True)
    nombre_heure=models.IntegerField(blank=True,)


    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = "Presence au cours "
        verbose_name_plural = "Presences aux cours"







def upload_to_programmes(instance, filename):
    # Génère un chemin unique pour chaque fichier
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join('programmes_cours', filename)

class Programmes_Cour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    verifier = models.BooleanField(default=False)
    nom = models.CharField(max_length=255, blank=True)   
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere_Programmer, on_delete=models.CASCADE)
    annee = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
    document = models.FileField(upload_to=upload_to_programmes, validators=[FileExtensionValidator(['pdf'])])
    date_upload = models.DateField(auto_now=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.enseignant}'































# class Programmes_Cour(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     verifier=models.BooleanField(default=False)
#     nom=models.CharField(max_length=8,blank=True)   
#     enseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)
#     matiere=models.ForeignKey(Matiere_Programmer,on_delete=models.CASCADE)
#     annee=models.ForeignKey(AnneeAcademique,on_delete=models.CASCADE)
#     document=models.ImageField(upload_to='Img_employer')#upload des fichiers
#     document=models.FileField()
#     date_upload=models.DateField(auto_now=True)
#     # slug = models.SlugField(max_length=200, unique=True, blank=True)
    
#     # def save(self, *args, **kwargs):
#     #     if not self.slug:
#     #         # Génère le slug à partir du titre si vide
#     #         self.slug = slugify(self.)


#     def __str__(self):
#         return f'{self.id} - {self.enseignant}'
    




# class PaiementHonoraire(models.Model):##prends en compte le formateur et Anneeacademique
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     enseignant=models.ForeignKey(Enseignant, on_delete=models.CASCADE)
#     annee_academique=models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE)
#     mois=models.ForeignKey(Mois,on_delete=models.CASCADE)
#     montant=models.IntegerField()
#     # recu=models.ForeignKey(Recu,on_delete=models.CASCADE)
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['enseignant', 'annee_academique', 'mois'],
#                 name='unique_paiement_honoraire_par_mois'
#             )
#         ]


#     def __str__(self):
#         return str(self.id)

    