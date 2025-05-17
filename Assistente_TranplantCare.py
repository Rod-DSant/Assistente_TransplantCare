import streamlit as st
import google.generativeai as genai
import os
import json

# --- Instalar bibliotecas extras (rodar no terminal do ambiente virtual) ---
# Rode no seu terminal (ambiente virtual ativo):
# pip install streamlit google-generativeai googlesearch-python

# --- Configuração da API Key (Adaptada para Streamlit/Variáveis de Ambiente) ---
API_KEY = os.getenv('GOOGLE_API_KEY')

if not API_KEY:
    st.error("Erro: Chave da API do Google não encontrada. Defina a variável de ambiente GOOGLE_API_KEY ou use o Secrets do Streamlit Cloud.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    # st.success("API Key configurada com sucesso!") # Feedback visual removido
except Exception as e:
    st.error(f"Erro ao configurar a API Key. Verifique sua chave. Detalhe: {e}")
    st.stop()

# --- Definição das Funções (Nossas Ferramentas Reais) ---

# Nossa ferramenta de adicionar lembrete
def adicionar_lembrete_func(tarefa: str, horario: str, data: str = None):
    """Adiciona um lembrete para o paciente sobre uma tarefa médica ou compromisso."""
    lembrete_str = f"Lembrete: {tarefa} às {horario}"
    if data:
        lembrete_str += f" em {data}"
    st.session_state.lista_lembretes.append(lembrete_str)
    print(f"DEBUG (Terminal): Função 'adicionar_lembrete_func' executada. Lembrete: '{lembrete_str}'")
    return f"Lembrete para '{tarefa}' anotado."

# --- NOVA FUNÇÃO: Ferramenta de Busca na Internet ---
from googlesearch import search # Importa a função de busca da biblioteca instalada

def buscar_na_internet_func(query: str):
    """Busca informações na internet usando a consulta fornecida."""
    print(f"\nDEBUG (Terminal): Função 'buscar_na_internet_func' executada com query: '{query}'")
    try:
        # Realiza a busca (limita para os 5 primeiros resultados, timeout de 5 segundos)
        # Pode ajustar num_results e timeout conforme necessário
        search_results = list(search(query, num_results=5, timeout=5))

        if not search_results:
            return "Nenhum resultado encontrado na internet para esta busca."

        # Formata os resultados para enviar para a IA
        # A biblioteca googlesearch-python retorna URLs. Podemos formatar como lista.
        formatted_results = "Resultados da busca:\n"
        for i, result in enumerate(search_results):
             formatted_results += f"{i+1}. {result}\n"

        # Limita o tamanho do resultado para não estourar o limite de tokens da IA
        # O limite exato pode variar, 1500 é um valor de segurança
        if len(formatted_results) > 1500:
             formatted_results = formatted_results[:1500] + "..." # Trunca se for muito longo


        return formatted_results # Retorna a string formatada dos resultados para a IA

    except Exception as e:
        print(f"DEBUG (Terminal): Erro ao executar busca na internet: {e}")
        # Retorna uma mensagem de erro para a IA caso a busca falhe
        return f"Ocorreu um erro ao buscar na internet: {e}"


# --- Mapeia os nomes das ferramentas para as funções Python reais ---
# Este dicionário permite encontrar a função correta a partir do nome que a IA solicitar
tools_available = {
    "adicionar_lembrete": adicionar_lembrete_func, # Mapeia o nome "adicionar_lembrete" para a função adicionar_lembrete_func
    "buscar_na_internet": buscar_na_internet_func, # Mapeia o nome "buscar_na_internet" para a função buscar_na_internet_func
}


# --- Descrição das Ferramentas para o Modelo ---
# Esta lista diz para a IA quais funções existem, o que elas fazem, e quais parâmetros esperam
tools_description = [
    {
        "function_declarations": [
            # Descrição da ferramenta de lembrete
            {
                "name": "adicionar_lembrete",
                "description": "Adiciona um lembrete para o paciente sobre uma tarefa médica ou compromisso, incluindo o que lembrar, horário e data (se especificada).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tarefa": {
                            "type": "string",
                            "description": "A descrição clara e concisa da tarefa a ser lembrada (ex: tomar remédio, consulta com nefrologista, fazer exame de sangue)."
                        },
                        "horario": {
                            "type": "string",
                            "description": "O horário específico do lembrete na linguagem do usuário (ex: 8 da manhã, 14:30, meio-dia). Tente extrair o mais preciso possível."
                        },
                         "data": {
                            "type": "string",
                            "description": "A data do lembrete se for para um dia específico diferente de hoje (ex: amanhã, segunda-feira, 25 de dezembro). Opcional.",
                            "nullable": True
                        }
                    },
                    "required": ["tarefa", "horario"]
                }
            },
            # --- NOVA DESCRIÇÃO DE FERRAMENTA: Buscar na Internet ---
            {
                "name": "buscar_na_internet", # Nome EXATO da chave em tools_available
                "description": "Busca informações gerais na internet sobre um tópico específico. Use para responder perguntas sobre eventos recentes, fatos específicos, definições, ou qualquer coisa que não esteja no conhecimento geral do assistente ou exija dados atualizados.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "A consulta de busca clara e concisa a ser usada para encontrar a informação relevante."
                        }
                    },
                    "required": ["query"] # A IA DEVE fornecer uma consulta para a busca
                }
            }
            # Adicionar descrições de outras ferramentas aqui
        ]
    }
]


# --- Instanciar o Modelo (Passando TODAS as Ferramentas AQUI e usando st.session_state) ---
# Usamos st.session_state para garantir que o modelo só seja instanciado uma vez por sessão do usuário
if 'model' not in st.session_state:
    try:
        # Passando tools=tools_description para genai.GenerativeModel
        st.session_state.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest', # Ou outro modelo adequado
            tools=tools_description # <-- Passamos TODAS as descrições das ferramentas AQUI!
            # tool_config={"function_calling_config": "ANY"} # Opcional: Pode adicionar AQUI se suportado e necessário para encorajar o uso de tools
        )
        # st.success(f"Modelo '{st.session_state.model.model_name}' instanciado com ferramentas.") # Feedback visual removido
    except Exception as e:
        st.error(f"Erro ao instanciar o modelo com ferramentas. Verifique o nome do modelo, sua API Key ou a descrição das ferramentas. Detalhe: {e}")
        st.stop()

# --- Iniciar o Chat (Sem Mensagem system no Histórico Inicial) ---
# Vamos tentar iniciar o chat sem a mensagem explícita com role="system" no histórico.
# Isso pode resolver o erro 400 em algumas versões da API/modelo.
if 'chat' not in st.session_state:
    # O texto da instrução do sistema ainda está na variável system_instruction_text,
    # mas NÃO a passaremos no histórico inicial.
    # Alguns modelos podem ainda usar instruções passadas na instanciação ou depender das tool descriptions.
    try:
        # Removido o history=[{"role": "system", "parts": [...]}]
        st.session_state.chat = st.session_state.model.start_chat(history=[])
        # tools e tool_config já foram passados na instanciação do modelo

        # st.info("Chat iniciado com ferramentas.") # Feedback visual removido
    except Exception as e:
         st.error(f"Erro ao iniciar o chat. Detalhe: {e}")
         st.stop()

# NOTA: Sem a instrução do sistema no histórico, o comportamento geral da IA
# pode ser um pouco diferente. Ela dependerá mais das descrições das ferramentas
# e do seu treinamento geral. Se precisar de um comportamento mais específico,
# podemos tentar adicionar a instrução como a primeira mensagem do usuário,
# ou verificar se há outra forma de passar system instructions compatível.

# --- Lista para Armazenar Lembretes (Usando st.session_state) ---
if 'lista_lembretes' not in st.session_state:
    st.session_state.lista_lembretes = []

# --- Interface Gráfica com Streamlit ---
st.title("Assistente Pessoal para Pacientes Transplantados")
st.warning("ATENÇÃO: Este assistente é um protótipo e NÃO substitui o aconselhamento médico profissional. Sempre consulte sua equipe de saúde para decisões sobre seu tratamento.")

# Área para exibir a conversa (histórico visível)
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = [] # Lista de dicionários para o histórico visível

# Exibir mensagens anteriores do histórico visível
for mensagem in st.session_state.mensagens:
    if mensagem["role"] == "user":
        with st.chat_message("user"):
            st.markdown(mensagem["content"])
    elif mensagem["role"] == "assistant":
         with st.chat_message("assistant"):
            st.markdown(mensagem["content"])
    elif mensagem["role"] == "tool_code": # Exibe que uma chamada de ferramenta foi detectada
         with st.expander("🤖 Chamada de Ferramenta Detectada"):
              st.json(mensagem["content"]) # Mostra os detalhes da chamada (nome e args)
    elif mensagem["role"] == "tool_result": # Exibe o resultado retornado pela ferramenta
         with st.expander("✅ Resultado da Ferramenta"):
              # Tenta exibir como JSON se for um dicionário, senão exibe como texto
              content = mensagem["content"]
              try:
                  st.json(json.loads(content)) # Tenta carregar como JSON
              except (json.JSONDecodeError, TypeError):
                   st.text(content) # Se não for JSON, exibe como texto simples


# Campo de entrada do usuário na parte inferior
user_input = st.chat_input("Como posso ajudar?")

# --- Lógica de Processamento (Este bloco roda QUANDO o usuário envia uma mensagem) ---
if user_input:
    # --- 1. Adicionar a mensagem do usuário ao histórico visível e exibir ---
    st.session_state.mensagens.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- 2. Enviar a mensagem para o chat do Gemini (que está em session_state) ---
    # A IA (que foi instanciada COM as ferramentas) pode responder com texto OU uma chamada de função
    try:
        # Adiciona uma mensagem temporária enquanto espera a resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."): # Mostra um spinner
                 response = st.session_state.chat.send_message(user_input)

        # --- 3. Processar a Resposta da IA e Executar Ferramentas (Orquestração) ---

        # Verifica a resposta do modelo: Primeiro checa se houve chamada de função
        if response.function_calls:
            print("DEBUG (Terminal): IA solicitou chamada(s) de função.")
            # Não adicionamos "Pensando em como usar as ferramentas..." ao histórico visível aqui,
            # pois já usamos o spinner acima. Podemos adicionar o resultado da execução ao histórico.

            # Executa cada chamada de função que a IA solicitou
            for fc in response.function_calls:
                tool_name = fc.name
                tool_args = fc.args

                # Opcional: Adicionar a chamada de função ao histórico visível para debug
                st.session_state.mensagens.append({"role": "tool_code", "content": {"tool_name": tool_name, "args": tool_args}})

                if tool_name in tools_available:
                    print(f"DEBUG (Terminal): Executando ferramenta: '{tool_name}' com args: {tool_args}")
                    try:
                        # --- Executar a Ferramenta Real (sua função Python) ---
                        # Encontra a função Python correspondente e a chama
                        tool_result = tools_available[tool_name](**tool_args)

                        print(f"DEBUG (Terminal): Resultado da ferramenta '{tool_name}': '{tool_result}'")
                        # Opcional: Adicionar o resultado da ferramenta ao histórico visível para debug
                        st.session_state.mensagens.append({"role": "tool_result", "content": tool_result})


                        # --- 4. Enviar o Resultado da Ferramenta de Volta para a IA ---
                        # Isso é CRUCIAL. Permite que a IA saiba que a ferramenta rodou e qual foi o resultado,
                        # para então gerar a resposta final amigável para o usuário.
                        response_from_tool = st.session_state.chat.send_message(
                            {"role": "tool", # Indica que esta mensagem é a resposta DA FERRAMENTA
                             "parts": [{"functionResponse": {"name": tool_name, "response": {"content": tool_result}}}]} # Formato esperado pela API
                        )

                        # --- 5. Obter a Resposta Final da IA para o Usuário ---
                        # A resposta final (que usou o resultado da ferramenta para formular a resposta)
                        if response_from_tool.text:
                             st.session_state.mensagens.append({"role": "assistant", "content": response_from_tool.text})
                        else:
                             # Caso a IA não gere texto após a resposta da ferramenta (raro)
                             st.session_state.mensagens.append({"role": "assistant", "content": "OK. Ação realizada ou informação obtida."})


                    except Exception as ex_func:
                        # 6. Lidar com erros na execução da sua função Python
                        error_message = f"Erro ao executar a ferramenta '{tool_name}'. Detalhe: {ex_func}"
                        print(f"DEBUG (Terminal): {error_message}")
                        st.session_state.mensagens.append({"role": "assistant", "content": f"Desculpe, tive um problema ao tentar executar a ação solicitada ({tool_name})."})


                else:
                    # 7. A IA pediu uma ferramenta que não definimos!
                    print(f"DEBUG (Terminal): IA solicitou ferramenta desconhecida em tools_available: {tool_name}")
                    st.session_state.mensagens.append({"role": "assistant", "content": f"Desculpe, não consigo realizar essa ação solicitada ({tool_name})."})


        # 8. Se a IA NÃO pediu função, ela respondeu apenas com texto direto
        elif response.text:
            print("DEBUG (Terminal): IA respondeu apenas com texto.")
            st.session_state.mensagens.append({"role": "assistant", "content": response.text})

        # 9. Outro tipo de resposta ou resposta vazia do modelo
        else:
             print("DEBUG (Terminal): Resposta da IA vazia ou inesperada.")
             st.session_state.mensagens.append({"role": "assistant", "content": "Não consegui obter uma resposta válida no momento."})

        # --- 10. Gatilho para re-executar o script e atualizar a tela ---
        st.rerun() # Isso faz o Streamlit recarregar a página para mostrar as novas mensagens e o estado atual

    except Exception as e:
        # 11. Lidar com erros gerais na comunicação com a API ou processamento
        print(f"DEBUG (Terminal): Erro geral no processamento da resposta: {e}")
        st.error(f"Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente. Detalhe do erro: {e}")


# --- Área de Lembretes na Sidebar ---
# Esta seção sempre será exibida na barra lateral
with st.sidebar:
    st.header("Lembretes Anotados")
    if st.session_state.lista_lembretes:
        for i, lembrete in enumerate(st.session_state.lista_lembretes):
            st.write(f"• {lembrete}") # Usando bullet points
    else:
        st.write("Nenhum lembrete anotado ainda.")

# --- Fim do Script app.py ---