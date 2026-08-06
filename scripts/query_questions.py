from baseline.config import EXAMS
from baseline.wrapper.response_format import generate_response_models
from baseline.wrapper.prompt import generate_prompts
import json
import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def create_answers_json(exam: str, test_number: str, responses: list[str]) -> None:

    # Handling the responses strings to create a single JSON object
    json_text = ''
    for i, response in enumerate(responses):
        json_start_idx = response.find(r'{')
        json_end_idx = response.rfind(r'}')
        if i == 0:
            json_text = response[json_start_idx:json_end_idx] + ","
        elif i == len(responses) - 1:
            json_text = json_text + response[(json_start_idx+1):(json_end_idx+1)]
        else:
            json_text = json_text + response[(json_start_idx+1):json_end_idx] + ","
    
    json_object = json.loads(json_text)

    folder_path = "./model_answers/" + exam + "/rag"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/test_" + test_number + "_answers.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_object, f, indent=3)

def main()->None:

    # Retrieve HF_TOKEN
    load_dotenv(dotenv_path="./config.env") 

    # Toogle the exam
    exam = "cpa-10"
    # exam = "ancord-aai"

    # Same model used to index the documents
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

    # Certify ollama model is running on port 11434
    llm = Ollama(model="llama3.1:latest", request_timeout=120.0)

    storage_context = StorageContext.from_defaults(persist_dir="./index/"+exam)
    index = load_index_from_storage(storage_context)

    test_numbers = EXAMS[exam]["test_numbers"]
    response_models = generate_response_models(exam)

    for test_number in test_numbers:
        responses:list[str] = []
        has_errors = False

        prompts = generate_prompts(exam, test_number)

        for idx, _iter in enumerate(zip(prompts, response_models)):
            prompt = _iter[0]
            response_model = _iter[1]
            sllm = llm.as_structured_llm(response_model)
            query_engine = index.as_query_engine(llm=sllm)

            try:
                response = query_engine.query(prompt)
                response_str = str(response)
                responses.append(response_str)
                print(f"Response of chunk {idx+1} of test {test_number}:\n{response_str}")
            except Exception as err:
                has_errors = True
                print(f"Could not query the response for the test {test_number} for the chunk {idx+1}. Error: {err}")
                # If a model could not generate the answers for one chunk of a test,
                # all the answers for the further chunks will be useless.
                break

        # If there was an error, continue to the next test
        if has_errors:
            continue

        try: 
            create_answers_json(exam, test_number, responses)
        except Exception as json_err:
            print(f"The JSON answers for test {test_number} could not be wrote. Error: {json_err}")

if __name__ == "__main__":
    main()