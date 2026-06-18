# Desafio MBA Engenharia de Software com IA - Full Cycle

## Ingestão e Busca Semântica com LangChain e Postgres

Sistema de busca semântica (RAG - Retrieval Augmented Generation) que permite fazer perguntas sobre o conteúdo de um PDF utilizando LangChain, PostgreSQL com pgVector e Google Gemini.

---

## Objetivo

Entregar um software capaz de:

1. **Ingestão**: Ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector
2. **Busca**: Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF

---

## Tecnologias Utilizadas

- **Linguagem**: Python 3.9+
- **Framework**: LangChain
- **Banco de dados**: PostgreSQL + pgVector
- **LLM**: Google Gemini (gemini-2.0-flash)
- **Embeddings**: Google Gemini (gemini-embedding-2)
- **Execução do banco**: Docker & Docker Compose

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.9 ou superior
- Docker e Docker Compose
- Git

---

## Como Executar

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

### 2. Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua API Key do Google:

```env
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_EMBEDDING_MODEL=gemini-embedding-2
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=pdf_embeddings
PDF_PATH=document.pdf
```

**Como obter a API Key do Google Gemini:**
1. Acesse: https://aistudio.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada

### 5. Subir o Banco de Dados

```bash
docker-compose up -d
```

Aguarde alguns segundos para o banco inicializar completamente.

### 6. Executar a Ingestão do PDF

```bash
python src/ingest.py
```

**Saída esperada:**
```
Iniciando processo de ingestão...
Carregando PDF: document.pdf
PDF carregado! Total de páginas: 34
Dividindo documento em chunks...
Documento dividido em 67 chunks
Configurando embeddings com modelo: gemini-embedding-2
Conectando ao banco de dados: postgresql+psycopg://postgres:postgres@localhost:5432/rag
Collection: pdf_embeddings
Chunks salvos no banco vetorial com sucesso!
Total de embeddings gerados: 67
Ingestão concluída!
```

### 7. Executar o Chat

```bash
python src/chat.py
```

**Exemplo de uso:**

```
============================================================
SISTEMA DE BUSCA SEMÂNTICA - RAG com LangChain
============================================================

Sistema pronto para responder perguntas sobre o PDF!
Dica: Digite 'sair' ou 'exit' para encerrar.

============================================================

────────────────────────────────────────────────────────────
Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
────────────────────────────────────────────────────────────

Buscando informações relevantes...

============================================================
RESPOSTA:
============================================================
O faturamento foi de 10 milhões de reais.
============================================================
```

**Exemplo de pergunta fora do contexto:**

```
────────────────────────────────────────────────────────────
Faça sua pergunta: Quantos clientes temos em 2024?
────────────────────────────────────────────────────────────

Buscando informações relevantes...

============================================================
RESPOSTA:
============================================================
Não tenho informações necessárias para responder sua pergunta.
============================================================
```

---

## Estrutura do Projeto

```
├── docker-compose.yml          # Configuração do PostgreSQL com pgVector
├── requirements.txt            # Dependências Python
├── .env.example               # Template de variáveis de ambiente
├── .env                       # Variáveis de ambiente (não versionado)
├── src/
│   ├── ingest.py             # Script de ingestão do PDF
│   ├── search.py             # Script de busca semântica
│   └── chat.py               # CLI para interação com usuário
├── document.pdf              # PDF para ingestão
└── README.md                 # Este arquivo
```

---

## Detalhes Técnicos

### Ingestão (`src/ingest.py`)

1. **Carregamento**: Utiliza `PyPDFLoader` para ler o PDF
2. **Divisão**: `RecursiveCharacterTextSplitter` divide o texto em chunks de 1000 caracteres com overlap de 150
3. **Embeddings**: `GoogleGenerativeAIEmbeddings` gera vetores para cada chunk
4. **Armazenamento**: `PGVector` salva os chunks e vetores no PostgreSQL

### Busca (`src/search.py`)

1. **Vetorização**: Converte a pergunta do usuário em embedding
2. **Busca Semântica**: `similarity_search_with_score` busca os 10 chunks mais relevantes (k=10)
3. **Prompt Engineering**: Monta prompt com contexto e regras rígidas
4. **LLM**: `ChatGoogleGenerativeAI` gera resposta baseada apenas no contexto

### Prompt Template

O sistema utiliza um prompt rigoroso que:
- Responde **apenas** com base no contexto fornecido
- Retorna mensagem padrão quando a informação não está disponível
- Nunca inventa ou usa conhecimento externo
- Não produz opiniões ou interpretações

---

## Gerenciamento do Docker

### Parar o banco de dados:
```bash
docker-compose down
```

### Ver logs do banco:
```bash
docker-compose logs -f postgres
```

### Limpar dados (recomeçar do zero):
```bash
docker-compose down -v
docker-compose up -d
```

---

## Testando o Sistema

### Perguntas que devem funcionar (dentro do contexto do PDF):
- "Qual o faturamento da empresa?"
- "Quais são os principais produtos?"
- "Qual a missão da empresa?"

### Perguntas que devem retornar "Não tenho informações":
- "Qual é a capital da França?"
- "Quantos clientes temos em 2024?"
- "Você acha isso bom ou ruim?"

---

## Dependências Principais

- `langchain` - Framework para aplicações com LLMs
- `langchain-community` - Integrações da comunidade (PyPDFLoader)
- `langchain-google-genai` - Integração com Google Gemini
- `langchain-postgres` - Integração com PostgreSQL
- `langchain-text-splitters` - Divisão de texto em chunks
- `pgvector` - Extensão vetorial para PostgreSQL
- `pypdf` - Leitura de arquivos PDF
- `python-dotenv` - Gerenciamento de variáveis de ambiente

---

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install -r requirements.txt
```

### Erro: "Connection refused" ao conectar no banco
```bash
# Verifique se o Docker está rodando
docker ps

# Reinicie o banco
docker-compose restart
```

### Erro: "Error embedding content: Timeout"
- Verifique sua conexão com a internet
- Confirme se a API Key do Google está correta
- Tente novamente após alguns segundos

### Erro: "insufficient_quota" (OpenAI)
- Este projeto usa Google Gemini, não OpenAI
- Verifique se a variável `GOOGLE_API_KEY` está configurada corretamente

---

## Notas

- O PDF `document.pdf` deve estar na raiz do projeto
- A ingestão precisa ser executada apenas uma vez (ou quando o PDF mudar)
- O banco de dados persiste os dados em um volume Docker
- O sistema usa `temperature=0` para respostas mais consistentes
- Chunks com overlap garantem que informações não sejam cortadas