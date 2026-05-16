"""CLI: build index and ask a question."""

import sys

from rag.pipeline import KnowledgeCopilot


def main():
    copilot = KnowledgeCopilot()
    if len(sys.argv) > 1 and sys.argv[1] == "index":
        count = copilot.ingest_directory()
        print(f"Indexed {count} chunks.")
        return

    if not copilot.is_ready:
        count = copilot.ingest_directory()
        if count == 0:
            print("No documents found. Add files to data/documents/ or run: python run.py index")
            sys.exit(1)
        print(f"Indexed {count} chunks.")

    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Question: ")
    result = copilot.ask(question)
    print("\nAnswer:\n", result["answer"])
    print("\nSources:", [d.metadata.get("source") for d in result["source_documents"]])


if __name__ == "__main__":
    main()
