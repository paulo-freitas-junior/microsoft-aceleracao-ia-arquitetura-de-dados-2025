# Python versão 3.13

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# 1. Carregar as chaves do arquivo .env

load_dotenv()

# 2. Configurar o cliente OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define título e ícone da página
st.set_page_config(
    page_title="DIO Bot Vulnerável",
    page_icon="⚠️" # https://emojiterra.com/pt/sinal-de-aviso/
)

# Exibe título e descrição na interface
st.title("Dio Bot Versão 1.0 (sem Governança)")
st.write("Esse assistente **não possui filtros**. Ele responde a qualquer interação")

# Histórico da conversa

# Inicializa o histórico de mensagens na sessão
# Define a mensagem de instrução inicial para o modelo
if "messages" not in st.session.state:
    st.session_state["messages"] = [{"role": "system", "content": "Você é um assistente financeiro."}]

# Percorre o histórico e mostra mensagens anteriores
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Captura o Input do usuário
if prompt := st.chat_input("Digite sua mensagem: "):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # CHAMADA DIRETA (PERIGOSA)
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = st.session_state.messages
    )
    msg_content = response.choices[0].message.content

    st.chat_message("assistant").write(msg_content)
    st.session_state.messages.append({"role": "assistant", "content": msg_content})
