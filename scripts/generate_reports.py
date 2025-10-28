from baseline.model_evaluation import get_answers, count_correct_answers
from baseline.plots import plot_graphs
import json

def main() -> None:
    exam = "ancord-aai"

    test_numbers = ["01", "02", "03", "04", "05", "06"]
    models = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gpt-5-nano", "deepseek-r1-distill-qwen-14B", "deepseek-r1-distill-llama-8B", "gemma-3-27B-it", "gpt-oss-20B", "llama-3.1-8B-instruct", "llama-3.3-70B-instruct", "qwen3-4B-instruct"]

    model_dict = {f'{model}': 0.0 for model in models}
    model_performances = {f'{test_number}': model_dict for test_number in test_numbers}
    model_performances['all'] = model_dict

    for test_number in test_numbers:
        for model in models:
            # TODO: implement the model performances in the model_performances dict

            pass

    # Export model_performances as a file
    file_path = "./reports/" + model + "/model_performances.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(model_performances, f, indent=4)

    # TODO: insert the plotting function to generate the reports

if __name__ == "__main__":
    main()  