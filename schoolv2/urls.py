from django.contrib import admin 
from unfold.admin import ModelAdmin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import handler404

# # Assignez votre handler personnalisé
# handler404 = 'pages.views.handler404'

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("pages.urls")),
    path('', include("transactions.urls")),
    path('', include("api.urls")),
    path('', include("notes.urls")),
    path('', include("utilisateur.urls")),
    path('', include("pdf.urls")),
]

# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files only in development
# In production, static files should be served by the web server (nginx/Apache), not Django

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
