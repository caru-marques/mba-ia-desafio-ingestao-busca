import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.messages import HumanMessage

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    """
    Função que realiza busca semântica e retorna resposta baseada no PDF.
    
    Fluxo:
    1. Conecta ao banco vetorial
    2. Busca os 10 chunks mais similares à pergunta
    3. Monta o prompt com o contexto
    4. Chama a LLM para gerar a resposta
    5. Retorna a resposta
    
    Args:
        question (str): Pergunta do usuário
        
    Returns:
        str: Resposta gerada pela LLM baseada no contexto do PDF
    """
    
    try:
        # 1. CONFIGURAR EMBEDDINGS
        embeddings = GoogleGenerativeAIEmbeddings(
            model=GOOGLE_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
        
        # 2. CONECTAR AO BANCO VETORIAL
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
        )
        
        # 3. BUSCAR CHUNKS SIMILARES (k=10)
        results = vectorstore.similarity_search_with_score(question, k=10)
        
        # Extrair apenas o conteúdo dos documentos (ignorar o score)
        context_chunks = [doc.page_content for doc, score in results]
        
        # Concatenar todos os chunks em um único contexto
        contexto = "\n\n".join(context_chunks)
        
        # 4. MONTAR O PROMPT
        prompt = PROMPT_TEMPLATE.format(
            contexto=contexto,
            pergunta=question
        )
        
        # 5. CHAMAR A LLM (Google Gemini)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0,
        )
        
        # Invocar a LLM com o prompt
        response = llm.invoke([HumanMessage(content=prompt)])
        
        # 6. RETORNAR A RESPOSTA
        return response.content
        
    except Exception as e:
        print(f"Erro ao processar pergunta: {e}")
        return "Desculpe, ocorreu um erro ao processar sua pergunta."