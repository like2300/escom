from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.utils.text import slugify
# import datetime


#--------------------------------------------- utilisateurs compris dans le site -----------------------------------#
class Utilisateur(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN","Admin"
        ETUDIANT = "ETUDIANT", "Etudiant" 
        ENSEINGNANT = "ENSEIGNANT", "Enseignant"

    base_role = Role.ADMIN


    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            if not self.password:
                self.set_password("escom@2025")
            return super().save(*args, **kwargs)
        
#Etudiant

class EtudiantManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Utilisateur.Role.ETUDIANT)


class Etudiant(Utilisateur):

    base_role = Utilisateur.Role.ETUDIANT

    student = EtudiantManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Pour les etudiants"
    
    # def __str__(self):
    #     return self.nom


@receiver(post_save, sender=Etudiant)
def create_etu_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ETUDIANT":
        EtudiantProfile.objects.create(utilisateur=instance)


class EtudiantProfile(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE,related_name='utilisateur')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    autres_prenom = models.CharField(max_length=255, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    nationalite = models.CharField(max_length=100, null=True, blank=True)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)
    matricule = models.CharField(max_length=255, null=True)
    cree_par = models.CharField(max_length=1000)


    def __str__(self):
        return self.utilisateur.username



#Enseignant


class EnseignantManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Utilisateur.Role.ENSEINGNANT)


class Enseignant(Utilisateur):

    base_role = Utilisateur.Role.ENSEINGNANT

    prof = EnseignantManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Pour les enseignants"
    
    # def __str__(self):
    #     return self.nom


@receiver(post_save, sender=Enseignant)
def create_prof_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ENSEIGNANT":
        EnseignantProfile.objects.create(utilisateur=instance)


class EnseignantProfile(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE,related_name='enseignant_utilisateur')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    autres_prenom = models.CharField(max_length=255, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    nationalite = models.CharField(max_length=100, null=True, blank=True)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)
    matricule = models.CharField(max_length=255, null=True)
    cree_par = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            # Génère le slug à partir du titre si vide
            self.slug = slugify(f'{self.nom}-{self.prenom}')
    
        super().save(*args, **kwargs)


    def __str__(self):
        return self.utilisateur.username

