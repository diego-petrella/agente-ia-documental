import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template_string
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


load_dotenv()

app = Flask(__name__)

# Nombre de tu archivo PDF
DOC_PATH = os.getenv("DOC_PATH", "politicas_empresa.pdf")
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("Error: No se encontró la variable GOOGLE_API_KEY en el entorno o archivo .env")

def init_rag():
    # Detecta el formato y usa PyPDFLoader para PDFs
    if DOC_PATH.endswith('.pdf'):
        loader = PyPDFLoader(DOC_PATH)
    else:
        loader = TextLoader(DOC_PATH)
        
    docs = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40).split_documents(loader.load())
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY, temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Responde la pregunta basándote únicamente en el siguiente contexto:\n\n{context}\n\nSi no encuentras la respuesta, indica explícitamente que la información no está en el documento."),
        ("human", "{input}")
    ])
    chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, chain)

rag_chain = init_rag()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Agente Consultor IA</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f6f8; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { color: #333; margin-top: 0; }
        input[type="text"] { width: 75%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        #respuesta { margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 Agente Consultor de Documentos</h2>
        <p>Haz preguntas en lenguaje natural sobre las políticas de la empresa:</p>
        <input type="text" id="pregunta" placeholder="Ej: ¿Qué lenguajes usan en el backend?">
        <button onclick="preguntar()">Consultar</button>
        <div id="respuesta">Aún no has hecho ninguna pregunta.</div>
    </div>
    <script>
        async function preguntar() {
            const q = document.getElementById('pregunta').value;
            if(!q) return;
            document.getElementById('respuesta').innerText = "Consultando el documento...";
            const res = await fetch('/api/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({pregunta: q})
            });
            const data = await res.json();
            document.getElementById('respuesta').innerText = data.respuesta;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    pregunta = data.get('pregunta', '')
    res = rag_chain.invoke({"input": pregunta})
    return jsonify({"respuesta": res["answer"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)