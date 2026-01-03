# Python versão 3.13

import os
import time
import datetime
import json
import requests
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

# 1 - Carregando o ambiente

load_dotenv()

st.set_page_config(
    page_title="DioBot V.2 - Seguro",
    page_icon="🛡️",
    layout="wide"
)

# 2 - Configuração das Keys

lf_public = os.getenv("LANGFUSE_PUBLIC_KEY")
lf_secret = os.getenv("LANGFUSE_SECRET_KEY")
lf_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Configurando a Segurança ( Azure )

azure_client = None
try:
    azure_client = ContentSafetyClient(os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"), AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY")))
except: pass

# 3 - BARRA LATERAL

st.sidebar.title ("Monitoramento")
if "logs" not in st.session_state: st.session_state["logs"] = []
for log in st.session_state["logs"]:
    if log["tipo"] == "BLOQUEIO": 
        st.sidebar.error(f"ERRO! {log['msg']}")
    else:
        st.sidebar.success(f"SUCESSO {log['msg']}")

# 4 - FUNÇÕES

def enviar_log_corrigido(input_text, output_text, tags):
    st.sidebar.info("Enviando...")

    # IDs Únicos para tudo

    trace_id = f"trace-{int(time.time()*1000)}-1"
    generation_id = f"gen-{int(time.time()*1000)}-1"

    event_id_trace = f"evt-{int(time.time()*1000)}-1"
    event_id_gen = f"evt-{int(time.time()*1000)}-2"

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    payload = {
        "batch": [
            {
                "id": event_id_trace,
                "type": "trace-create",
                "timestamp": now,
                "body": {
                    "id": trace_id,
                    "name": "CHAT-AULA-FINAL",
                    "userId": "aluno-dio",
                    "timestamp": now,
                    "tags": tags,
                    "input": {"text": input_text},
                    "output": {"text": output_text}
                } 
            },
            {
                "id": event_id_gen,
                "type": "generation-create",
                "timestamp": now,
                "body": {
                    "id": generation_id,
                    "name": "gpt-3.5-turbo",
                    "startTime": now,
                    "endTime": now,
                    "model": "gpt-3.5-turbo",
                    "input": input_text,
                    "output": output_text
                }
            }
        ]
    }

    try:
        r = requests.post(f"{lf_host}/api/public/ingestion", auth=(lf_public, lf_secret), json=payload)
        
        if r.status_code in [200, 201, 207]:
            resp_json = r.json()
            if len(resp_json.get("errors", [])) == 0:
                st.sidebar.success(f"Sucesso! Log Ativado.")
            else:
                # mostra erro exato se ainda houver
                st.sidebar.error(f"Erro interno: {resp_json['errors']}")
        else:
            st.sidebar.error(f"Error HTTP: {r.status_code}")
    except Exception as e:
        st.sidebar.error(f"Erro Conexão: {str(e)}")

# 5 - LÓGICA DO CHAT

st.title("DioBot V2")

if prompt := st.chat_input("Digite a sua mensagem: "):
    st.chat_message("user").write(prompt)

    # Analisa o Risco
    bloqueio = False
    motivo = ""

    # 1. Manual
    if "odeio" in prompt.lower():
        bloqueio, motivo = True, "Violência (Filtro Rápido)"
    
    # 2. Azure
    if not bloqueio and azure_client:
        try:
            res = azure_client.analyze_text(AnalyzeTextOptions(text=prompt))
            for cat in res.categories_analysis:
                if cat.severity > 0: 
                    bloqueio, motivo = True, cat.category
        except: pass

    # Resposta e Log
    
    if bloqueio:
        resp = f"BLOQUEADO: {motivo}"
        st.session_state["logs"].insert(0, {"tipo": "BLOQUEIO", "msg": motivo})
        enviar_log_corrigido(prompt, "BLOQUEADO", ["RISCO", motivo])
    else:
        try:
            full = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user","content":prompt}])
            resp = full.choices[0].message.content
            st.session_state["logs"].insert(0, {"tipo": "SUCESSO", "msg": "Gerado"})
            enviar_log_corrigido(prompt, resp, ["SUCESSO"])
        except: resp = "Erro IA"

    st.chat_message("assistant").write(resp)