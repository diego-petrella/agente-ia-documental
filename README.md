# 🤖 Alura Agente IA - Asistente Documental para Santos Pegasus Soluciones

> **Desafío Final - Alura Latam**  
> Un Agente de Inteligencia Artificial basado en Arquitectura RAG (Retrieval-Augmented Generation) capaz de responder preguntas sobre la documentación corporativa en tiempo real.

---

## 📌 Descripción General

**Santos Pegasus Soluciones** es una empresa de tecnología especializada en software escalable y soluciones de IA. Con el crecimiento de la compañía, la documentación interna (manuales de onboarding, guías de arquitectura y políticas) se ha vuelto extensa, lo que dificulta que los nuevos colaboradores encuentren información rápidamente.

Este proyecto implementa un **Agente Inteligente RAG** accesible mediante interfaz web. El usuario realiza preguntas en lenguaje natural y la IA busca los fragmentos más relevantes dentro del **Manual de Onboarding para Nuevos Desarrolladores**, generando respuestas precisas, contextualizadas y sin alucinaciones.

---

## 🏗️ Arquitectura de la Solución

```text
[ Usuario ] ──> ( Interfaz Web Flask )
                      │
                      ▼
             ( Pregunta en NL )
                      │
                      ▼
     [ Búsqueda Semántica Vectorial ]
                      │
    ┌─────────────────┴─────────────────┐
    ▼                                   ▼
[ documento.pdf ] ──> ( Embeddings ) ──> [ FAISS Store ]
                        (MiniLM)          (Top-k Context)
                                                │
                                                ▼
                                    [ Prompt Contextualizado ]
                                                │
                                                ▼
                                     [ Google Gemini 2.5 Flash ]
                                                │
                                                ▼
                                     [ Respuesta al Usuario ]
Ingesta y Embedding: El documento PDF se procesa y fragmenta (RecursiveCharacterTextSplitter). Cada fragmento se convierte en un vector denso usando all-MiniLM-L6-v2 de HuggingFace.

Almacenamiento Vectorial: Los vectores se cargan en un índice FAISS local para realizar búsquedas de similitud semántica a alta velocidad.

Retrieval-Augmented Generation: Al recibir una consulta, la aplicación recupera los fragmentos con mayor relevancia semántica y los inyecta en el prompt del modelo Gemini 2.5 Flash.

Respuesta Contextualizada: El LLM redacta una respuesta clara, estructurada y basada estrictamente en la documentación cargada.

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.10+

Framework Web: Flask

Orquestación RAG: LangChain

Vector Store: FAISS (Facebook AI Similarity Search)

Embeddings: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)

Modelo LLM: Google Gemini 2.5 Flash (ChatGoogleGenerativeAI)

Infraestructura Cloud: Oracle Cloud Infrastructure (OCI Compute Instance)

☁️ Deploy en la Nube (OCI)
La aplicación se encuentra desplegada y funcionando públicamente en una instancia OCI Compute (Ubuntu) en la nube de Oracle.

🌐 Enlace Público de la Aplicación: http://147.15.126.60:5000

💬 Ejemplos de Preguntas y Respuestas de Prueba
1. Pila Tecnológica
Pregunta: ¿Cuáles son las tecnologías principales utilizadas en el Back-end y en el Front-end de la empresa?

Respuesta del Agente:

Las tecnologías principales utilizadas en la empresa son:

Back-end: Java + Spring Boot, PostgreSQL, Kafka, Redis, Docker, Kubernetes, AWS.

Front-end: React 18+ + TypeScript, Next.js, Tailwind CSS, Jest, Cypress.

2. Normas de Git y Workflow
Pregunta: ¿Cuál es el patrón obligatorio para nombrar una branch y cuántas aprobaciones de Code Review se necesitan para hacer merge?

Respuesta del Agente:

El patrón obligatorio para nombrar una branch es: [tipo]/[JIRA-TICKET]-[descripcion-corta-en-kebab-case]. Se necesitan al menos 2 aprobaciones de miembros Senior o Semi-Senior (Pleno) para hacer merge de un Pull Request.

3. Seguridad y Buenas Prácticas
Pregunta: ¿Está permitido usar System.out.println() para hacer debug o hardcodear secretos en el código?

Respuesta del Agente:

No, está estrictamente prohibido usar System.out.println() en código que va al repositorio (se debe utilizar SLF4J con Logback). Asimismo, es una Regla de Oro que NUNCA se deben hardcodear contraseñas, claves de API o tokens en el código, debiendo utilizarse gestores como HashiCorp Vault o AWS Secrets Manager.

4. Beneficios e Integración
Pregunta: ¿Cuáles son las certificaciones técnicas que patrocina la empresa y cómo es la política de horario flexible?

Respuesta del Agente:

Las certificaciones patrocinadas son: AWS Certified Developer – Associate, AWS Certified Solutions Architect, Oracle Certified Professional: Java SE 17 Developer, PSD y CKAD. En cuanto al horario, la empresa establece Core Hours obligatorios de 10:00 a 17:00, siendo el resto de la jornada flexible.

🚀 Instrucciones para Ejecutar Localmente
1. Clonar el repositorio
Bash
git clone [https://github.com/TU_USUARIO/agente-ia-documental.git](https://github.com/TU_USUARIO/agente-ia-documental.git)
cd agente-ia-documental
2. Crear entorno virtual e instalar dependencias
Bash
python3 -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Configurar variables de entorno
Crea un archivo .env en la raíz del proyecto con tu API Key de Google Gemini:

Fragmento de código
GOOGLE_API_KEY=tu_api_key_aqui
4. Ejecutar la aplicación
Bash
python3 app.py
Abre tu navegador e ingresa a http://localhost:5000.


## 📷 Capturas de Pantalla

<img width="1534" height="814" alt="Agente 2" src="https://github.com/user-attachments/assets/0a62824d-caea-4089-a379-d0016fc1f130" />
<img width="1526" height="809" alt="Agente 1" src="https://github.com/user-attachments/assets/6c6ad76c-e001-465c-9acd-0191cebba3c3" />

