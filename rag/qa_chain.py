# qa_chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL


SYSTEM_PROMPT = """
You are an Enterprise Knowledge Copilot.

Answer the user's question using ONLY the provided context.

Rules:
1. If the answer is not found in the context, say:
   "I don't have enough information in the knowledge base to answer that."
2. Be concise, accurate, and professional.
3. Mention source filenames when relevant.

Context:
{context}
"""


def build_qa_chain(retriever):
    # Check whether API key is loaded from .env
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Make sure your .env file contains:\n"
            "GROQ_API_KEY=your_actual_api_key"
        )

    # Initialize Groq LLM
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0.2,
    )

    # Prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ]
    )

    # Format retrieved documents
    def format_docs(docs):
        if not docs:
            return "No relevant documents found."

        formatted_docs = []
        for doc in docs:
            source = doc.metadata.get("source", "Unknown Source")
            formatted_docs.append(
                f"[Source: {source}]\n{doc.page_content}"
            )

        return "\n\n---\n\n".join(formatted_docs)

    # Main function to answer questions
    def ask(question: str):
        docs = retriever.invoke(question)
        context = format_docs(docs)

        messages = prompt.format_messages(
            context=context,
            question=question,
        )

        response = llm.invoke(messages)

        return {
            "answer": response.content,
            "source_documents": docs,
        }

    return ask