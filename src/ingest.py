import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

def ingest_pdf():
    """
    Função principal de ingestão do PDF.
    
    Fluxo:
    1. Carrega o PDF
    2. Divide em chunks
    3. Gera embeddings
    4. Salva no banco vetorial
    """
    
    print("🚀 Iniciando processo de ingestão...")
    
    # 1. CARREGAR O PDF
    print(f"📄 Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"✅ PDF carregado! Total de páginas: {len(documents)}")
    
    # 2. DIVIDIR EM CHUNKS
    print("✂️  Dividindo documento em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Documento dividido em {len(chunks)} chunks")
    
    # 3. CONFIGURAR EMBEDDINGS (Google Gemini)
    print(f"🔧 Configurando embeddings com modelo: {GOOGLE_EMBEDDING_MODEL}")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=GOOGLE_EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY
    )
    
    # 4. CONECTAR AO BANCO E SALVAR
    print(f"💾 Conectando ao banco de dados: {DATABASE_URL}")
    print(f"📦 Collection: {COLLECTION_NAME}")
    
    # PGVector.from_documents cria a tabela (se não existir) e insere os chunks
    vectorstore = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
    )
    
    print("✅ Chunks salvos no banco vetorial com sucesso!")
    print(f"📊 Total de embeddings gerados: {len(chunks)}")
    print("🎉 Ingestão concluída!")


if __name__ == "__main__":
    ingest_pdf()