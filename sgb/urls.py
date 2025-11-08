
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sgblivros.urls')), 
    # path('livros/', include('sgblivros.urls')), 
    path('auth/', include('sgbUsuarios.urls')),
    path('accounts/', include('allauth.urls')),
    
   
]


# =========================================================
# 🖼️ CONFIGURAÇÃO DE MÍDIA (APENAS EM AMBIENTE DE DESENVOLVIMENTO)
# ESSENCIAL PARA VISUALIZAR OS EBOOKS (FileField)
# =========================================================
if settings.DEBUG:
    # Esta linha serve os arquivos da pasta MEDIA (onde os eBooks estão salvos)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)