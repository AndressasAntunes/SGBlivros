from django.contrib import admin
from .models import Autor, Livro, Emprestimo 

# Registra o modelo Autor
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'nacionalidade')
    search_fields = ('nome', 'sobrenome')

# Registra o modelo Livro
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'ano_publicacao', 'tem_ebook')
    list_filter = ('tem_ebook', 'ano_publicacao')
    search_fields = ('titulo', 'autor__nome')
    # Adicione o campo arquivo_digital e tem_ebook aqui
    fields = ('titulo', 'autor', 'ano_publicacao', 'editora', 'arquivo_digital', 'tem_ebook')

# Registra o modelo Emprestimo (útil para verificar o acesso)
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'data_emprestimo', 'data_prevista_devolucao', 'ativo')
    list_filter = ('ativo', 'data_prevista_devolucao')
    search_fields = ('livro__titulo', 'usuario__username')