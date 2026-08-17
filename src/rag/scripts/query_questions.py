from src.utils.config import EXAMS
from src.utils.files import create_answers_json
from src.rag.prompt import generate_prompts
from src.rag.response_format import Answer, json_from_answer
import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def main() -> None:

    # Retrieve HF_TOKEN
    load_dotenv(dotenv_path="./config.env")

    # Toogle the exam
    exam = "ancord-aai"
    # exam = "cpa-10"

    # Same model used to index the documents
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

    # Certify ollama model is running on port 11434
    llm = Ollama(model="llama3.1:latest", request_timeout=120.0)
    sllm = llm.as_structured_llm(Answer)

    storage_context = StorageContext.from_defaults(persist_dir="./src/rag/index/"+exam)
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine(llm=sllm)

    test_numbers = EXAMS[exam]["test_numbers"]
    
    for test_number in test_numbers:

        outputs:list[str] = []
        has_errors = False

        prompts = generate_prompts(exam, test_number)

        for question_number, prompt in prompts.items():

            try:
                response = query_engine.query(prompt)
                response_str = str(response)
                print(f"Response of question {question_number} of test {test_number}:\n{response_str}")

                json_response = json_from_answer(response_str, question_number)
                outputs.append(json_response)

            except Exception as err:
                has_errors = True
                print(f"Could not query the response for the test {test_number} for the question {question_number}. Error: {err}")

                # If a model could not generate the answers for one chunk of a test,
                # all the answers for the further chunks will be useless.
                break

        # If there was an error, continue to the next test
        if has_errors:
            continue

        try:
            folder_path = "./src/rag/answers/" + exam
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        
            file_path = folder_path + "/test_" + test_number + "_answers.json"
            create_answers_json(outputs, file_path)

        except Exception as json_err:
            print(f"The JSON answers for test {test_number} could not be wrote. Error: {json_err}")

if __name__ == "__main__":
    main()