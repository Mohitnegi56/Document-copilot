from pathlib import Path

import streamlit as st

from config import DOCUMENTS_DIR, GROQ_API_KEY, GROQ_MODEL, RETRIEVAL_K
from rag.pipeline import KnowledgeCopilot


st.set_page_config(
    page_title="Enterprise Knowledge Copilot",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-header { font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; }
    .sub-header { color: #6b7280; margin-bottom: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="main-header">Enterprise Knowledge Copilot</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">RAG pipeline: Documents → FAISS → Groq LLM</p>',
    unsafe_allow_html=True,
)


@st.cache_resource
def get_copilot():
    return KnowledgeCopilot()


def save_uploads(uploaded_files) -> list[Path]:
    saved: list[Path] = []
    for uploaded in uploaded_files:
        dest = DOCUMENTS_DIR / uploaded.name
        dest.write_bytes(uploaded.getvalue())
        saved.append(dest)
    return saved


with st.sidebar:
    st.header("Knowledge Base")
    st.caption(f"LLM: **{GROQ_MODEL}** (Groq)")
    st.caption(f"Retrieval top-k: **{RETRIEVAL_K}**")

    if not GROQ_API_KEY:
        st.error("Set `GROQ_API_KEY` in `.env` (copy from `.env.example`).")
    else:
        st.success("Groq API key loaded")

    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "txt", "md", "docx"],
        accept_multiple_files=True,
    )

    if st.button("Build / Update Index", type="primary", disabled=not uploaded_files):
        copilot = get_copilot()
        with st.spinner("Loading → splitting → embedding → FAISS..."):
            paths = save_uploads(uploaded_files)
            chunk_count = copilot.ingest_paths(paths)
        st.success(f"Indexed **{chunk_count}** chunks from **{len(paths)}** file(s).")
        st.cache_resource.clear()
        st.rerun()

    if st.button("Rebuild from data/documents folder"):
        copilot = get_copilot()
        with st.spinner("Rebuilding index from folder..."):
            chunk_count = copilot.ingest_directory()
        if chunk_count:
            st.success(f"Indexed **{chunk_count}** chunks.")
            st.cache_resource.clear()
            st.rerun()
        else:
            st.warning("No supported files in `data/documents/`.")

    if st.button("Clear index", type="secondary"):
        get_copilot().reset_index()
        st.cache_resource.clear()
        st.info("FAISS index cleared.")
        st.rerun()

    st.divider()
    st.markdown(
        """
        **Pipeline**
        1. Document loader
        2. Text splitter
        3. Embeddings (MiniLM)
        4. FAISS similarity search
        5. Groq LLM answer
        """
    )


copilot = get_copilot()

if not copilot.is_ready:
    st.info(
        "Upload PDF, TXT, MD, or DOCX files in the sidebar and click "
        "**Build / Update Index** to start asking questions."
    )
else:
    st.success("Knowledge base is ready. Ask a question below.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for src in message["sources"]:
                    st.markdown(f"- `{src['file']}` (chunk preview)")
                    st.caption(src["preview"][:300] + "...")

question = st.chat_input("Ask about your documents...")

if question:
    if not GROQ_API_KEY:
        st.error("Configure GROQ_API_KEY before chatting.")
        st.stop()

    if not copilot.is_ready:
        st.warning("Build the index first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving context and generating answer..."):
            try:
                result = copilot.ask(question)
                answer = result["answer"]
                sources = [
                    {
                        "file": doc.metadata.get("source", "unknown"),
                        "preview": doc.page_content,
                    }
                    for doc in result.get("source_documents", [])
                ]
            except Exception as exc:
                answer = f"Error: {exc}"
                sources = []

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for src in sources:
                    st.markdown(f"**{src['file']}**")
                    st.caption(src["preview"][:400])

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
