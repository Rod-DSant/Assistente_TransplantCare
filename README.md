✨ Assistente_TransplantCare ✨
Assistente Pessoal Inteligente para Pacientes Transplantados
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini API](https://img.shields.io/badge/Google%20Gemini%20API-SDK-informational.svg?style=for-the-badge&logo=google-ai&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Powered-red.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Project Status](https://img.shields.io/badge/Status-Prototype-orange.svg?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)


## 📄 Sobre o Projeto

Este projeto é um **protótipo** de assistente pessoal, criado com o objetivo de explorar o potencial da Inteligência Artificial Generativa para auxiliar pacientes que passaram por um transplante de órgãos. Ele serve como um exemplo prático de como a IA pode ser aplicada para oferecer suporte conversacional, gerenciar informações e automatizar tarefas simples, como lembretes e buscas por dados relevantes.

## 💡 Conexão com a Imersão IA Alura e Google Gemini

Este trabalho é um resultado direto do aprendizado na **Imersão IA Alura e Google Gemini**. Ele solidifica conceitos fundamentais das aulas:

* **Aula 4: Criando seu primeiro chatbot com IA generativa** 🤖
    * Utilização da API Key do Google AI Studio e do SDK do Gemini para construir a base conversacional.
    * Exploração de parâmetros da API para moldar as respostas.
* **Aula 5: Construindo agentes que resolvem tarefas por você** 🛠️
    * Implementação do conceito de **Agentes** através do mecanismo de **Chamada de Função (Function Calling)** da API do Gemini.
    * Criação e descrição de **Ferramentas** (funções Python) para o agente utilizar.
    * Orquestração da interação: a IA decide qual ferramenta usar, e o código Python executa a ferramenta e retorna o resultado para a IA gerar a resposta final para o usuário.

A interface gráfica com **Streamlit** transforma o backend em um aplicativo web acessível, demonstrando como entregar uma experiência de usuário mais amigável.

## ✨ Funcionalidades Principais

* **Chat Conversacional:** Interaja com o assistente sobre dúvidas gerais relacionadas ao pós-transplante (lembre-se do aviso médico!).
* **Gerenciamento de Lembretes:** Peça ao assistente para anotar lembretes específicos (tarefa, horário, data). Os lembretes são listados na barra lateral durante a sessão do aplicativo.
* **Busca na Internet:** O agente pode realizar buscas online para obter informações que ele não possui ou que necessitam de dados atualizados, utilizando o resultado para formular a resposta.
* **Interface Gráfica Web:** Acesse todas as funcionalidades através de uma interface web simples e intuitiva.

---

## 🚀 Como Rodar o Projeto Localmente

Siga estes passos para ter o assistente rodando na sua máquina:

1.  **Pré-requisitos:**
    * Python 3.8 ou superior instalado.
    * `pip` (gerenciador de pacotes do Python).
    * Acesso ao Terminal/Linha de Comando.
    * Uma **API Key válida do Google Gemini**. Obtenha a sua em: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

2.  **Clone o Repositório:**
    Abra o terminal e clone este projeto para uma pasta no seu computador:
    ```bash
    git clone [LINK_DO_SEU_REPOSITORIO_AQUI]
    cd [NOME_DA_PASTA_DO_REPOSITORIO] # Entre na pasta clonada
    ```
    *(Substitua os placeholders com as informações do seu repositório).*

3.  **Crie e Ative um Ambiente Virtual:**
    É uma boa prática para isolar as dependências.
    * No Linux/macOS:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * No Windows (Prompt de Comando):
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    * No Windows (PowerShell):
        ```powershell
        python -m venv venv
        venv\Scripts\Activate.ps1
        ```
    *(Seu prompt do terminal deve mostrar `(venv)` no início).*

4.  **Instale as Dependências do Projeto:**
    Com o ambiente virtual ativo, instale as bibliotecas listadas no `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure sua API Key como Variável de Ambiente:**
    Sua chave da API é lida de uma variável de ambiente chamada `GOOGLE_API_KEY`. Defina-a no **terminal onde você vai rodar o Streamlit** (substitua `SUA_CHAVE_DA_API_DO_GOOGLE` pela sua chave real):
    * No Linux/macOS:
        ```bash
        export GOOGLE_API_KEY='SUA_CHAVE_DA_API_DO_GOOGLE'
        ```
    * No Windows (Prompt de Comando):
        ```bash
        set GOOGLE_API_KEY='SUA_CHAVE_DA_API_DO_GOOGLE'
        ```
    * No Windows (PowerShell):
        ```powershell
        $env:GOOGLE_API_KEY='SUA_CHAVE_DA_API_DO_GOOGLE'
        ```
    *(Esta configuração vale apenas para esta sessão do terminal).*

6.  **Execute o Aplicativo Streamlit:**
    Com o ambiente virtual ativo e a variável de ambiente configurada no **mesmo terminal**, rode o script principal:
    ```bash
    streamlit run app.py
    ```

7.  **Acesse o Assistente:**
    Seu navegador padrão abrirá uma nova aba com o aplicativo, geralmente em `http://localhost:8501`.

---

## 📸 Screenshots

*(Esta é uma seção onde você adicionará imagens do seu aplicativo rodando. É a melhor forma de mostrar como ele funciona!)*

**Instruções:**
1.  Rode o Streamlit (`streamlit run app.py`).
2.  Abra o aplicativo no navegador (`http://localhost:8501`).
3.  Use a ferramenta de captura de tela do seu sistema operacional para tirar fotos da interface (por exemplo, uma do chat, outra mostrando um lembrete na sidebar).
4.  Salve essas imagens em uma pasta no seu repositório (sugiro criar uma pasta chamada `images`).
5.  Faça o upload das imagens para o seu repositório no GitHub (na pasta `images`).
6.  Use a sintaxe Markdown abaixo para incluir as imagens aqui no `README.md`.

![Screenshot da Interface Principal]([LINK_PARA_SUA_IMAGEM_DO_CHAT_AQUI])
*(Ex: `![Screenshot da Interface Principal](images/screenshot_chat.png)` se você salvou a imagem na pasta `images` com o nome `screenshot_chat.png`)*

![Screenshot da Sidebar com Lembretes]([LINK_PARA_SUA_IMAGEM_DA_SIDEBAR_AQUI])
*(Ex: `![Screenshot da Sidebar com Lembretes](images/screenshot_lembrete.png)`)*

---

## ⚠️ AVISO MÉDICO CRUCIAL:

**Este assistente é um PROTÓTIPO educacional e NÃO fornece aconselhamento médico profissional. Ele não substitui a consulta, diagnóstico ou tratamento por uma equipe de saúde qualificada (médicos, enfermeiros, nutricionistas, etc.).**

**Sempre consulte sua equipe médica para quaisquer dúvidas ou decisões relacionadas à sua saúde, medicação, dieta ou rotina pós-transplante.**

**Os lembretes gerenciados por este protótipo são SIMULADOS para fins de demonstração da funcionalidade de agente e podem não ser confiáveis para uso real. NÃO dependa deste assistente para gerenciar sua medicação ou compromissos médicos essenciais.**

---

## ⏭️ Possíveis Melhorias Futuras

* Persistência dos lembretes (salvar em banco de dados).
* Integração com fontes de informação médica validadas (APIs de saúde, bases de dados curadas).
* Implementação de mais ferramentas (ex: rastreamento simples de sinais vitais, registro alimentar).
* Melhorias na interface do usuário e responsividade.
* Funcionalidades como lembretes recorrentes ou notificações reais (requerem infraestrutura mais complexa).

---

## 🧑‍💻 Autor

Rodrigo dos Santos

* LinkedIn: https://www.linkedin.com/in/rodrigo-dos-santos-838326297/.
* GitHub: https://github.com/Rod-DSant/Assistente_TransplantCare.
