from baseline.wrapper.llm_wrapper import GeminiWrapper, GPT5Wrapper, HuggingFaceWrapper
from baseline.wrapper.prompt import generate_prompts
from baseline.wrapper.response_format import generate_response_formats
from baseline.config import EXAMS, MODELS
import json
import os

def create_answers_csv(exam: str, test_number: str, outputs: list[str], model_name: str) -> None:

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
                provider = model['provider']
                max_tokens = model['max_tokens']
                models[model_name] = HuggingFaceWrapper(model_name=model_name, provider=provider, max_tokens=max_tokens)

    # Toggle the exam
    exam = "ancord-aai"
    # exam = "cpa-10"

    test_numbers = EXAMS[exam]["test_numbers"]

    response_formats = generate_response_formats(exam)

    for test_number in test_numbers:
        prompts = generate_prompts(exam, test_number)
        for model_name, model in models.items():
            outputs: list[str] = []
            has_errors = False
            
            for prompt, response_format in zip(prompts, response_formats):
                try: 
                    output = model.generate_output(prompt, response_format)
                    outputs.append(output)
                except Exception as err:
                    has_errors = True
                    print(f"The model {model} could not generate the answers for the test {test_number}. Error: {err}")

            if not has_errors:
                try: 
                    create_answers_csv(exam, test_number, outputs, model_name)
                except Exception as csv_err:
                    print(f"The CSV answers for the model {model} and test {test_number} could not be wrote. Error: {csv_err}")


if __name__ == '__main__':
    main()