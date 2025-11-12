# 📚 SGbBook (SGBLivros) - Sistema de Gerenciamento e Empréstimo de Livros

O SGBook é um Sistema de Gerenciamento de Biblioteca (SGB) desenvolvido em Django, focado em fornecer uma plataforma completa para a administração de um catálogo de livros e o controle de empréstimos, com suporte para leitura de e-books diretamente na plataforma.

## ✨ Destaques e Funcionalidades Principais

### Gerenciamento de Conteúdo (`sgblivros` App)

* **Catálogo Completo:** Permite o cadastro e listagem de Livros, Autores e Editoras.
* **Detalhes do Livro:** Tela dedicada para visualizar informações completas sobre um livro, incluindo ano de publicação, autor e editora.
* **Controle de Empréstimos:** Funcionalidades para iniciar, rastrear e finalizar o empréstimo de livros físicos ou digitais.
* **Leitura Digital (Ebook):** Suporte para anexar arquivos PDF ou EPUB e iniciar a leitura diretamente no navegador, desde que o usuário possua um empréstimo ativo.
* **Administração:** Interface de administração robusta do Django (`/admin`) para gerenciamento de todos os modelos (Livros, Autores, Empréstimos, Usuários).

### Autenticação e Usuários (`sgbUsuarios` App)

* **Autenticação Padrão:** Login, Logout e Registro de usuários.
* **Autenticação Social:** Suporte nativo para login via **Google**, utilizando o pacote `django-allauth`.

## 🚀 Melhorias e Correções Implementadas (Última Atualização)

Esta seção detalha as principais melhorias e correções que garantiram a estabilidade e a usabilidade do sistema nas últimas iterações de desenvolvimento:

### 1. Reestruturação e Fixação de Templates

* **Padrão de Template Django Corrigido:** Todos os arquivos de template específicos do aplicativo (`detalhes_livro.html`, `livros.html`, etc.) foram movidos para a subpasta padrão `sgblivros/templates/sgblivros/`.
* **Correção na View de Detalhes:** A função `detalhes_livro` no `views.py` foi atualizada para buscar o template pelo caminho canônico `'sgblivros/detalhes_livro.html'`, resolvendo o erro `TemplateDoesNotExist` que impedia a abertura individual dos livros.
* **Configuração de Template Ajustada:** As configurações de `TEMPLATES` no `settings.py` foram revisadas para garantir que o `AppDirectoriesLoader` funcione corretamente, permitindo que o Django encontre templates dentro da estrutura de cada aplicativo (como `sgblivros` e `sgbUsuarios`).

### 2. Rotas e Acesso aos Livros

* **URL de Detalhes Ativa:** O endereço de rota `/livro/<int:livro_id>/` agora funciona corretamente, permitindo que os usuários naveguem da listagem para a página de detalhes de qualquer livro cadastrado (ex: `/livro/15/` para o livro "Silêncio").

### 3. Setup do Projeto

* **Instalação Finalizada:** Aplicação de todas as migrações de banco de dados pendentes (`makemigrations` e `migrate`), garantindo que a estrutura do banco de dados (incluindo modelos como `Livro`, `Emprestimo` e `Autor`) esteja atualizada e pronta para uso.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia | Uso Principal no Projeto |
| :--- | :--- | :--- |
| **Backend / Framework** | **Python 3.13+** | Linguagem de programação principal. |
| | **Django 5.x** | Framework web para o desenvolvimento rápido do servidor, lógica de negócios, ORM e URLs. |
| **Banco de Dados** | **SQLite 3** | Banco de dados leve e padrão do Django, utilizado para desenvolvimento e testes. |
| **Frontend / Templates** | **HTML5 & CSS3** | Estruturação e estilização da interface de usuário. |
| | **Django Template Language (DTL)** | Linguagem de template para renderização de conteúdo dinâmico. |
| **Autenticação** | **django-allauth** | Pacote robusto para gerenciar todas as formas de autenticação (registro, login social, redefinição de senha). |
| | **Google Social Provider** | Integração via `allauth` para permitir o login de usuários usando suas contas Google. |
| **Controle de Versão** | **Git** | Sistema de controle de versão distribuído. |
| | **GitHub** | Hospedagem remota do repositório Git. |

## ⚙️ Próximos Passos (Em Desenvolvimento)

* **Metas de Leitura:** Implementação de um novo modelo para que os usuários possam definir metas de leitura (por exemplo, "Ler 12 livros até o final do ano").
* **Relatórios e Estatísticas:** Desenvolvimento de views para exibir estatísticas sobre a biblioteca e o progresso das metas de leitura dos usuários.
