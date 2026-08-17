from src.utils.config import MATERIAL_TOPICS
from llama_cloud import LlamaCloud, LlamaCloudError
from dotenv import load_dotenv
from pathlib import Path
import re

def clean_markdown(text: str, exam:str) -> str:

    # Remove author logo
    text = re.sub(r"(?i)Logo\s*(?:da\s*)?Rafael\s*Tor[o]?\s*Academia\s*de\s*Finanças(?:\s*logo)?", "", text)
    text = re.sub(r"(?i)Logo\s*(?:da\s*)?Rafael\s*Tor[o]?", "", text)
    text = re.sub(r"(?i)Rafael\s*Tor[o]?\s*Academia\s*de\s*Finanças(?:\s*logo)?", "", text)
    text = re.sub(r"(?i)Logo\s*(?:da\s*)?\s*Academia\s*de\s*Finanças(?:\s*logo)?", "", text)
    text = re.sub(r"(?i)Rafael\s*Tor[o]?\s*", "", text)
    text = re.sub(r"(?i)A[Cc][Aa][Dd][Ee][Mm][Ii][Aa]\s*[Dd][Ee]\s*F[Ii][Nn][Aa][Nn][Çç][Aa][Ss](?:\s*logo)?", "", text)
    text = re.sub(r"(?i)Logo\s*", "", text)

    # Remove footer
    footer_pattern = {
        "cpa-10": r"(?i)Apostila\s*2025\s*\d*\s*\d*\s*(?:CPA.*10\s*)?.*(?:\s*Certificação\s*Profissional\s*ANBIMA\s*Série\s*10)?\s*\d*",
        "ancord-aai": r"(?i)A[nN][cC][oO][rR][dD].*(?:Agente\s*Autônomo)?(?:Assessor)?\s*de\s*Inves[ti]*mentos\s*\d*"
    }
    text = re.sub(footer_pattern[exam], "", text)
    
    # Remove blocks of blank lines and unwanted characters
    text = re.sub(r"\n\s*\d+\s*[\n]*", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\n---\n", "", text)

    return text.strip()


def main() -> None: 

    # Toogle the exam
    # exam = "ancord-aai"
    exam = "cpa-10"
    
    # Retrieve the LLAMA_CLOUD_API_KEY from dotenv file
    load_dotenv(dotenv_path="config.env")

    try:
        client = LlamaCloud()
    except LlamaCloudError as err:
        print(err)

    folder_path = "./src/rag/material/" + exam + "/"
    for chapter in MATERIAL_TOPICS[exam]:
        chapter_path = folder_path + "raw/cap" + str(chapter) + ".pdf"
        file = client.files.create(file=chapter_path, purpose="parse")

        try: 
            result = client.parsing.parse(
                file_id=file.id,
                tier="cost_effective",
                version="latest",
                verbose=True,
                processing_options={
                    "ignore": {"ignore_diagonal_text": True, "ignore_text_in_image": True}
                },
                expand=["markdown_full"]
            )

        except Exception as response_err:
            print(f"Could not parse the chapter {chapter}. Error: {response_err}")
            continue

        try: 
            md_text:str = result.markdown_full
            clean_md_text = clean_markdown(md_text, exam)

            md_path = folder_path + "cap" + str(chapter) + ".md"
            Path(md_path).write_text(clean_md_text, encoding='utf-8')
            
        except Exception as write_err: 
            print(f"Could not save the chapter {chapter}. Error: {write_err}")
            continue

if __name__ == "__main__":
    main()