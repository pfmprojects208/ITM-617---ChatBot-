import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

def iniciar_rag(ruta_pdf, pregunta_usuario):
    print("1. Leyendo el PDF completo...")
    loader = PyPDFLoader(ruta_pdf)
    documentos = loader.load()

    print("2. Cortando el texto en trozos (Chunking)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200 # Solapamos un poco para no cortar frases a la mitad
    )
    trozos = text_splitter.split_documents(documentos)
    print(f"   -> El PDF se ha dividido en {len(trozos)} trozos.")

    print("3 y 4. Creando base de datos matemática con ChromaDB y Nomic...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    # Esto creará una carpeta oculta '.chroma' en tu proyecto
    vectorstore = Chroma.from_documents(documents=trozos, embedding=embeddings, persist_directory="./.chroma")
    
    # Configuramos el buscador para que traiga los 4 trozos más relevantes
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    print("5. Conectando con Llama 3.1 y pensando la respuesta...\n")
    llm = OllamaLLM(model="llama3.1")

    # Le damos instrucciones estrictas a la IA
    system_prompt = (
        "Eres un asistente experto en analizar documentos. "
        "Usa los siguientes fragmentos de contexto recuperados para responder a la pregunta. "
        "Si no sabes la respuesta o no está en el contexto, di 'No tengo información sobre esto en el documento'. "
        "Responde de forma clara y concisa.\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # Unimos todo: Buscador + IA + Prompt
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # ¡Hacemos la pregunta!
    respuesta = rag_chain.invoke({"input": pregunta_usuario})
    
    print("========================================")
    print("🤖 RESPUESTA DE LA IA:")
    print("========================================")
    print(respuesta["answer"])
    print("========================================")

if __name__ == "__main__":
    # ⚠️ IMPORTANTE: Pon un PDF real tuyo en la carpeta y cambia este nombre
    archivo = "Unknown.pdf" 
    
    mi_pregunta = "Como se llama la estrategia que utilizo GAP?"
    
    iniciar_rag(archivo, mi_pregunta)