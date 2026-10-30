    Newspaper Agency

Sistema web de gerenciamento de redatores, tópicos, jornais e revistas, desenvolvido com Python e Django.

    Sobre o projeto

O Newspaper Agency é uma aplicação web desenvolvida para organizar e administrar as informações de uma agência de notícias. O sistema permite cadastrar redatores, criar tópicos e gerenciar publicações jornalísticas, oferecendo funcionalidades de listagem, pesquisa, paginação, visualização de detalhes e controle de acesso.

O projeto foi desenvolvido utilizando os recursos do Django para estruturar os modelos de dados, processar requisições, validar formulários, gerenciar usuários e implementar as operações de criação, consulta, atualização e exclusão de registros.
    
A aplicação possui quatro modelos principais:

Redactor: representa os redatores cadastrados e também funciona como modelo de usuário para autenticação.
Topic: representa os tópicos utilizados para organizar as publicações.
Newspaper: representa os jornais cadastrados.
Magazine: representa as revistas cadastradas.

O objetivo é oferecer uma plataforma organizada, segura e extensível para o gerenciamento das informações relacionadas à produção de conteúdo jornalístico.

    Objetivos
Desenvolver uma aplicação web utilizando Python e Django.
Implementar operações CRUD para as principais entidades do sistema.
Estabelecer relacionamentos entre redatores, tópicos, jornais e revistas.
Implementar autenticação para restringir o acesso às páginas da aplicação.
Aplicar regras de autorização para proteger operações de atualização e exclusão.
Disponibilizar campos de pesquisa específicos para cada módulo.
Facilitar a navegação por meio de páginas de listagem e detalhes.
Utilizar formulários do Django para validar e processar os dados enviados pelos usuários.
🛠️ Tecnologias e recursos utilizados
Python: linguagem utilizada no desenvolvimento da aplicação.
Django: framework responsável pela arquitetura web, pelas views, pelos formulários, pela autenticação e pelo acesso ao banco de dados.
Django ORM: utilizado para representar os modelos e consultar os registros por meio de objetos Python.
Django Generic Class-Based Views: utilizado para implementar listagens, cadastros, atualizações, exclusões e páginas de detalhes.
Django Authentication: utilizado no gerenciamento de usuários, login e sessões.
Django Forms e ModelForms: utilizados na construção e validação dos formulários.
django-countries: utilizado para disponibilizar campos de seleção de países nos formulários.
Templates Django: utilizados para renderizar as páginas HTML da aplicação.
Banco de dados relacional: utilizado para armazenar os registros e os relacionamentos entre as entidades.
    Modelagem de dados

A aplicação possui quatro modelos principais, definidos no arquivo models.py.

1. Redactor — Redatores

O modelo Redactor representa os profissionais cadastrados na agência e herda de AbstractUser, disponibilizado pelo Django.

Essa decisão permite aproveitar os recursos de autenticação existentes no framework, incluindo nome de usuário, senha, e-mail, nome, sobrenome e mecanismos de gerenciamento de usuários.

Campos
Campo	Descrição
username	Nome de usuário utilizado na identificação e autenticação.
password	Senha armazenada por meio dos mecanismos de hash do Django.
email	Endereço de e-mail do redator.
first_name	Nome do redator.
last_name	Sobrenome do redator.
experience_years	Quantidade de anos de experiência, com valor padrão igual a zero.
birth_date	Data de nascimento, opcional.

Os campos de autenticação herdados de AbstractUser também incluem atributos como is_active, is_staff, is_superuser e as permissões do usuário.

Funcionalidades
Listar todos os redatores cadastrados.
Cadastrar novos redatores.
Pesquisar redatores pelo nome ou sobrenome.
Selecionar um redator em uma lista de opções.
Visualizar os detalhes individuais de um redator.
Atualizar os dados de um redator.
Excluir um redator.

A listagem utiliza paginação de cinco registros por página.

A pesquisa é realizada por meio dos campos first_name e last_name, utilizando icontains, que permite localizar correspondências parciais sem diferenciar letras maiúsculas e minúsculas.

O formulário RedactorCreationForm utiliza ModelForm para gerar os campos a partir do modelo. A data de nascimento é configurada como opcional e possui um widget de entrada de data.

Regras de autorização

A atualização e a exclusão possuem uma verificação de acesso na view:

O próprio redator pode atualizar ou excluir sua conta.
Um superusuário também pode realizar essas operações.
Outros usuários recebem uma exceção PermissionDenied.

A página de detalhes também possui uma restrição semelhante no código atual. Portanto, a visualização individual não está liberada para qualquer usuário autenticado: ela depende da relação entre o usuário conectado e o redator consultado.

2. Topic — Tópicos

O modelo Topic representa os assuntos utilizados para classificar e organizar os conteúdos jornalísticos.

Campos
Campo	Descrição
name	Nome do tópico, com até 255 caracteres.
slug	Identificador textual exclusivo, adequado para URLs.
redactors	Relacionamento muitos-para-muitos com redatores.
creator	Referência ao redator responsável pela criação do tópico.

O campo slug possui a restrição unique=True, garantindo que dois tópicos não tenham o mesmo slug no banco de dados.

O campo redactors permite associar vários redatores ao mesmo tópico e um redator a vários tópicos.

O campo creator registra o responsável pelo tópico. Ele permite valores nulos, mas utiliza on_delete=models.CASCADE, de modo que a exclusão do redator responsável também pode excluir os tópicos relacionados a ele.

Funcionalidades
Listar todos os tópicos cadastrados.
Criar novos tópicos.
Pesquisar tópicos pelo nome.
Consultar os detalhes de um tópico.
Visualizar os redatores associados.
Atualizar tópicos.
Excluir tópicos.

A listagem utiliza paginação de cinco registros por página.

A pesquisa utiliza name__icontains, permitindo localizar tópicos por correspondências parciais no nome.

O método get_absolute_url() direciona para a rota de detalhes do tópico, utilizando seu identificador primário.

Regras de autorização

A atualização, a exclusão e a visualização dos detalhes verificam se o usuário conectado é o criador do tópico ou um superusuário.

Se o usuário não cumprir essa condição, a aplicação retorna PermissionDenied.

No código atual, a criação de tópicos exige autenticação, mas a view não define explicitamente o campo creator com o usuário conectado. Esse comportamento deve ser configurado na view de criação para garantir que a autoria seja registrada corretamente.

3. Newspaper — Jornais

O modelo Newspaper representa as publicações jornalísticas cadastradas na aplicação.

Campos
Campo	Descrição
title	Título do jornal, com até 255 caracteres.
comments	Campo de texto para comentários.
published_date	Data de publicação do jornal.
redactors	Relacionamento muitos-para-muitos com redatores.
topics	Relacionamento muitos-para-muitos com tópicos.
creator	Referência ao redator responsável pela criação do registro.

O modelo permite associar vários redatores e vários tópicos a um mesmo jornal.

Da mesma forma, um redator pode participar de diferentes publicações, e um tópico pode estar associado a diferentes jornais.

Funcionalidades
Listar os jornais cadastrados.
Criar novos jornais.
Pesquisar jornais pela data de publicação.
Consultar título, data de publicação, redatores e tópicos.
Visualizar os detalhes individuais de um jornal.
Atualizar jornais.
Excluir jornais.

A listagem utiliza paginação de cinco registros por página.

A pesquisa é realizada a partir do parâmetro date recebido na requisição e utiliza um filtro de igualdade para comparar a data informada com o campo de publicação.

O método get_absolute_url() direciona para a página de detalhes do jornal.

Regras de autorização

A atualização, a exclusão e a visualização dos detalhes são restritas ao criador do jornal ou a um superusuário.

O cadastro exige autenticação, mas o campo creator precisa ser preenchido explicitamente na criação para que a regra de autoria funcione de forma consistente.

4. Magazine — Revistas

O modelo Magazine representa as revistas cadastradas na agência.

Sua estrutura é semelhante à do modelo Newspaper, permitindo manter um padrão consistente entre os dois tipos de publicação.

Campos
Campo	Descrição
title	Título da revista, com até 255 caracteres.
comments	Campo de texto para comentários.
published_date	Data de publicação da revista.
redactors	Relacionamento muitos-para-muitos com redatores.
topics	Relacionamento muitos-para-muitos com tópicos.
creator	Referência ao redator responsável pela criação do registro.
Funcionalidades
Listar todas as revistas cadastradas.
Criar novas revistas.
Pesquisar revistas pelo título.
Consultar título, data de publicação, tópicos e redatores.
Visualizar os detalhes individuais de uma revista.
Atualizar revistas.
Excluir revistas.

A listagem utiliza paginação de cinco registros por página.

A pesquisa utiliza title__icontains, permitindo localizar revistas a partir de parte do título, sem diferenciar maiúsculas de minúsculas.

O método get_absolute_url() direciona para a página de detalhes da revista.

Regras de autorização

A atualização, a exclusão e a visualização dos detalhes verificam se o usuário conectado é o criador do registro ou um superusuário.

A criação exige autenticação. Para manter o controle de autoria, o campo creator deve ser preenchido pela view com o usuário conectado.

    Relacionamentos entre os modelos

Os relacionamentos foram definidos utilizando os recursos do Django ORM.

Redactor e Topic: relacionamento muitos-para-muitos por meio do campo redactors.
Redactor e Newspaper: relacionamento muitos-para-muitos por meio do campo redactors.
Redactor e Magazine: relacionamento muitos-para-muitos por meio do campo redactors.
Topic e Newspaper: relacionamento muitos-para-muitos por meio do campo topics.
Topic e Magazine: relacionamento muitos-para-muitos por meio do campo topics.
Redactor e Topic/Newspaper/Magazine: relacionamento adicional por meio do campo creator, que registra o responsável pela criação.

Esses relacionamentos permitem que os conteúdos sejam associados a vários profissionais e assuntos, sem a necessidade de duplicar os dados de redatores ou tópicos.

Representação simplificada
text
Redactor
   ├── Topics
   ├── Newspapers
   ├── Magazines
   └── Registros criados (creator)

Topic
   ├── Redactors
   ├── Newspapers
   └── Magazines

Newspaper
   ├── Redactors
   ├── Topics
   └── Creator

Magazine
   ├── Redactors
   ├── Topics
   └── Creator

📝 Formulários e validação

Os formulários estão definidos no arquivo forms.py e utilizam tanto forms.Form quanto forms.ModelForm.

Formulários de pesquisa
Formulário	Funcionalidade
RedactorSearchForm	Pesquisa por nome e seleção de redator.
TopicSearchForm	Pesquisa por nome do tópico.
NewspaperSearchForm	Pesquisa pela data de publicação.
MagazineSearchForm	Pesquisa pelo título da revista.

Os campos de pesquisa são opcionais, permitindo que o usuário consulte todos os registros quando não informa um filtro.

No formulário de redatores, o campo redactor utiliza ModelChoiceField, preenchido com os redatores existentes no banco de dados.

Formulários de criação e edição
RedactorCreationForm: utiliza o modelo Redactor e inclui a configuração do campo de data de nascimento e da nacionalidade.
TopicForm: utiliza o modelo Topic e configura o campo de nacionalidade.
NewspaperForm: utiliza o modelo Newspaper e configura o campo de nacionalidade.
MagazineCreationForm: utiliza o modelo Magazine e configura o campo de nacionalidade.

Os formulários de tópicos, jornais e revistas excluem o campo creator dos campos editáveis, evitando que o usuário escolha livremente o responsável pela criação no formulário.

O campo nationality é configurado com CountryField, disponibilizando uma seleção de países. Entretanto, esse campo não aparece nos modelos apresentados. Para que a nacionalidade seja armazenada de forma persistente, é necessário definir o campo nos modelos correspondentes ou tratá-lo separadamente.

Observação sobre as datas

O formulário de redatores configura a data de nascimento com um widget de data e formatos de entrada específicos.

Os formulários de jornais e revistas apresentam um placeholder para a data no formato dd/mm/yyyy. No entanto, a configuração de input_formats aparece dentro da classe Meta, em vez de estar em um método __init__ da classe do formulário.

Para garantir que o formato de data seja efetivamente aplicado, recomenda-se mover essa configuração para o nível da classe do formulário ou configurá-la diretamente no campo correspondente.

    Pesquisa e paginação

O sistema implementa filtros específicos para cada módulo.

Módulo	Campo pesquisado	Estratégia
Redatores	Nome e sobrenome	icontains
Tópicos	Nome	icontains
Jornais	Data de publicação	Igualdade
Revistas	Título	icontains

A pesquisa de redatores também permite selecionar um registro específico por meio de seu identificador.

Todas as listagens apresentadas em views.py utilizam paginate_by = 5, reduzindo a quantidade de registros exibidos por página.

A paginação contribui para a organização visual e pode reduzir a quantidade de dados processados e apresentados de uma só vez.

🔐 Autenticação e autorização

A aplicação utiliza os mecanismos de autenticação do Django para restringir o acesso às páginas protegidas.

O uso de LoginRequiredMixin nas views baseadas em classes exige que o usuário esteja autenticado para acessar listagens, cadastros, atualizações, exclusões e detalhes protegidos.

A página inicial utiliza o decorador login_required, aplicando a mesma exigência de autenticação.

Regras de acesso implementadas
Usuários autenticados podem acessar as listagens e os formulários de criação protegidos.
Redatores podem atualizar e excluir seus próprios registros.
Criadores podem atualizar, excluir e visualizar os detalhes dos registros que criaram, conforme as verificações existentes.
Superusuários podem acessar as operações protegidas por essas verificações.
Usuários sem autorização recebem PermissionDenied.

Importante: a autorização implementada nas views é baseada principalmente na propriedade do registro e no status de superusuário. Ela não equivale automaticamente a um sistema completo de permissões por grupos do Django.

Além disso, os botões da interface devem refletir as mesmas regras das views. A proteção no servidor continua sendo obrigatória, mesmo quando um botão não é exibido.

    Página inicial e indicadores

A função index apresenta informações gerais sobre a aplicação.

Ela consulta a quantidade total de:

Redatores.
Tópicos.
Jornais.
Revistas.

A página também utiliza a sessão do Django para registrar o número de visitas realizadas pelo usuário ao painel, por meio da chave num_visits.

Esses dados permitem apresentar um resumo da atividade cadastrada e oferecer um ponto de entrada para os principais módulos do sistema.

    Rotas da aplicação

As rotas estão definidas no arquivo urls.py, com o namespace newspaper.

Caminho	Funcionalidade
/	Página inicial.
/accounts/login/	Login.
/logout/	Logout.
/redactors/	Listagem de redatores.
/redactors/create/	Cadastro de redator.
/redactors/<id>/detail/	Detalhes de redator.
/redactors/<id>/update/	Atualização de redator.
/redactor/<id>/delete/	Exclusão de redator.
/topics/	Listagem de tópicos.
/topics/create/	Cadastro de tópico.
/topic/<id>/detail/	Detalhes de tópico.
/topics/<id>/update/	Atualização de tópico.
/topics/<id>/delete/	Exclusão de tópico.
/publications/	Listagem de jornais.
/publications/create/	Cadastro de jornal.
/publications/<id>/	Detalhes de jornal.
/publications/<id>/update/	Atualização de jornal.
/publications/<id>/delete/	Exclusão de jornal.
/magazines/	Listagem de revistas.
/magazines/create/	Cadastro de revista.
/magazines/<id>/	Detalhes de revista.
/magazines/<id>/update/	Atualização de revista.
/magazines/<id>/delete/	Exclusão de revista.

<id> representa o identificador numérico do registro, recebido pela view como parâmetro pk.

    Decisões técnicas
Uso de modelos baseados em classes

O projeto utiliza modelos Django para definir os campos e relacionamentos das entidades.

A herança de AbstractUser no modelo Redactor evita a necessidade de manter uma tabela de perfil completamente separada para os principais dados de autenticação.

Como o modelo de usuário foi personalizado, a configuração do projeto deve definir AUTH_USER_MODEL = "newspaper.Redactor" se newspaper for o nome real da aplicação Django. Essa configuração deve ser feita desde o início do projeto, antes das primeiras migrações de usuários.

Uso de Generic Class-Based Views

As views utilizam classes genéricas do Django, como:

ListView para listagens.
CreateView para cadastros.
UpdateView para atualizações.
DeleteView para exclusões.
DetailView para detalhes individuais.

Essa decisão reduz a repetição de código e aproveita o comportamento padrão do Django para carregar objetos, processar formulários e renderizar templates.

Uso de reverse_lazy

O projeto utiliza reverse_lazy para definir URLs de redirecionamento após operações de criação, atualização e exclusão.

Essa abordagem permite resolver o nome da rota de maneira preguiçosa, o que é adequado para atributos de classes baseadas em views genéricas.

Uso de get_queryset

O método get_queryset() é sobrescrito nas listagens para aplicar filtros com base nos parâmetros enviados na requisição.

Essa estratégia centraliza a lógica de pesquisa na view, mantendo os templates responsáveis principalmente pela apresentação dos resultados.

Uso de get_object

O método get_object() é utilizado em views protegidas para verificar se o usuário conectado pode acessar o registro solicitado.

Quando a condição de autorização não é atendida, a view lança PermissionDenied, impedindo a operação.

Uso de get_absolute_url

Os modelos Topic, Newspaper e Magazine implementam get_absolute_url() para fornecer uma URL canônica para seus detalhes.

Isso facilita a navegação e permite que o Django identifique a página associada a cada objeto.

Uso de Q para pesquisas combinadas

Na listagem de redatores, a classe Q permite pesquisar pelo nome ou sobrenome utilizando uma condição lógica OR.

Essa abordagem amplia a flexibilidade da pesquisa sem exigir formulários ou consultas separadas para cada campo.

    Testes recomendados

Para validar as regras de negócio e a segurança da aplicação, recomenda-se testar:

O login e o logout.
O cadastro e a listagem de redatores.
A pesquisa por nome e sobrenome.
A seleção de redatores.
A criação, a pesquisa e os detalhes dos tópicos.
O cadastro, a pesquisa por data e os detalhes dos jornais.
O cadastro, a pesquisa por título e os detalhes das revistas.
A atualização e a exclusão pelo criador do registro.
A tentativa de acessar registros de outros usuários.
O acesso de superusuários às operações protegidas.
A validação dos campos obrigatórios.
A integridade dos relacionamentos entre os modelos.
O comportamento da paginação.
A validação dos formatos de data.

Os testes podem ser implementados com TestCase, Client e as ferramentas de teste disponibilizadas pelo Django.

🚀 Como executar o projeto
1. Clonar o repositório
bash
git clone <URL_DO_REPOSITORIO>
cd newspaper-agency

2. Criar e ativar um ambiente virtual

Windows:

bash
python -m venv .venv
.venv\Scripts\activate


Linux ou macOS:

bash
python3 -m venv .venv
source .venv/bin/activate

3. Instalar as dependências

Se o projeto possuir um arquivo requirements.txt:

bash
pip install -r requirements.txt


As dependências devem incluir a versão de Django utilizada e o pacote django-countries, além de eventuais outras bibliotecas do projeto.

4. Configurar o banco de dados

Confira as configurações em settings.py, incluindo o modelo de usuário personalizado.

Se o projeto ainda estiver em desenvolvimento e as migrações não tiverem sido criadas:

bash
python manage.py makemigrations
python manage.py migrate

5. Criar um superusuário
bash
python manage.py createsuperuser

6. Executar o servidor
bash
python manage.py runserver


A aplicação ficará disponível, por padrão, em http://127.0.0.1:8000/.

    Considerações finais

O Newspaper Agency aplica conceitos importantes do desenvolvimento web com Django, incluindo modelagem relacional, herança de modelos, formulários, views genéricas, filtros, paginação, autenticação e autorização.

A estrutura foi pensada para permitir que a agência organize os redatores, classifique os conteúdos por tópicos e gerencie jornais e revistas com informações centralizadas.

A separação das responsabilidades entre modelos, formulários, views e rotas facilita a manutenção e permite que novas funcionalidades sejam adicionadas de maneira progressiva.

O projeto também demonstra a importância de associar regras de negócio ao controle de acesso, garantindo que operações sensíveis sejam verificadas no servidor e não dependam exclusivamente da interface.

Observação: este README descreve a implementação fornecida e destaca os pontos que merecem atenção para que o comportamento final seja consistente com as regras de negócio pretendidas. Os ajustes identificados podem ser realizados sem alterar o objetivo principal do sistema.