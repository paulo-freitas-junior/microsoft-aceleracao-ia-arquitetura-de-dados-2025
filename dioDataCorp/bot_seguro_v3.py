# Python versão 3.13

import os
import re
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ========================
# 1) Inicialização segura
# ========================

# Carrega variáveis de ambiente do .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.stop()  # Interrompe o app caso a chave não exista
client = OpenAI(api_key=API_KEY)

# ==========================
# 2) Configuração da página
# ==========================

st.set_page_config(
    page_title="DIO Bot Seguríssimo",
    page_icon="🛡️",
)

st.title("DIO Bot 3.0 — Seguro e com Governança")
st.caption("Este assistente financeiro aplica regras de segurança, validação de entrada e tratamento de erros.")

# ========================
# 3) Regras de governança
# ========================

SAFE_SYSTEM_PROMPT = (
    "Você é um assistente financeiro responsável, objetivo e seguro. "
    "Regras: "
    "1) Não forneça conselhos médicos, legais, violentos, discriminatórios ou instruções perigosas. "
    "2) Não dê recomendações financeiras personalizadas; ofereça informações gerais, riscos e incentive consulta a profissionais. "
    "3) Recuse solicitações que envolvam fraude, hacking, conteúdo adulto explícito, ódio, assédio ou auto/heteroagressão. "
    "4) Seja claro, educado e cite riscos, limitações e pressupostos. "
    "5) Se um pedido for sensível, explique brevemente por que não pode atender e ofereça alternativas seguras (ex: educação financeira geral). "
)

# Palavras/temas a bloquear
BANNED_PATTERNS = [
    r"\b(suicid|autoles|matar|assassin|violênc|explosiv|bomba|hack|phish|fraude)\b",
    r"\b(porn|sexo explícito|conteúdo adulto)\b",
    r"\b(ódio|discriminaç|depreciar grupo)\b",
    r"\b(medicament|diagnóstic|posologia)\b",
]

def is_prompt_allowed(text: str) -> bool:
    """Valida rapidamente entradas com expressões proibidas e tamanho."""
    if not text or not text.strip():
        return False
    if len(text) > 3000:
        return False  # Limita comprimento para evitar abusos
    text_lower = text.lower()
    for pat in BANNED_PATTERNS:
        if re.search(pat, text_lower):
            return False
    return True

def sanitize_response(text: str) -> str:
    """Remoção simples de trechos sensíveis (exemplo)."""
    # Exemplo de neutralização mínima; em produção, use serviços de content safety dedicados
    redactions = [
        (r"(?i)\b(bomba|explosivo|hack)\b", "[conteúdo removido]"),
    ]
    out = text
    for pat, rep in redactions:
        out = re.sub(pat, rep, out)
    return out

# ====================
# 4) Estado de sessão
# ====================

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": SAFE_SYSTEM_PROMPT}
    ]
if "last_interaction_ts" not in st.session_state:
    st.session_state["last_interaction_ts"] = 0.0

# ==========================
# 5) Sidebar com informações
# ==========================

with st.sidebar:
    st.subheader("Controles")
    st.write("• Governança básica ativada")
    st.write("• Validação de entrada e bloqueio de tópicos sensíveis")
    st.write("• Limite de taxa simples por sessão")
    st.divider()
    st.subheader("Dicas de uso")
    st.write("Faça perguntas de educação financeira, planejamento, conceitos e exemplos gerais.")

# ========================
# 6) Exibição do histórico
# ========================

for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# ===================
# 7) Input do usuário
# ===================

prompt = st.chat_input("Digite sua mensagem:")
if prompt:
    # Rate limit simples (1 interação a cada 2 segundos)
    now = time.time()
    if now - st.session_state["last_interaction_ts"] < 2:
        st.warning("Aguarde um instante antes de enviar outra mensagem.")
    else:
        st.session_state["last_interaction_ts"] = now

        # Validação
        if not is_prompt_allowed(prompt):
            st.chat_message("assistant").write(
                "Não posso responder a esse pedido. "
                "Posso ajudar com educação financeira geral, como orçamento, juros, investimentos e riscos."
            )
        else:
            # Exibe a mensagem do usuário e adiciona ao histórico
            st.chat_message("user").write(prompt)
            st.session_state["messages"].append({"role": "user", "content": prompt})

            # ============================================
            # 8) Chamada ao modelo com tratamento de erros
            # ============================================

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=0.4,  # Respostas mais estáveis e seguras
                    messages=st.session_state["messages"],
                    max_tokens=600,
                )
                msg_content = response.choices[0].message.content
                msg_content = sanitize_response(msg_content)

                # Exibe e salva resposta
                st.chat_message("assistant").write(msg_content)
                st.session_state["messages"].append(
                    {"role": "assistant", "content": msg_content}
                )
            except Exception as e:
                st.error("Ocorreu um erro ao processar sua solicitação. Tente novamente.")
                # Opcional: logar o erro de forma segura (não exibir detalhes ao usuário)
                # st.write(str(e))  # Evita expor detalhes técnicos em produção
