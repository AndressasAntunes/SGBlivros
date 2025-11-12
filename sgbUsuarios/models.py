from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Pega o modelo de Usuário
User = get_user_model() 

# ----------------------------------------------
# MODELO LIVROLIDO (CORRIGIDO: NÍVEL SUPERIOR)
# ----------------------------------------------
class LivroLido(models.Model):
    # Usando settings.AUTH_USER_MODEL ou get_user_model() para FK ao User
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='livros_lidos'
    )
    
    # Referencia o modelo 'Livro' no app 'sgblivros'
    livro = models.ForeignKey(
        'sgblivros.Livro',
        on_delete=models.CASCADE,
        verbose_name='Livro Lido'
    )
    
    data_conclusao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Conclusão'
    )

    class Meta:
        # Garante que um usuário só possa marcar um livro como lido uma vez.
        unique_together = ('usuario', 'livro')
        verbose_name = "Livro Lido"
        verbose_name_plural = "Livros Lidos"

    def __str__(self):
        return f"{self.usuario.username} leu {self.livro.titulo}"

# ----------------------------------------------
# MODELO METALEITURA
# ----------------------------------------------
class MetaLeitura(models.Model):
    # Relaciona a meta a um usuário
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='metas_leitura',
        verbose_name='Usuário'
    )
    
    meta_livros = models.IntegerField(
        verbose_name='Meta de Livros',
        default=1 
    )
    
    # Foi adicionado 'livros_lidos' na view para rastrear o progresso. 
    # Para ser consistente com a view, adicionei o campo aqui.
    livros_lidos = models.IntegerField(
        verbose_name='Contador de Livros Lidos',
        default=0
    )
    
    meta_paginas = models.IntegerField(
        verbose_name='Meta de Páginas',
        default=0,
        blank=True,
        null=True
    )
    
    # O campo ManyToManyField 'livros_completados' não é mais necessário para 
    # rastrear o progresso. A MetaLeitura agora usa o contador 'livros_lidos' 
    # e o progresso é rastreado no modelo 'LivroLido'.
    # Removendo ou comentando a linha abaixo, pois LivroLido já faz o rastreamento.
    
    # livros_completados = models.ManyToManyField( 
    #     'sgblivros.Livro', 
    #     blank=True,
    #     related_name='metas_associadas',
    #     verbose_name='Livros Completados'
    # )
    
    data_inicio = models.DateField(
        auto_now_add=True, 
        verbose_name='Data de Início'
    )
    
    data_fim = models.DateField(
        verbose_name='Data Final Prevista'
    )
    
    STATUS_CHOICES = (
        ('ATIVA', 'Ativa'),
        ('CONCLUIDA', 'Concluída'),
        ('EXPIRADA', 'Expirada'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ATIVA',
        verbose_name='Status'
    )

    class Meta:
        verbose_name = 'Meta de Leitura'
        verbose_name_plural = 'Metas de Leitura'
        ordering = ['-data_inicio']

    def __str__(self):
        return f"Meta de {self.usuario.username}: {self.meta_livros} Livros"