from src.baseline.config import MATERIAL_TOPICS
from llama_cloud import LlamaCloud, LlamaCloudError
from dotenv import load_dotenv
from pathlib import Path

def main() -> None:

    # Toogle the exam
    # exam = "cpa-10"
    exam = "ancord-aai"

    # Retrieve the LLAMA_CLOUD_API_KEY from dotenv file
    load_dotenv(dotenv_path="config.env")

    try:
        client = LlamaCloud()
    except LlamaCloudError as err:
        print(err) 

    folder_path = "./data/material/" + exam + "/"
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

            md_path = folder_path + "cap" + str(chapter) + ".md"
            Path(md_path).write_text(result.markdown_full, encoding='utf-8')

        except Exception as err:
            print(f"Could not parse the chapter {chapter}. Error: {err}")
            continue

if __name__ == "__main__":
    main()