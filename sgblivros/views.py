from django.urls import path
from . import views

urlpatterns = [
   
    # AUTORES
    path('autores/', views.autores, name='autores'),
    path('cadastra_autor/', views.cadastra_autor, name='cadastra_autor'),
    path('excluir_autor/<int:autor_id>/', views.exclui_autor, name='exclui_autor'),
    path('editar_autor/<int:autor_id>/', views.edita_autor, name='edita_autor'),
    
   
    path('marcar-lido/<int:livro_id>/', views.marcar_livro_lido, name='marcar_livro_lido'),
    
    
    # ==================================================
    # 📚 NOVAS ROTAS DE EBOOK (DETALHES, EMPRÉSTIMO, LEITURA)
    # ==================================================
    
    # 1. Detalhes do Livro: Exibe informações e botões de ação (Emprestar/Ler)
    # Rota: /livro/123/
    path('livro/<int:livro_id>/', views.detalhes_livro, name='detalhes_livro'),
    
    # 2. Iniciar Empréstimo: Processa a criação do registro de Empréstimo
    # Rota: /livro/123/emprestar/
    path('livro/<int:livro_id>/emprestar/', views.iniciar_emprestimo_ebook, name='iniciar_emprestimo_ebook'),
    
    # 3. Leitura do Ebook: Serve o arquivo PDF/EPUB (Acesso protegido)
    # Rota: /livro/123/ler/
    path('livro/<int:livro_id>/ler/', views.ler_ebook, name='ler_ebook'),
    
    # 4. Devolução:
]