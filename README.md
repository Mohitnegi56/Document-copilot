## Enterprise Knowledge Copilot 🧠

A production-ready Retrieval-Augmented Generation (RAG) application that allows users to upload enterprise documents and ask natural language questions. The system retrieves relevant document chunks using FAISS and generates accurate answers with Groq LLMs via LangChain.

## 🚀 Features
📄 Upload and index PDF, DOCX, TXT, and Markdown files
✂️ Automatic document chunking with configurable overlap
🔎 Semantic search using Sentence Transformers
🗂️ Vector storage with FAISS
🤖 Answer generation using Groq LLMs
📚 Displays source documents used to generate answers
💾 Persistent FAISS index saved to disk
🌐 Interactive web interface built with Streamlit
🔐 Environment-based configuration using .env

## 🌐 Live Demo
Try the application here: https://document-copilot-iuapphdsyiwqpsjksjuaj5q.streamlit.app/

## 🏗️ Architecture
Documents
   ↓
Document Loader
   ↓
Text Splitter
   ↓
Embeddings (MiniLM)
   ↓
FAISS Vector Store
   ↓
Retriever (Top-K Similarity Search)
   ↓
Groq LLM
   ↓
Answer + Source Citations

## 🛠️ Tech Stack
Python 3.10+
LangChain
FAISS
Sentence Transformers
Groq API
Streamlit
Python Dotenv

## 📂 Project Structure
```
Enterprise-Knowledge-Copilot/
│── app.py
│── config.py
│── requirements.txt
│── .env
│── README.md
│
├── rag/
│   │── __init__.py
│   │── document_loader.py
│   │── embeddings.py
│   │── pipeline.py
│   │── qa_chain.py
│   │── text_splitter.py
│   │── vector_store.py
│
├── data/
│   └── documents/
│
└── storage/
    └── faiss_index/
```
## ⚙️ Installation
1. Clone the Repository
```
git clone https://github.com/your-username/enterprise-knowledge-copilot.git
cd enterprise-knowledge-copilot
```
2. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```
3. Install Dependencies
```
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a .env file in the project root:
```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```
Get your Groq API key from:
```
https://console.groq.com/keys
```

▶️ Run the Application
```
streamlit run app.py
```
📖 Usage
Launch the Streamlit app.

Upload one or more documents.
Click Build / Update Index.
Ask questions in natural language.
View answers along with source document excerpts.
Example Questions
What is the leave policy?
Summarize this document.
What are the key terms in the agreement?
What technologies are mentioned?

🔘 Sidebar Controls
Build / Update Index
Indexes the uploaded documents and adds them to the existing knowledge base.
Rebuild from data/documents
Recreates the vector index from all files stored in the documents folder.
Clear Index
Deletes the existing FAISS index and resets the knowledge base.

## 🧠 How It Works
# Document Loading
Documents are loaded using specialized loaders:
PDF → PyPDFLoader
DOCX → Docx2txtLoader
TXT/MD → TextLoader
# Text Splitting
Documents are divided into overlapping chunks using RecursiveCharacterTextSplitter.
# Embeddings
Each chunk is converted into vector embeddings using:
sentence-transformers/all-MiniLM-L6-v2
# Vector Storage
Embeddings are stored in a persistent FAISS index.
# Retrieval
Top-K similar chunks are retrieved for each user question.
# Answer Generation
Retrieved context is sent to a Groq-hosted LLM with a strict prompt instructing it to answer only from the provided context.

## 📦 Supported File Types
PDF (.pdf)
Word Documents (.docx)
Text Files (.txt)
Markdown (.md)

## 🧪 Example Workflow
```
Upload employee_handbook.pdf
       ↓
Build / Update Index
       ↓
Ask: "How many paid leaves are allowed?"
       ↓
Retriever finds relevant chunks
       ↓
Groq LLM generates answer
       ↓
Displays answer with source citations
```
## 📝 Resume Description
Enterprise Knowledge Copilot (RAG)
Developed a document question-answering system using LangChain, FAISS, and Groq LLMs. Implemented document ingestion, chunking, embeddings, semantic retrieval, and a Streamlit-based interface to answer questions from enterprise documents with source citations.

## 🔮 Future Enhancements
Conversation memory
Hybrid search (BM25 + vector search)
OCR support for scanned PDFs
User authentication
Role-based document access
Docker deployment
Evaluation metrics (RAGAS)

## 📄 License
This project is licensed under the MIT License.

## 🙌 Acknowledgements
LangChain
FAISS
Groq
Streamlit
Sentence Transformers
