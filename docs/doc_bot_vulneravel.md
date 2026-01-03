# Documentação Técnica - DIO Bot Vulnerável v1.0

## Visão Geral

Este documento descreve a implementação de um chatbot financeiro desenvolvido com Streamlit e OpenAI API. A aplicação foi criada para fins educacionais, demonstrando uma implementação **sem mecanismos de governança e segurança**, o que a torna vulnerável a diversos tipos de ataques e uso indevido.

## Informações do Projeto

- **Nome**: DIO Bot Versão 1.0 (sem Governança)
- **Versão**: 1.0
- **Arquivo**: `bot_vulneravel_v1.py`
- **Status**: ⚠️ Vulnerável - Não recomendado para produção

## Dependências

```python
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
```

### Bibliotecas Utilizadas

| Biblioteca | Versão Sugerida | Propósito |
|-----------|----------------|-----------|
| `streamlit` | >= 1.20.0 | Framework para interface web |
| `openai` | >= 1.0.0 | Cliente oficial da API OpenAI |
| `python-dotenv` | >= 0.19.0 | Gerenciamento de variáveis de ambiente |

## Arquitetura do Sistema

### Fluxo de Dados

```
Usuário → Interface Streamlit → Histórico de Sessão → OpenAI API → Resposta → Interface
```

### Componentes Principais

1. **Gerenciamento de Configuração**
2. **Interface de Usuário**
3. **Gerenciamento de Estado**
4. **Integração com OpenAI API**

## Funcionalidades Detalhadas

### 1. Carregamento de Configurações

```python
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

**Descrição**: Carrega as variáveis de ambiente do arquivo `.env` e inicializa o cliente OpenAI.

**Variáveis Necessárias**:
- `OPENAI_API_KEY`: Chave de API da OpenAI

### 2. Configuração da Interface

```python
st.set_page_config(
    page_title="DIO Bot Vulnerável",
    page_icon="⚠️"
)
```

**Descrição**: Define metadados da página web.

**Parâmetros**:
- `page_title`: Título exibido na aba do navegador
- `page_icon`: Emoji de aviso indicando vulnerabilidade

### 3. Elementos Visuais

```python
st.title("Dio Bot Versão 1.0 (sem Governança)")
st.write("Esse assistente **não possui filtros**. Ele responde a qualquer interação")
```

**Descrição**: Renderiza o cabeçalho e aviso sobre a falta de filtros de segurança.

### 4. Gerenciamento de Histórico de Conversação

```python
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Você é um assistente financeiro."}
    ]
```

**Descrição**: Inicializa o histórico de mensagens na sessão do Streamlit.

**Estrutura de Dados**:
```python
[
    {"role": "system", "content": "Prompt do sistema"},
    {"role": "user", "content": "Mensagem do usuário"},
    {"role": "assistant", "content": "Resposta do assistente"}
]
```

### 5. Renderização de Mensagens Anteriores

```python
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])
```

**Descrição**: Exibe todas as mensagens anteriores da conversa, exceto a mensagem de sistema.

### 6. Captura de Input do Usuário

```python
if prompt := st.chat_input("Digite sua mensagem: "):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
```

**Descrição**: Captura a entrada do usuário utilizando o operador walrus (`:=`) e adiciona ao histórico.

### 7. Chamada à API OpenAI

```python
response = client.chat.completion.create(
    model = "gpt-3.5-turbo",
    messages = st.session_state.messages
)
msg_content = response.choices[0].message.content
```

**Descrição**: Envia o histórico completo para a API e extrai a resposta.

**Parâmetros da API**:
- `model`: "gpt-3.5-turbo"
- `messages`: Histórico completo da conversa

### 8. Exibição e Armazenamento da Resposta

```python
st.chat_message("assistant").write(msg_content)
st.session_state.messages.append({"role": "assistant", "content": msg_content})
```

**Descrição**: Mostra a resposta na interface e adiciona ao histórico da sessão.

## Vulnerabilidades Identificadas

### 🔴 Críticas

1. **Ausência de Validação de Input**
   - Não há filtros ou sanitização de entrada
   - Permite prompt injection e manipulação de contexto

2. **Sem Moderação de Conteúdo**
   - Não utiliza OpenAI Moderation API
   - Pode gerar conteúdo inadequado ou perigoso

3. **Exposição de Chave API**
   - Risco se o arquivo `.env` for exposto
   - Sem rotação de chaves implementada

### 🟡 Médias

4. **Ausência de Tratamento de Erros**
   - Sem try-except para falhas de API
   - Experiência ruim se houver problemas de conexão

5. **Sem Limitação de Tokens**
   - Pode gerar custos elevados
   - Histórico cresce indefinidamente na sessão

6. **Sem Rate Limiting**
   - Usuários podem fazer requisições ilimitadas
   - Risco de abuso e custos descontrolados

## Requisitos de Sistema

### Arquivo `.env`

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

### Instalação

```bash
pip install streamlit openai python-dotenv
```

### Execução

```bash
streamlit run bot_vulneravel_v1.py
```

## Melhorias Recomendadas

### Segurança
- Implementar validação de input
- Adicionar OpenAI Moderation API
- Implementar rate limiting
- Adicionar tratamento de erros robusto

### Funcionalidade
- Limitar tamanho do histórico
- Adicionar controle de tokens
- Implementar logs de auditoria
- Adicionar botão de limpar conversa

### Código
- Adicionar type hints
- Implementar constantes para valores fixos

## Conclusão

Este código serve como exemplo educacional de uma implementação **insegura** de chatbot. Ele demonstra os riscos de não implementar mecanismos de governança e segurança adequados. **Não deve ser utilizado em ambiente de produção** sem as devidas correções e implementações de segurança.

---

Créditos de documentação: claude AI usando modelo Sonnet 4.5