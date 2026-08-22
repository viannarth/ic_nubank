# Evaluation of LLMs on Brazilian financial market certififcation exams

This project is related to an undergraduate research (ITA/Nubank) in which proprietary and open-source LLMs were evaluated on multiple-choice questions from ANBIMA CPA-10 and ANCORD-AAI exams, both certifications for the Brazilian financial market.

## Repo structure

```bash
eval_llms/
├── config.yaml     # Configuration file   
├── README.md
├── requirements.txt
└── src/
    ├── baseline/   # Baseline construction
    │   ├── model_answers/
    │   ├── plot.py
    │   ├── reports/
    │   ├── scripts/
    │   │   ├── generate_model_answers.py    
    │   │   └── generate_reports.py         
    │   └── wrapper/   
    │       ├── base_prompt.txt
    │       ├── model_wrapper.py
    │       ├── prompt.py
    │       └── response_format.py
    ├── data/
    │   ├── create_dataset.py
    │   ├── dataset/    # Parsed dataset
    │   └── dataset.py
    ├── rag/    # RAG pipeline construction
    │   ├── answers/   
    │   ├── base_prompt.txt
    │   ├── index/      # Indexed material
    │   ├── material/   # Parsed material
    │   ├── prompt.py
    │   ├── reports/
    │   ├── response_format.py
    │   └── scripts/
    │       ├── eval_rag.py
    │       ├── index_document.py
    │       ├── parse_material.py
    │       └── query_questions.py
    └── utils/  # Helper functions
        ├── config.py
        ├── eval_answers.py
        └── files.py
```

## Instructions

This project was implemented with Python 3.14. Certify you have this Python version on your machine. 

Clone the project with `git clone` and move to the root folder. It is recommended to create a Python virtual environment (see [venv](https://docs.python.org/3/library/venv.html)). Run `pip install -r requirements.txt` in the root folder to install the project dependencies.

Run a script in the root folder with `python -m src.dir.script`. For example, to parse the dataset, you can run `python -m src.data.create_dataset`.

## Authors

**Main author**: Arthur de Sousa Vianna  
**Advisor**: Prof. Paulo André de Lima Castro