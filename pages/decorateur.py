# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from .models import Utilisateur

# # Décorateurs personnalisés
# def admin(view_func):
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated or request.user.role != Utilisateur.Role.ADMIN:
#             return HttpResponseForbidden("Accès réservé aux administrateurs")
#         return view_func(request, *args, **kwargs)
#     return wrapper

# def etudiant(view_func):
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated or request.user.role != Utilisateur.Role.ETUDIANT:
#             return HttpResponseForbidden("Accès réservé aux étudiants")
#         return view_func(request, *args, **kwargs)
#     return wrapper

# def prof(view_func):
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated or request.user.role != Utilisateur.Role.ENSEIGNANT:
#             return HttpResponseForbidden("Accès réservé aux enseignants")
#         return view_func(request, *args, **kwargs)
#     return wrapper

# # Vues
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             if user.role == Utilisateur.Role.ADMIN:
#                 return redirect('admin_dashboard')
#             elif user.role == Utilisateur.Role.ETUDIANT:
#                 return redirect('student_dashboard')
#             elif user.role == Utilisateur.Role.ENSEIGNANT:
#                 return redirect('teacher_dashboard')
#         else:
#             return render(request, 'login.html', {'error': 'Identifiants incorrects'})
    
#     return render(request, 'login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# @login_required
# @admin
# def admin_dashboard(request):
#     return render(request, 'dashboard.html', {
#         'user_type': 'Administrateur',
#         'content': 'Espace réservé aux administrateurs'
#     })

# @login_required
# @etudiant
# def etudiant_dashboard(request):
#     profile = request.user.utilisateur  # Accès au profil étudiant
#     return render(request, 'dashboard.html', {
#         'user_type': 'Étudiant',
#         'content': f'Bienvenue {profile.nom} {profile.prenom}',
#         'profile': profile
#     })

# @login_required
# @prof
# def prof_dashboard(request):
#     profile = request.user.enseignant_utilisateur  # Accès au profil enseignant
#     return render(request, 'dashboard.html', {
#         'user_type': 'Enseignant',
#         'content': f'Bienvenue Professeur {profile.nom}',
#         'profile': profile
#     })















# <!DOCTYPE html>
# <html>
# <head>
#     <title>Connexion</title>
# </head>
# <body>
#     <h1>Connexion</h1>
#     {% if error %}
#     <p style="color: red;">{{ error }}</p>
#     {% endif %}
#     <form method="post">
#         {% csrf_token %}
#         <input type="text" name="username" placeholder="Nom d'utilisateur" required><br>
#         <input type="password" name="password" placeholder="Mot de passe" required><br>
#         <button type="submit">Se connecter</button>
#     </form>
# </body>
# </html>




# <!DOCTYPE html> 
# <html>
# <head>
#     <title>Tableau de bord {{ user_type }}</title>
# </head>
# <body>
#     <h1>Tableau de bord {{ user_type }}</h1>
#     <p>{{ content }}</p>
    
#     {% if profile %}
#     <div>
#         <h3>Vos informations :</h3>
#         <p>Nom complet: {{ profile.nom }} {{ profile.prenom }}</p>
#         <p>Matricule: {{ profile.matricule }}</p>
#     </div>
#     {% endif %}
    
#     <a href="{% url 'logout' %}">Déconnexion</a>
# </body>
# </html>