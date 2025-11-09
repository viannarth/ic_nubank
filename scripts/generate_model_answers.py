from baseline.wrapper.llm_wrapper import GeminiWrapper, GPT5Wrapper, HuggingFaceWrapper
from baseline.wrapper.prompt import generate_prompts
from baseline.wrapper.response_format import generate_response_formats
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
    models = {
        "gemini-2.5-flash-lite": GeminiWrapper(model_name="gemini-2.5-flash-lite"),
        "gemini-2.5-flash": GeminiWrapper(model_name="gemini-2.5-flash"),
        "gpt-5-nano": GPT5Wrapper(model_name='gpt-5-nano'),
        "deepseek-r1-distill-qwen-14B": HuggingFaceWrapper(model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", provider="novita"),
        "deepseek-r1-distill-llama-8B": HuggingFaceWrapper(model_name="deepseek-ai/DeepSeek-R1-Distill-Llama-8B", provider="nscale", max_tokens=8192),
        "gemma-3-27B-it": HuggingFaceWrapper(model_name="google/gemma-3-27b-it", provider="nebius"),
        "gpt-oss-20B": HuggingFaceWrapper(model_name="openai/gpt-oss-20b", provider="together", max_tokens=16384),
        "llama-3.1-8B-instruct": HuggingFaceWrapper(model_name="meta-llama/Llama-3.1-8B-Instruct", provider="cerebras"), 
        "llama-3.3-70B-instruct": HuggingFaceWrapper(model_name="meta-llama/Llama-3.3-70B-Instruct", provider="cerebras"),
        "qwen3-4B-instruct": HuggingFaceWrapper(model_name="Qwen/Qwen3-4B-Instruct-2507", provider="nscale")
    }

    exam = "ancord-aai"
    test_numbers = [
        "01", 
        "02",
        "03",
        "04",
        "05",
        "06"
    ]
    total_number_questions = 80
    
    # The prompt and the response are split into chunks to avoid
    # exceeding the maximum completion tokens.
    chunk_size = 20 # Number of questions of each chunk

    response_formats = generate_response_formats(total_number_questions, chunk_size)

    for test_number in test_numbers:
        prompts = generate_prompts(exam, test_number, total_number_questions, chunk_size)
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