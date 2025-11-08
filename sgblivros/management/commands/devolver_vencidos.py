from django.core.management.base import BaseCommand
from datetime import date
from sgblivros.models import Emprestimo 

class Command(BaseCommand):
    help = 'Verifica e marca automaticamente como devolvidos os empréstimos virtuais vencidos.'

    def handle(self, *args, **options):
        # 1. Obter a data de hoje
        hoje = date.today()
        
        # 2. Filtrar empréstimos vencidos e ativos
        emprestimos_vencidos = Emprestimo.objects.filter(
            ativo=True,
            data_prevista_devolucao__lte=hoje # (menor ou igual a)
        )

        if not emprestimos_vencidos.exists():
            self.stdout.write(self.style.SUCCESS('Nenhum empréstimo vencido encontrado para devolução automática.'))
            return

        count = 0
        for emprestimo in emprestimos_vencidos:
            # 3. Realizar a devolução
            emprestimo.ativo = False
            
            # Garante que a data de devolução seja preenchida (usamos a data de vencimento)
            if emprestimo.data_devolucao_real is None:
                emprestimo.data_devolucao_real = emprestimo.data_prevista_devolucao
                
            emprestimo.save()
            count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Devolvido: "{emprestimo.livro.titulo}" de {emprestimo.usuario.username}. Vencimento: {emprestimo.data_prevista_devolucao}'
                )
            )

        self.stdout.write(self.style.SUCCESS(f'Processo concluído. Total de {count} empréstimos devolvidos automaticamente.'))