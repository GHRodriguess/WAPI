# WAPI

### ÍNDICE 

1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Pré-requisitos](#pré-requisitos)
5. [Instalação](#instalação) 
  5.1. [IDE](#ide)
  5.2. [SETUP](#setup)
6. [Uso](#uso) 


### VISÃO GERAL
A WhatsApp Automation API foi desenvolvida para simplificar a comunicação em massa via WhatsApp Web. Através de uma interface gráfica construída com PyQt5, o usuário pode adicionar contatos, criar grupos e enviar mensagens em lote de maneira automatizada. A aplicação também permite a execução de múltiplas tarefas em segundo plano, além de tratar erros e reconectar-se ao WhatsApp Web automaticamente caso ocorram problemas durante o envio.

### FUNCIONALIDADES
* Interface gráfica intuitiva: Desenvolvida com PyQt5, facilitando o uso por parte do usuário.
* Envio automatizado de mensagens: Envio em massa para contatos e grupos via WhatsApp Web utilizando Selenium.
* Adição e gerenciamento de contatos/grupos: Ferramentas fáceis para gerenciar e armazenar listas de contatos e grupos.
* Execução de múltiplas tarefas simultaneamente: Suporte a threads para executar tarefas como o envio de mensagens em paralelo.
* Reconexão automática: Em caso de falha ou perda de conexão, a API tenta reconectar-se ao WhatsApp Web automaticamente.
* Exibição de erros e logs: A aplicação gera logs detalhados sobre erros encontrados durante a execução de tarefas.

### TECNOLOGIAS UTILIZADAS
* **Python 3.10.6**: Linguagem principal para o desenvolvimento da API.
* **PyQt5**: Framework utilizado para a construção da interface gráfica (GUI).
* **Selenium**: Ferramenta para automação de interação com o WhatsApp Web.

### PRÉ-REQUISITOS
Antes de começar, verifique se você atende os seguintes requisitos:

* **Google Chrome** instalado no sistema.

Além disso, se você for rodar a aplicação localmente em sua IDE, certifique-se de instalar todas as dependências necessárias. Utilize o comando abaixo para instalar os pacotes listados no arquivo requirements.txt:

```pip install -r requirements.txt```

### INSTALAÇÃO

##### IDE
1. Clone esse repositório:

```git clone https://github.com/GHRodriguess/WAPI.git```

2. Acesse o diretório do projeto:

```cd WAPI```

3. Instale as dependências necessárias:

```pip install -r requirements.txt```

4. Certifique-se que você tem alguma versão do Chrome instalada.

5. Execute a aplicação:

```python main.py ```

##### SETUP
Se preferir, você pode instalar a aplicação utilizando o instalador .exe disponível nas releases. Basta baixar o arquivo mais recente e seguir o processo de instalação.

1. Acesse a página de [releases](https://github.com/GHRodriguess/WAPI/releases/latest) do projeto.
2. Execute o arquivo "*setupWAPI.exe*".
3. Siga as instruções para instalar a aplicação. 

### USO

##### INTERFACE
Ao abrir o aplicativo, a tela de carregamento será exibida enquanto a API do WhatsApp é inicializada e o navegador é configurado. Após a inicialização, a tela principal da aplicação será carregada com diversas funcionalidades.

##### CONEXÃO COM O WHATSAPP WEB
A aplicação abrirá automaticamente o WhatsApp Web.
1. Escaneie o código QR com o aplicativo WhatsApp no seu telefone para conectar.
2. Após a conexão bem-sucedida, a interface da API estará pronta para uso.

##### GERENCIAMENTO DE CONTATOS E GRUPOS
Na tela de contatos, você pode adicionar novos contatos ou grupos clicando nos botões "Adicionar Contato" ou "Adicionar Grupo".

* Adicionar Contato: Insira os detalhes do contato e clique em "Salvar". O contato será adicionado à lista de contatos.
* Adicionar Grupo: Insira os nomes dos membros do grupo e clique em "Salvar" para criar um novo grupo. O grupo será adicionado à lista de contatos.

Selecione os contatos e grupos que você deseja enviar as mensagens.

##### ENVIO DE MENSAGENS
Após selecionar os contatos para enviar mensagens configure as mensagens na tela principal, após configuração clique no botão "Executar" para iniciar o envio. O status do envio de mensagens será atualizado na interface, e a API informará se houver algum problema durante o processo.

##### TRATAMENTO DE ERROS
Se ocorrerem erros durante o processo de envio de mensagens, eles serão exibidos em uma tela separada dedicada ao tratamento de erros. Você poderá visualizar os detalhes e tentar reenviar as mensagens.


### CONTRIBUIÇÕES
Contribuições são sempre bem-vindas! Se você deseja contribuir para o projeto, siga os seguintes passos:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção (git checkout -b minha-feature).
3. Faça commit das suas alterações (git commit -am 'Adiciona nova feature').
4. Faça push para a branch criada (git push origin minha-feature).
5. Abra um Pull Request.