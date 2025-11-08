from django.db import models
from django.conf import settings

# Create your models here.
# trabalhamos com classes aqui 
# define o banco de dados - modela o banco de dados 

#chave estrangeira 
class Autor (models.Model):
    nome = models.CharField (max_length=150)
    sobrenome = models.CharField (max_length=500)
    data_nascimento = models.DateField (blank=True, null=True)
    nacionalidade = models.CharField (max_length=80, blank=True, null=True)

    '''
    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
        '''

#chave primaria
class Livro(models.Model): #models.model indica que a classe Livro é um modelo do Django é padrão
    titulo = models.CharField(max_length=200) #CharField é um campo de texto com tamanho máximo definido
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros') #ForeignKey cria uma relação muitos-para-um com o modelo Autor
    ano_publicacao = models.PositiveIntegerField()
    editora = models.CharField(max_length=100, blank=True, null=True) #blank e null permitem que o campo seja opcional

    #Arquivo Digital (PDF/EPUB)
    arquivo_digital = models.FileField(
        upload_to='ebooks/', 
        blank=True, 
        null=True, 
        help_text="Opcional: Arquivo PDF ou EPUB para leitura virtual."
    )

    # indicar se o livro tem uma cópia digital
    tem_ebook = models.BooleanField(
        default=False, 
        help_text="Indica se existe um arquivo digital (eBook) associado a este livro."
    )
    

    def __str__(self):
        return self.titulo


# controlar empréstimos (físicos ou virtuais)
class Emprestimo(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='emprestimos'
    )
    
    livro = models.ForeignKey(
        Livro, 
        on_delete=models.CASCADE, 
        related_name='emprestimos'
    )
    
    data_emprestimo = models.DateField(auto_now_add=True)
    data_prevista_devolucao = models.DateField()
    data_devolucao_real = models.DateField(blank=True, null=True)
    
    # chave para controlar o acesso ao eBook
    ativo = models.BooleanField(default=True) 

    def __str__(self):
        status = "Ativo" if self.ativo else "Devolvido"
        return f"Empréstimo de '{self.livro.titulo}' para {self.usuario.username} - ({status})"
    
# Create your models here.

