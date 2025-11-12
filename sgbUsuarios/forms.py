# Arquivo: sgbUsuarios/forms.py
from django import forms
from .models import MetaLeitura

class MetaLeituraForm(forms.ModelForm):
    class Meta:
        model = MetaLeitura
        # Campos que o usuário irá preencher no formulário
        fields = ['meta_livros', 'meta_paginas', 'data_fim']
        
        widgets = {
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'meta_livros': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'meta_paginas': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Opcional'}),
        }

        labels = {
            'meta_livros': 'Meta (Quantos livros)',
            'meta_paginas': 'Meta (Total de páginas)',
            'data_fim': 'Prazo Final',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # remove o campo usuario (será preenchido automaticamente)
        if 'usuario' in self.fields:
            del self.fields['usuario']
        # remove o campo status (será definido como ATIVA por padrão)
        if 'status' in self.fields:
            del self.fields['status']