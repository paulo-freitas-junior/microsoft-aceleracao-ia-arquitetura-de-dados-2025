# 🛡️ Projeto DIO Bot - Evolução de Governança em IA

## 📋 Visão Geral

Este projeto demonstra a **evolução progressiva de um chatbot financeiro**, desde uma implementação completamente vulnerável até uma versão com governança robusta e múltiplas camadas de segurança. Desenvolvido com Streamlit e OpenAI API, o projeto serve como material educacional sobre boas práticas de segurança em aplicações de IA.

## 🎯 Objetivos do Projeto

- ✅ Demonstrar vulnerabilidades comuns em chatbots sem governança
- ✅ Apresentar técnicas de moderação de conteúdo em múltiplas camadas
- ✅ Ilustrar a importância de logging e observabilidade
- ✅ Fornecer exemplos práticos de implementação segura
- ✅ Educar sobre trade-offs entre simplicidade e segurança

## 📚 Versões Disponíveis

### Versão 1.0 - Bot Vulnerável ⚠️

**Status**: Educacional - Demonstração de vulnerabilidades

A primeira versão demonstra uma implementação **completamente insegura** de um chatbot, sem qualquer mecanismo de governança, validação ou proteção. Criada propositalmente para fins educacionais.

**Características**:
- ❌ Sem validação de entrada
- ❌ Sem moderação de conteúdo
- ❌ Sem tratamento de erros
- ❌ Sem rate limiting
- ❌ Sem logging ou auditoria

**Documentação**: [`doc_bot_vulneravel.md`](/docs/doc_bot_vulneravel.md)

---

### Versão 2.0 - Bot Seguro 🛡️

**Status**: Enterprise - Requer serviços externos

A segunda versão implementa **segurança robusta** utilizando serviços externos premium (Azure Content Safety e Langfuse), oferecendo moderação avançada com IA e observabilidade completa.

**Características**:
- ✅ Moderação dupla camada (Manual + Azure AI)
- ✅ Logging completo com Langfuse
- ✅ Monitoramento em tempo real
- ✅ Rastreabilidade de eventos
- ⚠️ Requer Azure e Langfuse (custos adicionais)
- ⚠️ Sem histórico de conversa

**Documentação**: [`doc_bot_seguro_v2.md`](/docs/doc_bot_seguro_v2.md)

---

### Versão 3.0 - Bot Seguríssimo 🔒

**Status**: Recomendado - Pronto para ambientes controlados

A terceira versão representa a **implementação mais madura**, equilibrando segurança máxima com simplicidade. Não depende de serviços externos complexos, mantém contexto completo da conversa e implementa 6 camadas de proteção.

**Características**:
- ✅ 6 camadas de segurança independentes
- ✅ Histórico completo com contexto
- ✅ Rate limiting implementado
- ✅ System prompt com governança explícita
- ✅ Validação multi-camada via regex
- ✅ Sanitização de output
- ✅ Sem dependências pesadas (apenas Streamlit + OpenAI)
- ✅ Controle de temperatura e tokens

**Documentação**: [`doc_bot_seguro_v3.md`](/docs/doc_bot_seguro_v3.md)

---

## 📊 Comparação Rápida

| Aspecto | v1.0 Vulnerável | v2.0 Seguro | v3.0 Seguríssimo |
|---------|----------------|-------------|------------------|
| **Moderação** | ❌ Nenhuma | ✅ Azure + Manual | ✅ Regex + Prompt |
| **Histórico** | ❌ Sem contexto | ❌ Sem contexto | ✅ Completo |
| **Rate Limiting** | ❌ Não | ❌ Não | ✅ Sim (2s) |
| **Observabilidade** | ❌ Zero | ✅ Langfuse | ⚠️ Básica |
| **Dependências** | Mínimas | Pesadas | ✅ Mínimas |
| **Custos Operacionais** | Baixo | Alto | Baixo |
| **Complexidade** | Simples | Alta | Média |
| **Recomendado para** | Educação | Enterprise | Produção |

## 🚀 Como Usar Este Projeto

### Pré-requisitos

```bash
# Python 3.13+
python --version

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Instalação Base (todas versões)

```bash
pip install streamlit openai python-dotenv
```

### Instalação Adicional para v2.0

```bash
pip install requests azure-ai-contentsafety
```

### Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
# Obrigatório para todas versões
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# Apenas para v2.0
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxxxxxxxxxxx
LANGFUSE_HOST=https://cloud.langfuse.com
AZURE_CONTENT_SAFETY_ENDPOINT=https://xxxxx.cognitiveservices.azure.com/
AZURE_CONTENT_SAFETY_KEY=xxxxxxxxxxxxxxxxxxxxx
```

### Execução

```bash
# Versão 1.0
streamlit run bot_vulneravel_v1.py

# Versão 2.0
streamlit run bot_seguro_v2.py

# Versão 3.0 (Recomendado)
streamlit run bot_seguro_v3.py
```

## 📖 Documentação Completa

Cada versão possui documentação técnica detalhada:

- **[Documentação v1.0](/docs/doc_bot_vulneravel.md)** - Análise de vulnerabilidades
- **[Documentação v2.0](/docs/doc_bot_seguro_v2.md)** - Arquitetura com serviços externos
- **[Documentação v3.0](/docs/doc_bot_seguro_v3.md)** - Implementação autocontida

Cada documento inclui:
- ✓ Arquitetura detalhada do sistema
- ✓ Explicação de cada funcionalidade
- ✓ Análise de segurança
- ✓ Exemplos de uso
- ✓ Melhorias recomendadas
- ✓ Guias de implementação

## 🎓 Conceitos Abordados

### Segurança
- Validação de entrada
- Moderação de conteúdo
- Filtros regex
- System prompts de governança
- Sanitização de output
- Rate limiting

### Observabilidade
- Logging estruturado
- Rastreamento de eventos
- Trace IDs únicos
- Métricas de uso

### Boas Práticas
- Tratamento de erros robusto
- Degradação graceful
- Fail-safe design
- Defense in depth
- Separação de configurações

## 🔍 Casos de Uso

### Versão 1.0
- ✓ Workshops sobre segurança em IA
- ✓ Demonstrações de vulnerabilidades
- ✓ Material didático sobre o que evitar
- ✗ Nunca usar em produção

### Versão 2.0
- ✓ Ambientes enterprise com budget
- ✓ Necessidade de observabilidade avançada
- ✓ Compliance rigoroso
- ✓ Análise forense de conversas
- ⚠️ Requer Azure e Langfuse ativos

### Versão 3.0
- ✓ Startups e pequenas empresas
- ✓ Protótipos e MVPs
- ✓ Ambientes educacionais
- ✓ Assistentes internos de empresa
- ✓ Aplicações com orçamento limitado
- ✓ **Melhor custo-benefício geral**

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão Mínima | Propósito |
|------------|---------------|-----------|
| **Python** | 3.13+ | Linguagem base |
| **Streamlit** | 1.20.0+ | Framework web |
| **OpenAI API** | 1.0.0+ | LLM (GPT-3.5-turbo) |
| **python-dotenv** | 0.19.0+ | Gerenciamento de env vars |
| **Azure Content Safety** | 1.0.0+ | Moderação IA (v2.0) |
| **Langfuse** | - | Observabilidade (v2.0) |
| **Regex** | Built-in | Validação de padrões (v3.0) |

## 📈 Roadmap

### Em Desenvolvimento
- [ ] Versão 4.0 com banco de dados persistente
- [ ] Suporte multi-idioma nos filtros
- [ ] Dashboard de analytics
- [ ] Testes automatizados completos
- [ ] API REST para integração

### Planejado
- [ ] Autenticação de usuários
- [ ] Sistema de plugins
- [ ] Modo offline
- [ ] Mobile app

## 🤝 Contribuições

Este é um projeto educacional. Sugestões de melhorias são bem-vindas!

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## ⚖️ Licença

Este projeto é fornecido para fins educacionais. Ao utilizá-lo em produção, certifique-se de:
- ✓ Revisar e adaptar todas medidas de segurança
- ✓ Implementar logging adequado
- ✓ Realizar testes de segurança
- ✓ Cumprir regulamentações aplicáveis (LGPD, GDPR, etc.)

## 📞 Suporte

Para dúvidas ou problemas:
- 📖 Consulte a documentação específica de cada versão
- 💬 Abra uma issue no repositório
- 📧 Entre em contato com a equipe DIO

## 🎯 Recomendação Final

**Para a maioria dos casos de uso, recomendamos a v3.0** por oferecer:
- ✅ Excelente equilíbrio segurança/simplicidade
- ✅ Baixo custo operacional
- ✅ Fácil manutenção
- ✅ Contexto de conversa completo
- ✅ Sem dependências externas pesadas

---

**Desenvolvido com 🛡️ para demonstrar boas práticas em IA**

*Última atualização: Janeiro 2026*

