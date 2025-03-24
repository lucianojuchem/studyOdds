import streamlit as st
import google.generativeai as genai
import time


# Configuração da API do Gemini
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"] # Ou defina como variável de ambiente
genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-1.5-pro') #gemini-1.5-pro  gemini-2.0-flash

# Definição do contexto e instruções para o Gemini
CONTEXTO_APOSTAS = """
Você é um especialista em apostas esportivas e trader esportivo. Seu nome é Oddly. Seu objetivo é responder perguntas relacionadas a esses temas com enfase em trader esportivo.
Responda de forma resumida e com exemplos de aplicação nas apostas esportivas. Responda também somente se for questionado sobre conteúdos de estatisticas para trader esportivo e modelos de previsão que podem ser usados.
Lembre se que oa odd do LAY aumenta se a probabilidade do evento diminuir e a odd do BACK também aumenta se a probabilidade diminuir. Se a probabilidade do evento ocorrer aumenta, as odds tanto de LAY como de BACK diminuem pelo fato de ser mais provável de ocorrer.
Handicap Asiático pode devolver apostas se a vantagem for inteira. Handicap Europeu não devolve e possui uma outra lógica de aplicação.

Se o usuário perguntar algo fora desse contexto, diga educadamente que você só pode responder perguntas sobre apostas e trader esportivo.
"""

# Função para gerar respostas com o Gemini
def gerar_resposta(prompt):
    """
    Gera uma resposta usando o modelo Gemini Pro, restringindo o contexto às apostas e trader esportivo.
    """
    prompt_completo = CONTEXTO_APOSTAS + "\n\nUsuário: " + prompt
    try:
        response = model.generate_content(prompt_completo)
        resposta_tratada = response.text.encode('utf-8').decode('utf-8')
        return resposta_tratada
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta: {e}"

def clear_chat_history():
    st.session_state.messages = []


# Interface Streamlit
st.title("Oddly - Especialista em Apostas e Trader Esportivo")
st.write("Pergunte sobre estratégias de apostas, gestão de banca, análise de odds, mercados esportivos, técnicas de trader esportivo e etc.")

# Inicializa o estado da sessão para armazenar o histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico da conversa
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada do usuário
prompt = st.chat_input("Faça sua pergunta sobre apostas ou trader esportivo:")

if st.button("Limpar Histórico"):
    clear_chat_history()
    st.rerun()  # Recarrega o Streamlit para refletir a mudança

if prompt:
    # Adiciona a pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Pensando..."):   
        resposta = gerar_resposta(prompt)
        time.sleep(1)# Gera a resposta do Gemini

    # Adiciona a resposta do Gemini ao histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
