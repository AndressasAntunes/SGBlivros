# Arquivo: sgbUsuarios/views.py

from django.shortcuts import render, redirect, get_object_or_404 # Adicionado get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from sgblivros.models import Livro # Já importado
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import MetaLeituraForm 
from .models import MetaLeitura, LivroLido 
from django.utils import timezone 
from datetime import datetime, timedelta
import pyotp



from .utils import send_otp
from datetime import datetime, timedelta
import pyotp

import re

def cadastra_usuario(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        nome_usuario = request.POST.get('nome_usuario', '').strip()
        nome = request.POST.get('nome', '').strip()
        sobrenome = request.POST.get('sobrenome', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        # Verificação de campos obrigatórios
        if not nome or not sobrenome or not nome_usuario or not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('cadastro')

        # Verificação de formato de e-mail
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request, 'E-mail em formato inválido.')
            return redirect('cadastro')

        # Verificação de senha com no mínimo 8 caracteres
        if len(senha) < 8:
            messages.error(request, 'A senha deve ter no mínimo 8 caracteres.')
            return redirect('cadastro')

        # Verificação de nome de usuário já existente
        if User.objects.filter(username=nome_usuario).exists():
            messages.error(request, 'Nome de usuário já está em uso.')
            return redirect('cadastro')

        # Criação do usuário
        usuario = User.objects.create_user(
            username=nome_usuario,
            first_name=nome,
            last_name=sobrenome,
            email=email,
            password=senha
        )
        usuario.save()

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('cadastro')



def loga_usuario(request):
    """View de login com suporte a 2FA"""
    error_message = None

    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        usuario = authenticate(request, username=username, password=senha)

        if usuario is not None:
            # Envia código OTP para o email do usuário
            send_otp(request, usuario)


            # Salva nome de usuário na sessão
            request.session['nome_usuario'] = username

            # Redireciona para a página de verificação do OTP
            return redirect('otp')
        else:
            error_message = 'Usuário ou senha incorretos.'

    # Renderiza o formulário de login (GET ou erro)
    return render(request, 'login.html', {'error_message': error_message})


def otp_view(request):
    error_message = None

    if request.method == 'POST':
        otp = request.POST.get('otp')
        username = request.session.get('nome_usuario')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_until:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if datetime.now() < valid_until:
                totp = pyotp.TOTP(otp_secret_key, interval=300)
                if totp.verify(otp):
                    usuario = User.objects.filter(username=username).first()
                    if usuario:
                        usuario.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, usuario)

                        # Limpa a sessão
                        request.session.pop('otp_secret_key', None)
                        request.session.pop('otp_valid_date', None)
                        request.session.pop('nome_usuario', None)

                        return redirect('cadastro_livro')
                    else:
                        error_message = 'Usuário não encontrado.'
                else:
                    error_message = 'Código inválido. Tente novamente.'
            else:
                error_message = 'O código expirou. Solicite um novo login.'
        else:
            error_message = 'Sessão inválida. Tente novamente.'

    return render(request, 'otp.html', {'error_message': error_message})



def logout_usuario(request):
    logout(request)
    return render (request, 'login.html')


# Redefinir a senha - enviar email com link
def ForgetPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            usuario = User.objects.get(email=email)
            
            # Gera token seguro
            token = default_token_generator.make_token(usuario)
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            
            # Cria o link de redefinição
            reset_link = f"http://127.0.0.1:8000/auth/NewPasswordPage/{uid}/{token}/"
            
            # Envia email
            send_mail(
                'Redefinição de senha - SGLivros',
                f"Olá, {usuario.username}!\n\n"
                f"Você solicitou a redefinição de senha.\n\n"
                f"Clique no link abaixo para redefinir sua senha:\n"
                f"{reset_link}\n\n"
                f"Este link expira em 24 horas.\n\n"
                f"Se você não solicitou esta redefinição, ignore este email.",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            
            messages.success(request, 'Email enviado com sucesso! Verifique sua caixa de entrada.')
            return render(request, 'EmailEnviado.html', {
                'mensagem_sucesso': 'Um link de redefinição foi enviado para seu email.'
            })
            
        except User.DoesNotExist:
            # Por segurança, não revela se o email existe ou não
            messages.info(request, 'Se este email estiver cadastrado, você receberá um link de redefinição.')
            return render(request, 'EmailEnviado.html', {
                'mensagem_sucesso': 'Se o email estiver cadastrado, você receberá as instruções.'
            })
    
    return render(request, 'forget_password.html')


def NewPasswordPage(request, uidb64, token):
    """View para redefinir senha com token de segurança"""
    try:
        # Decodifica o ID do usuário
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usuario = None
    
    # Verifica se o usuário existe e se o token/senha é válido
    if usuario is not None and default_token_generator.check_token(usuario, token):
        if request.method == "POST":
            nova_senha = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')
            
            if not nova_senha or not confirmar_senha:
                messages.error(request, 'Preencha todos os campos!')
                return render(request, 'NewPassword.html', {'validlink': True, 'usuario': usuario})
            
            if nova_senha == confirmar_senha:
                if len(nova_senha) < 6:
                    messages.error(request, 'A senha deve ter no mínimo 6 caracteres!')
                    return render(request, 'NewPassword.html', {'validlink': True, 'usuario': usuario})
                
                usuario.set_password(nova_senha)
                usuario.save()
                messages.success(request, 'Senha redefinida com sucesso! Faça login com sua nova senha.')
                return redirect('login')
            else:
                messages.error(request, 'As senhas não coincidem!')
                return render(request, 'NewPassword.html', {'validlink': True, 'usuario': usuario})
        
        # GET request - mostra formulário
        return render(request, 'NewPassword.html', {'validlink': True, 'usuario': usuario})
    else:
        # Token inválido ou expirado
        messages.error(request, 'Link inválido ou expirado! Solicite um novo link de redefinição.')
        return render(request, 'NewPassword.html', {'validlink': False})


@login_required(login_url='/auth/login/')
def cadastrar_meta(request):
    # Verifica se o usuário já tem uma meta ATIVA
    meta_ativa = MetaLeitura.objects.filter(usuario=request.user, status='ATIVA').exists()
    
    if meta_ativa:
        messages.warning(request, "Você já possui uma meta de leitura ativa. Finalize a atual para criar uma nova.")
        # Redireciona para o painel ou lista de metas 
        return redirect('minhas_metas') 

    if request.method == 'POST':
        form = MetaLeituraForm(request.POST)
        if form.is_valid():
            # Não salva no banco ainda (commit=False)
            meta = form.save(commit=False) 
            # Define o usuário da meta como o usuário logado
            meta.usuario = request.user 
            # Salva no banco de dados
            meta.save() 
            messages.success(request, "Meta de leitura cadastrada com sucesso!")
            # Redireciona para a listagem de metas
            return redirect('minhas_metas') 
    else:
        # Se for um GET request, exibe um formulário vazio
        form = MetaLeituraForm()

    context = {
        'form': form,
        'meta_ativa': meta_ativa
    }
    
    # Renderiza o template de cadastro
    return render(request, 'sgbUsuarios/cadastrar_meta.html', context)

@login_required(login_url='/auth/login/')
def minhas_metas(request):
    """View para listar todas as metas de leitura do usuário logado."""
    
    # Obtém todas as metas de leitura para o usuário logado, ordenadas pela mais recente
    metas = MetaLeitura.objects.filter(usuario=request.user).order_by('-data_inicio')
    
    context = {
        'metas': metas,
    }
    
    # Renderiza o template de listagem
    return render(request, 'sgbUsuarios/minhas_metas.html', context)

@login_required
def marcar_livro_lido(request, livro_id):
    """
    Marca um livro como lido pelo usuário e atualiza a Meta de Leitura ativa.
    """
    # 1. Deve ser uma requisição POST (clique no botão do formulário)
    if request.method == 'POST':
        livro = get_object_or_404(Livro, pk=livro_id)

        # 2. Checa se já está lido
        if LivroLido.objects.filter(usuario=request.user, livro=livro).exists():
            messages.warning(request, f'O livro "{livro.titulo}" já está marcado como lido.')
            # Redireciona para a lista de livros (nome da URL que lista os livros)
            return redirect('livros')
        
        # 3. Cria o registro de livro lido
        LivroLido.objects.create(
            usuario=request.user,
            livro=livro,
            data_conclusao=timezone.now().date() # Salva apenas a data
        )
        
        # 4. Tenta atualizar a meta de leitura ativa
        try:
            # Busca a meta ATIVA mais recente do usuário
            meta_ativa = MetaLeitura.objects.filter(
                usuario=request.user, 
                status='ATIVA'
            ).order_by('-data_inicio').first()
            
            if meta_ativa:
                # Incrementa o contador de livros lidos
                meta_ativa.livros_lidos = (meta_ativa.livros_lidos or 0) + 1
                
                # Checa se a meta foi atingida
                if meta_ativa.livros_lidos >= meta_ativa.meta_livros:
                    meta_ativa.status = 'CONCLUIDA' # Altera o status
                    messages.success(request, f'Parabéns! Você concluiu sua meta de {meta_ativa.meta_livros} livros!')
                
                meta_ativa.save()

        except Exception as e:
            # Em caso de erro, apenas loga e deixa o livro marcado
            print(f"Erro ao tentar atualizar meta de leitura: {e}")
            
        messages.success(request, f'O livro "{livro.titulo}" foi marcado como lido.')
        
    # Retorna para a lista de livros
    return redirect('livros')