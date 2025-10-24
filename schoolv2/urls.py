from django.contrib import admin 
from unfold.admin import ModelAdmin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import handler404

# # Assignez votre handler personnalisé
# handler404 = 'pages.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("pages.urls")),
    path('', include("transactions.urls")),
    path('', include("api.urls")),
    path('', include("notes.urls")),
    path('', include("utilisateur.urls")),
    path('', include("pdf.urls")),





]
urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
