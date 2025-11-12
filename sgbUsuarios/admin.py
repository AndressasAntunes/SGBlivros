from django.contrib import admin
from .models import MetaLeitura # Importa seu novo modelo

# Registra o novo modelo
admin.site.register(MetaLeitura)
