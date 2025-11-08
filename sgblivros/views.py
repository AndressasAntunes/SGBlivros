from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from .models import Livro, Autor, Emprestimo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
# Create your views here.


# ALTERAÇÃO PRINCIPAL: Esta função agora busca os livros e os passa para o template.
def livros (request):
    # O primeiro 'return' impedia a busca dos dados.
    livros_cadastrados = Livro.objects.all().order_by('titulo')
    autores = Autor.objects.all().order_by('nome')
    context = {
        'livros': livros_cadastrados,
        'autores': autores
    }
    return render(request, 'livros.html', context)
    # A segunda parte do código original era inatingível.


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

#adicionar uma notação para proteger essa função só se tiver logado no sistema 
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



# AUTORES


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
        autor.save()
        messages.success(request, f"Autor(a) '{autor.nome} {autor.sobrenome}' editado(a) com sucesso!")
        return redirect('autores')

    autores = Autor.objects.all()
    return render(request, 'autor.html', {'autor_editar': autor, 'autores': autores})

def exclui_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    autor.delete()
    messages.success(request, f"Autor(a) '{autor.nome} {autor.sobrenome}' excluído(a) com sucesso.")
    return redirect('autores')

# ===============================================
# FUNÇÕES DE LIVROS VIRTUAIS (PDF) E EMPRÉSTIMOS
# ===============================================

@login_required 
def iniciar_emprestimo_ebook(request, livro_id):
    
    livro = get_object_or_404(Livro, pk=livro_id)

    # 1. Checa se o livro tem mídia digital
    if not livro.tem_ebook or not livro.arquivo_digital:
        messages.error(request, 'Este livro não possui uma cópia digital disponível para empréstimo.')
        return redirect('detalhes_livro', livro_id=livro_id) 

    # 2. Verifica se o usuário já possui um empréstimo ATIVO para este livro
    emprestimo_existente = Emprestimo.objects.filter(
        usuario=request.user, 
        livro=livro, 
        ativo=True
    ).exists()

    if emprestimo_existente:
        messages.warning(request, f'Você já possui um empréstimo ativo para "{livro.titulo}".')
    else:
        # 3. Define a data de devolução (7 dias)
        data_devolucao = date.today() + timedelta(days=7)
        
        # 4. Cria o novo registro de Empréstimo
        Emprestimo.objects.create(
            usuario=request.user,
            livro=livro,
            data_prevista_devolucao=data_devolucao,
            ativo=True
        )
        messages.success(request, f'Empréstimo virtual de "{livro.titulo}" realizado com sucesso! Você tem acesso até {data_devolucao.strftime("%d/%m/%Y")}.')

    # Após iniciar ou confirmar que já tem, redireciona para a View de leitura
    return redirect('ler_ebook', livro_id=livro.pk)


@login_required
def ler_ebook(request, livro_id):
  
    livro = get_object_or_404(Livro, pk=livro_id)
    
    # 1. Verifica se o usuário tem um empréstimo ATIVO
    tem_acesso = Emprestimo.objects.filter(
        usuario=request.user, 
        livro=livro, 
        ativo=True
    ).exists()

    if not tem_acesso:
        messages.error(request, 'Você não tem um empréstimo ativo para este livro.')
        return redirect('detalhes_livro', livro_id=livro_id) 

    if livro.arquivo_digital:
        
        try:
            # Tenta abrir o arquivo e servi-lo
            return FileResponse(livro.arquivo_digital.open(), content_type='application/pdf') 
        except FileNotFoundError:
            raise Http404("Arquivo digital não encontrado no servidor.")
    else:
        messages.error(request, 'Arquivo digital não está disponível no momento.')
        return redirect('detalhes_livro', livro_id=livro_id) 


@login_required
def devolver_livro(request, emprestimo_id):
    """
    Marca um empréstimo como devolvido.
    """
    # 1. Busca o empréstimo ativo pertencente ao usuário
    emprestimo = get_object_or_404(
        Emprestimo, 
        pk=emprestimo_id, 
        usuario=request.user, 
        ativo=True 
    )

    if request.method == 'POST':
        # 2. Finaliza o empréstimo
        emprestimo.ativo = False
        emprestimo.data_devolucao_real = date.today()
        emprestimo.save()
        
        messages.success(request, f'O livro "{emprestimo.livro.titulo}" Livro devolvido com sucesso! Seu acesso virtual foi encerrado.')
        
        # Redireciona para o dashboard do usuário ou lista de empréstimos
        # Mantenho 'livros', mas 'cadastro_livro' é o nome mais seguro visto nas URLs.
        return redirect('livros') 

    # Se não for POST (pedindo confirmação)
    return render(request, 'sgblivros/confirmar_devolucao.html', {'emprestimo': emprestimo})

def detalhes_livro(request, livro_id):
    """
    Exibe os detalhes de um livro e verifica o status do empréstimo para botões de ação.
    """
    livro = get_object_or_404(Livro, pk=livro_id)
    
    tem_acesso = False
    emprestimo_ativo = None
    
    if request.user.is_authenticated:
        # Tenta encontrar um empréstimo ativo do usuário para este livro
        try:
            emprestimo_ativo = Emprestimo.objects.get(
                usuario=request.user, 
                livro=livro, 
                ativo=True
            )
            tem_acesso = True
        except Emprestimo.DoesNotExist:
            tem_acesso = False
    
    context = {
        'livro': livro,
        'tem_acesso': tem_acesso,
        'emprestimo_ativo': emprestimo_ativo, 
    }
    return render(request, 'sgblivros/detalhes_livro.html', context)