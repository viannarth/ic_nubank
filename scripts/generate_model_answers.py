from baseline.wrapper.model_wrapper import GeminiWrapper, GPT5Wrapper, HuggingFaceWrapper
from baseline.wrapper.prompt import generate_prompts
from baseline.wrapper.response_format import generate_json_schemas
from baseline.config import EXAMS, MODELS
import json
import os

# Maximum number of tries for a model to generate the answers
# for a test  
MAX_REQUEST_TRIES = 5

def create_answers_json(exam: str, test_number: str, outputs: list[str], model_name: str) -> None:

    # Handling the outputs strings to create a single JSON object
    json_text = ''
    for i, output in enumerate(outputs):
        json_start_idx = output.find(r'{')
        json_end_idx = output.rfind(r'}')
        if i == 0:
            json_text = output[json_start_idx:json_end_idx] + ","
        elif i == len(outputs) - 1:
            json_text = json_text + output[(json_start_idx+1):(json_end_idx+1)]
        else:
            json_text = json_text + output[(json_start_idx+1):json_end_idx] + ","
    
    json_object = json.loads(json_text)

    folder_path = "./model_answers/" + exam + "/" + model_name
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + "/test_" + test_number + "_answers.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_object, f, indent=3)


def main() -> None:

    models: dict[str, GeminiWrapper | GPT5Wrapper | HuggingFaceWrapper] = {}

    for wrapper_name, wrapper_dict in MODELS.items():
        if wrapper_name == 'gemini':
            for model_name in wrapper_dict:
                models[model_name] = GeminiWrapper(model_name=model_name)
        elif wrapper_name == 'gpt-5':
            for model_name in wrapper_dict:
                models[model_name] = GPT5Wrapper(model_name=model_name)
        elif wrapper_name == 'hugging_face':
            for model_name, model in wrapper_dict.items():
                model_repo = model['model_repo']
                provider = model['provider']
                max_tokens = model['max_tokens']
                models[model_name] = HuggingFaceWrapper(model_name=model_repo, provider=provider, max_tokens=max_tokens)

    # Toggle the exam
    # exam = "ancord-aai"
    exam = "cpa-10"

    test_numbers = EXAMS[exam]["test_numbers"]

    response_formats = generate_json_schemas(exam)

    for test_number in test_numbers:
        prompts = generate_prompts(exam, test_number)
        for model_name, model in models.items():
            file_path = "./model_answers/" + exam + "/" + model_name + "/" + "test_" + test_number + "_answers.json"
            num_tries = 0
            # Loop while the model answers file is not created and the number
            # of tries does not reach the maximum
            while not os.path.exists(file_path) and num_tries <= MAX_REQUEST_TRIES: 
                
                num_tries += 1

                outputs: list[str] = []
                has_errors = False
                
                for idx, _iter in enumerate(zip(prompts, response_formats)):
                    try: 
                        prompt = _iter[0]
                        response_format = _iter[1]
                        output = model.generate_output(prompt, response_format)
                        outputs.append(output)
                    except Exception as err:
                        has_errors = True
                        print(f"The model {model_name} could not generate the answers for the test {test_number} for the chunk {idx+1}. Error: {err}")
                        # If a model could not generate the answers for one chunk of a test,
                        # all the answers for the further chunks will be useless.
                        break

                # If there was an error, continue to the next iteration
                if has_errors:
                    continue

                try: 
                    create_answers_json(exam, test_number, outputs, model_name)
                except Exception as csv_err:
                    print(f"The CSV answers for the model {model_name} and test {test_number} could not be wrote. Error: {csv_err}")


if __name__ == '__main__':
    main()