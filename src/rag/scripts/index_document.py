import regex
from dotenv import load_dotenv
from utils.config import MATERIAL_TOPICS
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path

def main() -> None:

    # Retrieve HF_TOKEN
    load_dotenv(dotenv_path="./config.env")

    # Toogle the exam
    exam = "ancord-aai"
    # exam = "cpa-10"

    documents:list[Document] = []

    for chapter, topic in MATERIAL_TOPICS[exam].items():
        md_path = "./src/rag/material/" + exam + "/cap" + str(chapter) + ".md"
        document_text = Path(md_path).read_text(encoding="utf-8")
        document = Document(
            text=document_text, 
            metadata={"topic": topic}
        )

        documents.append(document)

    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

    Settings.embed_model = embed_model

    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir = "./index/" + exam)

if __name__ == "__main__":
    main()