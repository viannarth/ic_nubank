import regex
from dotenv import load_dotenv
from utils.config import MATERIAL_TOPICS
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path
import re

# TODO: handle text cleaning in parse_material.py
def clean_markdown(exam:str, chapter:int) -> str:

    md_path = "./src/rag/material/" + exam + "/cap" + str(chapter) + ".md"
    text = Path(md_path).read_text(encoding="utf-8")

    # Remove author logo
    text = re.sub(r"(?i)Logo\s*(?:da\s*)?Rafael\s*Tor[o]?\s*Academia\s*de\s*Finanças(?:\s*logo)?", "", text)
    text = re.sub(r"(?i)Logo\s*(?:da\s*)?Rafael\s*Tor[o]?", "", text)
    text = re.sub(r"(?i)Rafael\s*Tor[o]?\s*Academia\s*de\s*Finanças(?:\s*logo)?", "", text)

    # Remove footer
    footer_pattern = {
        "cpa-10": r"(?i)Apostila\s*2025\s*\d*\s*CPA.*10\s*.*\s*Certificação\s*Profissional\s*ANBIMA\s*Série\s*10\s*\d*",
        "ancord-aai": r"(?i)A[nN][cC][oO][rR][dD].*Agente\s*Autônomo\s*de\s*Investimentos\d*"
    }
    text = re.sub(footer_pattern[exam], "", text)
    
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\u27A2", "", text)

    return text.strip()

def main() -> None:

    # Retrieve HF_TOKEN
    load_dotenv(dotenv_path="./config.env")

    # Toogle the exam
    # exam = "cpa-10"
    exam = "ancord-aai"

    documents = []

    for chapter, topic in MATERIAL_TOPICS[exam].items():
        document_text = clean_markdown(exam, chapter)
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