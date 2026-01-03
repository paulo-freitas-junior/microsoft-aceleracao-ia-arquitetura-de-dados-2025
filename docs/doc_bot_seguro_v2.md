# Documentação Técnica - DIO Bot Seguro v2.0

## Visão Geral

Este documento descreve a implementação de um chatbot com **camadas de segurança e governança**, desenvolvido com Streamlit, OpenAI API, Azure Content Safety e Langfuse. Esta é uma evolução significativa da versão 1.0, incluindo moderação de conteúdo em múltiplas camadas, logging de observabilidade e monitoramento em tempo real.

## Informações do Projeto

- **Nome**: DioBot V.2 - Seguro
- **Versão**: 2.0
- **Arquivo**: `bot_seguro_v2.py`
- **Python**: 3.13
- **Status**: 🛡️ Com Governança e Segurança

## Dependências

```python
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
```

### Bibliotecas Utilizadas

| Biblioteca | Versão Mínima | Propósito |
|-----------|---------------|-----------|
| `streamlit` | >= 1.20.0 | Framework para interface web interativa |
| `openai` | >= 1.0.0 | Cliente oficial da API OpenAI |
| `python-dotenv` | >= 0.19.0 | Gerenciamento de variáveis de ambiente |
| `requests` | >= 2.28.0 | Requisições HTTP para Langfuse |
| `azure-ai-contentsafety` | >= 1.0.0 | Moderação de conteúdo com IA da Microsoft |

### Instalação

```bash
pip install streamlit openai python-dotenv requests azure-ai-contentsafety
```

## Arquitetura do Sistema

### Fluxo de Dados com Governança

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ Input
       ▼
┌─────────────────────┐
│  Filtro Manual      │ ◄─── Camada 1: Palavras-chave
│  (Baixa Latência)   │
└──────┬──────────────┘
       │ ✓ Passou
       ▼
┌─────────────────────┐
│  Azure Content      │ ◄─── Camada 2: IA Avançada
│  Safety Analysis    │      (Hate, Violence, Sexual, Self-Harm)
└──────┬──────────────┘
       │ ✓ Passou
       ▼
┌─────────────────────┐
│  OpenAI API         │ ◄─── Geração de Resposta
│  (GPT-3.5-turbo)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Langfuse Logging   │ ◄─── Observabilidade
│  (Trace + Events)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Resposta ao        │
│  Usuário            │
└─────────────────────┘
```

### Componentes Principais

1. **Sistema de Moderação Multi-Camadas**
2. **Plataforma de Observabilidade (Langfuse)**
3. **Interface com Monitoramento em Tempo Real**
4. **Integração Segura com Múltiplas APIs**

## Configuração Inicial

### 1. Variáveis de Ambiente (`.env`)

```env
# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# Langfuse (Observabilidade)
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxxxxxxxxxxx
LANGFUSE_HOST=https://cloud.langfuse.com

# Azure Content Safety
AZURE_CONTENT_SAFETY_ENDPOINT=https://xxxxx.cognitiveservices.azure.com/
AZURE_CONTENT_SAFETY_KEY=xxxxxxxxxxxxxxxxxxxxx
```

### 2. Carregamento e Configuração da Interface

```python
load_dotenv()

st.set_page_config(
    page_title="DioBot V.2 - Seguro",
    page_icon="🛡️",
    layout="wide"
)
```

**Descrição**: Carrega as variáveis de ambiente e configura a página Streamlit com layout expandido para melhor visualização dos logs de monitoramento.

**Parâmetros**:
- `page_title`: Define o título na aba do navegador
- `page_icon`: Ícone de escudo 🛡️ indicando segurança
- `layout`: "wide" para utilizar toda largura da tela

### 3. Inicialização de Clientes

#### Cliente OpenAI

```python
lf_public = os.getenv("LANGFUSE_PUBLIC_KEY")
lf_secret = os.getenv("LANGFUSE_SECRET_KEY")
lf_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

**Descrição**: Configura as credenciais para OpenAI e Langfuse.

**Observações**:
- Langfuse é uma plataforma de observabilidade para LLMs
- Permite rastreamento completo de conversas
- O host possui fallback para o cloud da Langfuse

#### Cliente Azure Content Safety

```python
azure_client = None
try:
    azure_client = ContentSafetyClient(
        os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"), 
        AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY"))
    )
except: 
    pass
```

**Descrição**: Inicializa o cliente Azure Content Safety com tratamento de erro gracioso.

**Comportamento**:
- Se as credenciais estiverem ausentes ou inválidas, `azure_client` permanece `None`
- O sistema continua funcionando apenas com filtro manual
- Não interrompe a aplicação por falta de Azure

**Estratégia**: Degradação graceful - o bot continua operacional sem moderação Azure

## Painel de Monitoramento

### Sidebar de Logs em Tempo Real

```python
st.sidebar.title("Monitoramento")
if "logs" not in st.session_state: 
    st.session_state["logs"] = []

for log in st.session_state["logs"]:
    if log["tipo"] == "BLOQUEIO": 
        st.sidebar.error(f"ERRO! {log['msg']}")
    else:
        st.sidebar.success(f"SUCESSO {log['msg']}")
```

**Descrição**: Cria um painel lateral que exibe o histórico de eventos em tempo real.

**Estrutura de Log**:
```python
{
    "tipo": "BLOQUEIO" | "SUCESSO",
    "msg": "Descrição do evento ou categoria de risco"
}
```

**Visualização**:
- **Eventos BLOQUEIO**: Exibidos em vermelho com ícone de erro
- **Eventos SUCESSO**: Exibidos em verde com ícone de sucesso
- Logs mais recentes aparecem no topo (insert na posição 0)

**Persistência**: Os logs são mantidos durante toda a sessão do usuário

## Sistema de Logging - Langfuse

### Função Principal: `enviar_log_corrigido()`

```python
def enviar_log_corrigido(input_text, output_text, tags):
    st.sidebar.info("Enviando...")
    # [Lógica de logging]
```

**Parâmetros**:
- `input_text`: Mensagem enviada pelo usuário
- `output_text`: Resposta gerada ou "BLOQUEADO"
- `tags`: Lista de tags para categorização (ex: ["SUCESSO"], ["RISCO", "Violence"])

### Geração de Identificadores Únicos

```python
trace_id = f"trace-{int(time.time()*1000)}-1"
generation_id = f"gen-{int(time.time()*1000)}-1"
event_id_trace = f"evt-{int(time.time()*1000)}-1"
event_id_gen = f"evt-{int(time.time()*1000)}-2"
```

**Descrição**: Cria IDs únicos baseados em timestamp em milissegundos.

**Formato**:
- `trace-{timestamp}-1`: Identifica toda a conversa/trace
- `gen-{timestamp}-1`: Identifica a geração específica
- `evt-{timestamp}-1`: ID do evento de criação de trace
- `evt-{timestamp}-2`: ID do evento de criação de generation

**Timestamp**:
```python
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
```
Gera timestamp ISO 8601 em UTC (ex: `2026-01-03T15:30:45.123456+00:00`)

### Estrutura do Payload Langfuse

```python
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
```

**Componentes do Payload**:

1. **Trace (Rastreamento)**:
   - Representa a conversa completa
   - Contém input e output textuais
   - Associado a um userId
   - Possui tags para categorização

2. **Generation (Geração)**:
   - Representa a chamada específica ao modelo
   - Registra modelo utilizado
   - Marca tempos de início e fim
   - Útil para análise de performance

### Envio e Tratamento de Resposta

```python
try:
    r = requests.post(
        f"{lf_host}/api/public/ingestion",
        auth=(lf_public, lf_secret),
        json=payload
    )
    
    if r.status_code in [200, 201, 207]:
        resp_json = r.json()
        if len(resp_json.get("errors", [])) == 0:
            st.sidebar.success(f"Sucesso! Log Ativado.")
        else:
            st.sidebar.error(f"Erro interno: {resp_json['errors']}")
    else:
        st.sidebar.error(f"Error HTTP: {r.status_code}")
except Exception as e:
    st.sidebar.error(f"Erro Conexão: {str(e)}")
```

**Autenticação**: Basic Auth usando chaves pública e secreta

**Status Codes Aceitos**:
- **200 OK**: Requisição bem-sucedida
- **201 Created**: Recurso criado com sucesso
- **207 Multi-Status**: Sucesso parcial (alguns eventos processados)

**Tratamento de Erros**:
1. Verifica status code da resposta
2. Analisa JSON de resposta em busca de erros internos
3. Exibe feedback visual na sidebar
4. Captura exceções de conexão

## Sistema de Moderação Multi-Camadas

### Camada 1: Filtro Manual Rápido

```python
bloqueio = False
motivo = ""

if "odeio" in prompt.lower():
    bloqueio, motivo = True, "Violência (Filtro Rápido)"
```

**Descrição**: Primeira linha de defesa com verificação imediata de palavras-chave perigosas.

**Características**:
- **Latência**: < 1ms (verificação em memória)
- **Customizável**: Fácil adicionar mais palavras
- **Case-insensitive**: Converte para minúsculas antes de verificar
- **Propósito**: Bloquear conteúdo obviamente problemático sem custos de API

**Exemplo de Expansão**:
```python
palavras_bloqueadas = ["odeio", "matar", "violência", "terrorismo"]
if any(palavra in prompt.lower() for palavra in palavras_bloqueadas):
    bloqueio, motivo = True, "Violência (Filtro Rápido)"
```

### Camada 2: Azure Content Safety

```python
if not bloqueio and azure_client:
    try:
        res = azure_client.analyze_text(AnalyzeTextOptions(text=prompt))
        for cat in res.categories_analysis:
            if cat.severity > 0: 
                bloqueio, motivo = True, cat.category
    except: 
        pass
```

**Descrição**: Análise avançada usando IA da Microsoft Azure.

**Funcionamento**:
- Só executa se o filtro manual não bloqueou
- Só executa se `azure_client` foi inicializado com sucesso
- Analisa múltiplas categorias de risco simultaneamente

**Categorias Analisadas pelo Azure**:

| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| **Hate** | Discurso de ódio | Ataques baseados em raça, religião, gênero |
| **Violence** | Conteúdo violento | Descrições de violência física, ameaças |
| **Sexual** | Conteúdo sexual | Conteúdo adulto, exploração |
| **SelfHarm** | Auto-mutilação | Suicídio, lesões auto-infligidas |

**Níveis de Severidade**:
- **0**: Seguro (não bloqueado)
- **1-2**: Baixo risco
- **3-4**: Risco médio
- **5-6**: Alto risco

**Comportamento**: Qualquer severidade > 0 resulta em bloqueio nesta implementação

**Tratamento de Erros**: Falhas na API Azure são silenciadas - o sistema continua sem moderação Azure

## Lógica Principal do Chat

### Fluxo Completo de Interação

```python
st.title("DioBot V2")

if prompt := st.chat_input("Digite a sua mensagem: "):
    st.chat_message("user").write(prompt)
    
    # [Sistema de moderação executado]
    
    if bloqueio:
        # Cenário 1: Conteúdo Bloqueado
        resp = f"BLOQUEADO: {motivo}"
        st.session_state["logs"].insert(0, {
            "tipo": "BLOQUEIO", 
            "msg": motivo
        })
        enviar_log_corrigido(prompt, "BLOQUEADO", ["RISCO", motivo])
    else:
        # Cenário 2: Conteúdo Aprovado
        try:
            full = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user","content":prompt}]
            )
            resp = full.choices[0].message.content
            st.session_state["logs"].insert(0, {
                "tipo": "SUCESSO", 
                "msg": "Gerado"
            })
            enviar_log_corrigido(prompt, resp, ["SUCESSO"])
        except: 
            resp = "Erro IA"
    
    st.chat_message("assistant").write(resp)
```

### Cenário 1: Conteúdo Bloqueado

**Quando Ocorre**:
- Filtro manual detectou palavra-chave
- Azure Content Safety identificou risco

**Ações Executadas**:
1. Cria mensagem de bloqueio com motivo
2. Adiciona log de BLOQUEIO na sessão
3. Envia evento para Langfuse com tags ["RISCO", categoria]
4. Exibe mensagem de bloqueio ao usuário

**Exemplo de Resposta**:
```
BLOQUEADO: Violência (Filtro Rápido)
```

### Cenário 2: Conteúdo Aprovado

**Quando Ocorre**:
- Passou por todas camadas de moderação

**Ações Executadas**:
1. Envia prompt para OpenAI API
2. Extrai resposta do modelo
3. Adiciona log de SUCESSO na sessão
4. Envia evento para Langfuse com tag ["SUCESSO"]
5. Exibe resposta ao usuário

**Tratamento de Erro**:
- Se OpenAI falhar, exibe "Erro IA"
- Não interrompe a aplicação

### Características da Chamada OpenAI

```python
full = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"user","content":prompt}]
)
```

**Observações**:
- **Sem histórico**: Cada mensagem é independente
- **Sem system message**: Não há instruções de comportamento
- **Modelo fixo**: Sempre usa GPT-3.5-turbo
- **Sem parâmetros**: Usa defaults (temperature, max_tokens, etc.)

## Matriz de Decisão de Segurança

| Filtro Manual | Azure Safety | Azure Disponível | Ação Final | Tags Langfuse |
|---------------|--------------|------------------|------------|---------------|
| ❌ Bloqueado | - | - | **BLOQUEAR** | ["RISCO", "Violência (Filtro Rápido)"] |
| ✅ Passou | ❌ Bloqueado | ✅ Sim | **BLOQUEAR** | ["RISCO", categoria_azure] |
| ✅ Passou | ✅ Passou | ✅ Sim | **PROCESSAR** | ["SUCESSO"] |
| ✅ Passou | - | ❌ Não | **PROCESSAR** | ["SUCESSO"] |

## Comparação: v1.0 vs v2.0

| Aspecto | v1.0 (Vulnerável) | v2.0 (Seguro) |
|---------|-------------------|---------------|
| **Moderação de Conteúdo** | ❌ Nenhuma | ✅ Dupla camada (Manual + Azure) |
| **Logging/Observabilidade** | ❌ Ausente | ✅ Langfuse completo |
| **Tratamento de Erros** | ❌ Mínimo | ✅ Try-catch implementado |
| **Monitoramento Visual** | ❌ Não possui | ✅ Sidebar com logs em tempo real |
| **Filtros de Segurança** | ❌ Zero | ✅ 2 camadas independentes |
| **Rastreabilidade** | ❌ Impossível | ✅ Trace IDs únicos |
| **Layout** | Padrão (estreito) | ✅ Wide com monitoramento |
| **Degradação Graceful** | ❌ Falhas quebram app | ✅ Continua sem Azure se indisponível |
| **Auditoria** | ❌ Impossível | ✅ Todos eventos registrados |
| **Custo de Operação** | Baixo | Médio (Azure + Langfuse) |

## Melhorias Implementadas da v1.0 para v2.0

### ✅ Segurança

1. **Filtro manual** para bloqueio instantâneo de palavras-chave
2. **Azure Content Safety** para análise avançada com IA
3. **Sistema de bloqueio** com feedback claro ao usuário
4. **Registro de eventos de risco** para auditoria

### ✅ Observabilidade

1. **Integração com Langfuse** para rastreamento completo
2. **Trace IDs únicos** para cada interação
3. **Tags personalizadas** (SUCESSO, RISCO + categorias)
4. **Registro de input/output** para análise posterior
5. **Timestamps UTC** para correlação temporal

### ✅ Experiência do Usuário

1. **Monitoramento em tempo real** na sidebar
2. **Feedback visual** diferenciado (vermelho/verde)
3. **Layout expandido** para melhor visualização
4. **Mensagens descritivas** sobre motivos de bloqueio

### ✅ Resiliência

1. **Degradação graceful** se Azure estiver indisponível
2. **Try-catch** em chamadas críticas
3. **Fallback** para erro genérico em falhas da OpenAI

## Limitações Conhecidas

### Funcionais

1. **Sem histórico de conversa**: Cada mensagem é tratada isoladamente
2. **Filtro manual limitado**: Apenas uma palavra-chave
3. **Sem contexto**: Bot não mantém contexto entre mensagens
4. **Bloqueio binário**: Não há níveis de alerta, apenas bloqueia ou permite

### Técnicas

1. **IDs baseados em timestamp**: Possíveis colisões em requisições simultâneas
2. **Sem rate limiting**: Usuários podem enviar requisições ilimitadas
3. **Modelo hardcoded**: GPT-3.5-turbo fixo, não configurável
4. **Sem retry logic**: Falhas de API não são retentadas
5. **Análise síncrona**: Azure bloqueia a thread durante análise

### Segurança

1. **Severidade Azure > 0 bloqueia tudo**: Pode ser muito restritivo
2. **Sem whitelist**: Usuários confiáveis têm mesmas restrições
3. **Logs sem sanitização**: Input malicioso pode aparecer nos logs
4. **Sem proteção contra prompt injection**: Usuário pode tentar manipular

### Custos

1. **Chamadas Azure**: Custo por análise de texto
2. **Chamadas OpenAI**: Sem limite de tokens
3. **Langfuse**: Custo por evento registrado
4. **Sem budget controls**: Pode gerar custos inesperados

## Melhorias Futuras Recomendadas

### 🔴 Alta Prioridade

1. **Corrigir erros de sintaxe** (OpenAi → OpenAI, sucess → success)
2. **Implementar histórico de conversa** com context window
3. **Adicionar rate limiting** por usuário/IP
4. **Usar UUID** para IDs em vez de timestamp
5. **Expandir filtro manual** com lista configurável de palavras

### 🟡 Média Prioridade

6. **Configurar níveis de severidade Azure** (não bloquear tudo > 0)
7. **Adicionar cache** para respostas comuns
8. **Implementar retry logic** com backoff exponencial
9. **Criar dashboard** de métricas no Langfuse
10. **Adicionar timeout** nas chamadas de API
11. **Implementar circuit breaker** para Azure

### 🟢 Baixa Prioridade

12. **Suporte multi-idioma** nos filtros
13. **Sistema de feedback** do usuário
14. **Testes automatizados** de segurança
15. **Whitelist** para usuários confiáveis
16. **Análise assíncrona** para melhor performance
17. **Modo debug** com logs detalhados

## Arquitetura de Defesa em Profundidade

### Camadas de Proteção

```
┌─────────────────────────────────────────┐
│ Camada 1: Filtro Manual (< 1ms)         │
│ - Verificação rápida de palavras-chave  │
│ - Zero custo                             │
│ - Customizável                           │
└────────────────┬────────────────────────┘
                 │ ✓ Passou
                 ▼
┌─────────────────────────────────────────┐
│ Camada 2: Azure Content Safety (100-300ms)│
│ - Análise com IA avançada                │
│ - Múltiplas categorias                   │
│ - Custo por requisição                   │
└────────────────┬────────────────────────┘
                 │ ✓ Passou
                 ▼
┌─────────────────────────────────────────┐
│ Camada 3: OpenAI API                     │
│ - Moderação interna da OpenAI            │
│ - Geração de resposta                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Camada 4: Logging & Auditoria           │
│ - Registro completo no Langfuse          │
│ - Rastreabilidade total                  │
└─────────────────────────────────────────┘
```

### Princípios de Segurança Aplicados

1. **Defense in Depth**: Múltiplas camadas independentes
2. **Fail-Safe**: Sistema continua mesmo se Azure falhar
3. **Least Privilege**: Apenas permissões necessárias
4. **Auditability**: Todos eventos são registrados
5. **Transparency**: Usuário sabe quando/por que foi bloqueado

## Métricas e Observabilidade

### Dados Rastreados no Langfuse

| Métrica | Descrição | Uso |
|---------|-----------|-----|
| **Input Text** | Mensagem do usuário | Análise de padrões |
| **Output Text** | Resposta ou "BLOQUEADO" | Auditoria |
| **Tags** | Categorização do evento | Filtros e relatórios |
| **Timestamps** | Momento exato do evento | Análise temporal |
| **Trace ID** | Identificador único | Rastreamento |
| **User ID** | Identificador do usuário | Análise por usuário |
| **Model** | Modelo utilizado | Análise de custos |

### Casos de Uso da Observabilidade

1. **Auditoria de Segurança**: Revisar todos bloqueios
2. **Análise de Padrões**: Identificar tentativas de abuse
3. **Melhoria de Filtros**: Ver falsos positivos/negativos
4. **Controle de Custos**: Monitorar uso de APIs
5. **Performance**: Identificar gargalos
6. **Compliance**: Demonstrar conformidade com políticas

## Execução da Aplicação

### Pré-requisitos

1. Python 3.13 instalado
2. Arquivo `.env` configurado com todas as chaves
3. Conta Langfuse (pode ser free tier)
4. Conta Azure com Content Safety habilitado
5. Chave OpenAI válida

### Comando de Execução

```bash
# Instalar dependências
pip install streamlit openai python-dotenv requests azure-ai-contentsafety

# Executar aplicação
streamlit run bot_seguro_v2.py
```

### Acesso

- **URL Local**: http://localhost:8501
- **Porta Padrão**: 8501
- **Hot Reload**: Automático ao salvar alterações

## Considerações de Produção

### ⚠️ Não Recomendado para Produção Sem:

1. **Implementação de rate limiting**
2. **Uso de UUIDs reais** para IDs únicos
3. **Sistema de autenticação** de usuários
4. **Logs estruturados** (JSON) para análise
5. **Monitoramento de saúde** das APIs
6. **Alertas automáticos** para falhas
7. **Testes automatizados** de segurança
8. **Documentação de incidentes**
9. **Plan B** se Langfuse estiver indisponível

### ✅ Adequado Para:

- Ambientes de desenvolvimento
- Provas de conceito (POC)
- Demonstrações educacionais
- Testes de governança de IA
- Laboratórios de segurança

## Conclusão

A versão 2.0 representa um **avanço significativo** em segurança e governança comparada à v1.0 vulnerável. Com **dupla camada de moderação**, **logging completo** e **monitoramento em tempo real**, o bot demonstra boas práticas de governança de IA.

### Pontos Fortes

- ✅ Arquitetura de segurança em camadas
- ✅ Observabilidade completa com Langfuse
- ✅ Degradação graceful em falhas
- ✅ Feedback claro ao usuário
- ✅ Auditoria de todas interações

### Pontos de Atenção

- ⚠️ Sem histórico de conversa
- ⚠️ Sem controle de custos
- ⚠️ IDs únicos podem colidir
- ⚠️ Filtro manual muito limitado

### Status Final

🛡️ Arquitetura Segura | ⚠️ Requer Correções Sintáticas | 📊 Observabilidade Completa

---

Documentação: Claude AI - Sonnet 4.5