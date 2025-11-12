from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from .models import Livro, Autor, Emprestimo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
# Importações cruciais para a funcionalidade de leitura e meta
from sgbUsuarios.models import LivroLido, MetaLeitura 
from django.db import IntegrityError 


# VIEWS DE LIVROS
@login_required
def livros (request):
    """
    Lista todos os livros e verifica quais o usuário já leu.
    """
    livros_cadastrados = Livro.objects.all().order_by('titulo')
    autores = Autor.objects.all().order_by('nome')

    livros_lidos_ids = []
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        livros_lidos_ids = LivroLido.objects.filter(
            usuario=request.user
        ).values_list('livro_id', flat=True)

    context = {
        'livros': livros_cadastrados,
        'autores': autores,
        'livros_lidos_ids': set(livros_lidos_ids) 
    }
    return render(request, 'livros.html', context)


def salvar_livro(request):
    if request.method == 'POST':
        titulo_livro = request.POST['titulo_livro']
        autor_livro = request.POST['autor_livro']
        editora = request.POST['editora']
        return render(request, 'livros.html', context={
            'titulo_livro': titulo_livro,
            'autor_livro': autor_livro,
            'editora': editora
        })
    return HttpResponse('Método não permitido', status=405)


def index(request):
    return render(request, 'index.html')

@login_required
def cadastro_livro(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        titulo = request.POST['titulo']
        autor = request.POST['autor']
        ano_publicacao = request.POST['ano_publicacao']
        editora = request.POST['editora']

        if livro_id: # Se o ID do livro for fornecido, atualize o livro existente
            try:
                livro = Livro.objects.get(id=livro_id)
                livro.titulo = titulo
                # Correção: Garante que o autor é criado ou obtido
                autor_obj, created = Autor.objects.get_or_create(nome=autor) 
                livro.autor = autor_obj
                livro.ano_publicacao = ano_publicacao
                livro.editora = editora
                livro.save()
                messages.success(request, f"Livro '{titulo}' atualizado com sucesso!")
            except Livro.DoesNotExist:
                messages.error(request, 'Livro não encontrado para edição.')
        else: 
            autor_obj, created = Autor.objects.get_or_create(nome=autor)
            Livro.objects.create(
                titulo=titulo,
                autor=autor_obj,
                ano_publicacao=ano_publicacao,
                editora=editora
            )
            messages.success(request, f"Livro '{titulo}' cadastrado com sucesso!")

        return redirect('cadastro_livro')

    livros = Livro.objects.all().order_by('titulo')
    autores = Autor.objects.all().order_by('nome')
    return render(request, 'livros.html', {'livros': livros, 'autores': autores})


def exclui_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    livro.delete()
    messages.success(request, f"Livro '{livro.titulo}' excluído com sucesso.")
    return redirect('cadastro_livro')

def edita_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    livros = Livro.objects.all().order_by('titulo') 
    autores = Autor.objects.all().order_by('nome')
    
    if request.method == 'POST':
        livro.titulo = request.POST['titulo']
        autor = request.POST['autor']
        # Correção: Usar get_or_create para evitar duplicação de autor
        autor_obj, created = Autor.objects.get_or_create(nome=autor)
        livro.autor = autor_obj
        livro.ano_publicacao = request.POST['ano_publicacao']
        livro.editora = request.POST['editora']
        livro.save()
        messages.success(request, f"Livro '{livro.titulo}' editado com sucesso.")
        return redirect('cadastro_livro')
        
    return render(request, 'livros.html', {'livros': livros, 'autores': autores, 'livro_editar': livro})


# VIEWS DE AUTORES
def autores(request):
    autores = Autor.objects.all()
    return render(request, 'autor.html', {'autores': autores})

@login_required
def cadastra_autor(request):
    if request.method == 'POST':
        autor_id = request.POST.get('autor_id')
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        data_nascimento = request.POST['data_nascimento']
        nacionalidade = request.POST['nacionalidade']

        if autor_id:
            try:
                autor = Autor.objects.get(id=autor_id)
                autor.nome = nome
                autor.sobrenome = sobrenome
                autor.data_nascimento = data_nascimento
                autor.nacionalidade = nacionalidade
                autor.save()
                messages.success(request, f"Autor(a) '{nome} {sobrenome}' atualizado(a) com sucesso!")
            except Autor.DoesNotExist:
                messages.error(request, 'Autor não encontrado para edição.')
        else:
            Autor.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                data_nascimento=data_nascimento,
                nacionalidade=nacionalidade
            )
            messages.success(request, f"Autor(a) '{nome} {sobrenome}' cadastrado(a) com sucesso!")

        return redirect('autores') # redireciona para a lista de autores

    autores = Autor.objects.all()
    return render(request, 'autor.html', {'autores': autores})

def edita_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)

    if request.method == 'POST':
        autor.nome = request.POST['nome']
        autor.sobrenome = request.POST['sobrenome']
        autor.data_nascimento = request.POST['data_nascimento']
        autor.nacionalidade = request.POST['nacionalidade']