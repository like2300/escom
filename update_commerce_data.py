#!/usr/bin/env python
"""
Script pour supprimer toutes les données des tables Filière, Option et Classe,
puis ajouter de nouvelles données liées spécifiquement au commerce.
"""

import os
import sys
import django

# Configurer Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolv2.settings')
django.setup()

from transactions.models import Filiere, Option, Classe, Cycle, Niveau


def update_commerce_data():
    print(\"Suppression des données existantes...\")
    
    # Supprimer toutes les classes en premier (en raison des clés étrangères)
    Classe.objects.all().delete()
    print(\"Classes supprimées\")
    
    # Supprimer toutes les options
    Option.objects.all().delete()
    print(\"Options supprimées\")
    
    # Supprimer toutes les filières
    Filiere.objects.all().delete()
    print(\"Filières supprimées\")
    
    print(\"\nCréation des nouvelles données liées au commerce...\")
    
    # Créer les cycles nécessaires s'ils n'existent pas
    cycle1, created = Cycle.objects.get_or_create(
        libelle=\"Cycle1\",
        description=\"Licence - Bac+3\",
        defaults={'libelle': \"Cycle1\", 'description': \"Licence - Bac+3\"}
    )
    
    cycle2, created = Cycle.objects.get_or_create(
        libelle=\"Cycle2\",
        description=\"Master - Bac+5\",
        defaults={'libelle': \"Cycle2\", 'description': \"Master - Bac+5\"}
    )
    
    # Créer les niveaux nécessaires s'ils n'existent pas
    l1, created = Niveau.objects.get_or_create(
        libelle=\"L1\",
        description=\"Licence 1 - Bac+1\",
        defaults={'libelle': \"L1\", 'description': \"Licence 1 - Bac+1\"}
    )
    
    l2, created = Niveau.objects.get_or_create(
        libelle=\"L2\",
        description=\"Licence 2 - Bac+2\",
        defaults={'libelle': \"L2\", 'description': \"Licence 2 - Bac+2\"}
    )
    
    l3, created = Niveau.objects.get_or_create(
        libelle=\"L3\",
        description=\"Licence 3 - Bac+3\",
        defaults={'libelle': \"L3\", 'description': \"Licence 3 - Bac+3\"}
    )
    
    m1, created = Niveau.objects.get_or_create(
        libelle=\"M1\",
        description=\"Master 1 - Bac+4\",
        defaults={'libelle': \"M1\", 'description': \"Master 1 - Bac+4\"}
    )
    
    m2, created = Niveau.objects.get_or_create(
        libelle=\"M2\",
        description=\"Master 2 - Bac+5\",
        defaults={'libelle': \"M2\", 'description': \"Master 2 - Bac+5\"}
    )
    
    # Créer la filière Commerce
    filiere_commerce, created = Filiere.objects.get_or_create(
        libelle=\"Commerce\",
        description=\"Filière dédiée aux études commerciales et de gestion\"
    )
    
    # Créer différentes options liées au commerce
    option_commerce_international, created = Option.objects.get_or_create(
        libelle=\"Commerce International\",
        filiere=filiere_commerce,
        description=\"Spécialisation dans le commerce international et les échanges transfrontaliers\"
    )
    
    option_marketing, created = Option.objects.get_or_create(
        libelle=\"Marketing\",
        filiere=filiere_commerce,
        description=\"Spécialisation dans les stratégies de marketing et de communication\"
    )
    
    option_gestion_commerciale, created = Option.objects.get_or_create(
        libelle=\"Gestion Commerciale\",
        filiere=filiere_commerce,
        description=\"Spécialisation dans la gestion commerciale et les ventes\"
    )
    
    option_finance, created = Option.objects.get_or_create(
        libelle=\"Finance\",
        filiere=filiere_commerce,
        description=\"Spécialisation dans la finance et les marchés financiers\"
    )
    
    # Créer des classes pour chaque option et niveau
    classes_data = [
        # L1
        {
            'nom': 'CI-L1',
            'cycle': cycle1,
            'niveau': l1,
            'option': option_commerce_international,
            'description': 'Classe de Commerce International - Licence 1'
        },
        {
            'nom': 'MARK-L1',
            'cycle': cycle1,
            'niveau': l1,
            'option': option_marketing,
            'description': 'Classe de Marketing - Licence 1'
        },
        {
            'nom': 'GC-L1',
            'cycle': cycle1,
            'niveau': l1,
            'option': option_gestion_commerciale,
            'description': 'Classe de Gestion Commerciale - Licence 1'
        },
        {
            'nom': 'FIN-L1',
            'cycle': cycle1,
            'niveau': l1,
            'option': option_finance,
            'description': 'Classe de Finance - Licence 1'
        },
        # L2
        {
            'nom': 'CI-L2',
            'cycle': cycle1,
            'niveau': l2,
            'option': option_commerce_international,
            'description': 'Classe de Commerce International - Licence 2'
        },
        {
            'nom': 'MARK-L2',
            'cycle': cycle1,
            'niveau': l2,
            'option': option_marketing,
            'description': 'Classe de Marketing - Licence 2'
        },
        {
            'nom': 'GC-L2',
            'cycle': cycle1,
            'niveau': l2,
            'option': option_gestion_commerciale,
            'description': 'Classe de Gestion Commerciale - Licence 2'
        },
        {
            'nom': 'FIN-L2',
            'cycle': cycle1,
            'niveau': l2,
            'option': option_finance,
            'description': 'Classe de Finance - Licence 2'
        },
        # L3
        {
            'nom': 'CI-L3',
            'cycle': cycle1,
            'niveau': l3,
            'option': option_commerce_international,
            'description': 'Classe de Commerce International - Licence 3'
        },
        {
            'nom': 'MARK-L3',
            'cycle': cycle1,
            'niveau': l3,
            'option': option_marketing,
            'description': 'Classe de Marketing - Licence 3'
        },
        {
            'nom': 'GC-L3',
            'cycle': cycle1,
            'niveau': l3,
            'option': option_gestion_commerciale,
            'description': 'Classe de Gestion Commerciale - Licence 3'
        },
        {
            'nom': 'FIN-L3',
            'cycle': cycle1,
            'niveau': l3,
            'option': option_finance,
            'description': 'Classe de Finance - Licence 3'
        },
        # M1
        {
            'nom': 'CI-M1',
            'cycle': cycle2,
            'niveau': m1,
            'option': option_commerce_international,
            'description': 'Classe de Commerce International - Master 1'
        },
        {
            'nom': 'MARK-M1',
            'cycle': cycle2,
            'niveau': m1,
            'option': option_marketing,
            'description': 'Classe de Marketing - Master 1'
        },
        {
            'nom': 'GC-M1',
            'cycle': cycle2,
            'niveau': m1,
            'option': option_gestion_commerciale,
            'description': 'Classe de Gestion Commerciale - Master 1'
        },
        {
            'nom': 'FIN-M1',
            'cycle': cycle2,
            'niveau': m1,
            'option': option_finance,
            'description': 'Classe de Finance - Master 1'
        },
        # M2
        {
            'nom': 'CI-M2',
            'cycle': cycle2,
            'niveau': m2,
            'option': option_commerce_international,
            'description': 'Classe de Commerce International - Master 2'
        },
        {
            'nom': 'MARK-M2',
            'cycle': cycle2,
            'niveau': m2,
            'option': option_marketing,
            'description': 'Classe de Marketing - Master 2'
        },
        {
            'nom': 'GC-M2',
            'cycle': cycle2,
            'niveau': m2,
            'option': option_gestion_commerciale,
            'description': 'Classe de Gestion Commerciale - Master 2'
        },
        {
            'nom': 'FIN-M2',
            'cycle': cycle2,
            'niveau': m2,
            'option': option_finance,
            'description': 'Classe de Finance - Master 2'
        },
    ]
    
    # Créer les classes
    for classe_data in classes_data:
        Classe.objects.get_or_create(
            nom=classe_data['nom'],
            cycle=classe_data['cycle'],
            niveau=classe_data['niveau'],
            option=classe_data['option'],
            description=classe_data['description']
        )
    
    print(f\"\\n{Filiere.objects.count()} filière créée (Commerce)\")
    print(f\"{Option.objects.count()} options créées dans la filière Commerce\")
    print(f\"{Classe.objects.count()} classes créées dans la filière Commerce\")
    
    print(\"\\nDonnées mises à jour avec succès !\")


if __name__ == \"__main__\":
    update_commerce_data()