# import pdfkit
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.conf import settings

# def impression(element,):



#     # Préparer le contexte
#     context = {
#         'element': element,
#     }
    
#     try:
#         # Rendre le template HTML
#         html_string = render_to_string('pages/pdf/scolarite.html', context)
        
#         # Configurer pdfkit
#         config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
        
#         # Générer le PDF
#         pdf = pdfkit.from_string(
#             html_string, 
#             False,  # Ne pas sauvegarder dans un fichier
#             options=settings.PDF_DEFAULT_OPTIONS,
#             configuration=config
#         )
        
#         # Créer la réponse HTTP
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="ecolage_{ecolage.etudiant.utilisateur.nom}{ecolage.etudiant.utilisateur.prenom}_{ecolage.mois.nom}_{ecolage.annee_academique.annee}.pdf"'
        
#         return response
        
#     except Exception as e:
#         # Gestion des erreurs
#         return HttpResponse(f"Erreur lors de la génération du PDF: {str(e)}")
