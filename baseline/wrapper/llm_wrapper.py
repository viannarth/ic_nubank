import os
from abc import ABC, abstractmethod
from google import genai
from openai import OpenAI
from huggingface_hub import InferenceClient
from typing import Any

# Make sure to have the following environment variables in your computer.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Message content to the model as system/developer
SYSTEM_ROLE = "You are an expert on Brazilian financial market and a sublime question answering assistant. You always respond in the correct proposed output format."

class LLMWrapper(ABC):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

    @abstractmethod
    def preprocess_input(self, prompt: str, response_format: dict[str, Any]) -> dict[str, Any]:
        pass
    
    @abstractmethod
    def generate_output(self, prompt: str, response_format: dict[str, Any]) -> str:
        pass

class GeminiWrapper(LLMWrapper):
    def __init__(self, model_name: str, api_key: str = GEMINI_API_KEY):
        super().__init__(model_name, api_key)
        self.client = genai.Client(api_key=self.api_key)

    def preprocess_input(self, prompt: str, response_format: dict[str, Any]) -> dict[str, Any]:

        contents = prompt
        config = {
            "temperature": 0.0,
            "system_instruction": SYSTEM_ROLE,
            "response_mime_type": "application/json", 
            "response_json_schema": response_format["json_schema"]
        }

        input_dict = {
            "contents": contents,
            "config": config
        }
        return input_dict
    
    def generate_output(self, prompt: str, response_format: dict[str, Any]) -> str:

        input_dict = self.preprocess_input(prompt, response_format)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=input_dict["contents"],
                config=input_dict["config"]
            )
            output = response.text
            return output
        
        except Exception as err:
            raise err

class GPT5Wrapper(LLMWrapper):
    def __init__(self, model_name: str, api_key: str = OPENAI_API_KEY):
        super().__init__(model_name, api_key)
        self.client = OpenAI(api_key=self.api_key)

    def preprocess_input(self, prompt: str, response_format: dict[str, Any]) -> dict[str, Any]:

        messages = [
            {
                "role": "developer",
                "content": f"{SYSTEM_ROLE}"
            },
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ]

        verbosity = 'low'

        input_dict = {
            "messages": messages,
            "verbosity": verbosity,
            "response_format": response_format
        }

        return input_dict

    def generate_output(self, prompt: str, response_format: dict[str, Any]) -> str:

        input_dict = self.preprocess_input(prompt, response_format)

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=input_dict["messages"],
                verbosity=input_dict["verbosity"],
                response_format=input_dict["response_format"]
            )
            output = completion.choices[0].message.content
            return output
        
        except Exception as err:
            raise err

class HuggingFaceWrapper(LLMWrapper):
    def __init__(self, model_name: str, provider: str, max_tokens: int = 4096, api_key: str = HF_TOKEN):
        super().__init__(model_name, api_key)
        self.client = InferenceClient(
            provider=provider,
            api_key=self.api_key
        )
        self.max_tokens = max_tokens

    def preprocess_input(self, prompt: str, response_format: dict[str, Any]) -> dict[str, Any]:

        messages = [
            {
                "role": "system",
                "content": f"{SYSTEM_ROLE}"
            },
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ]

        temperature = 0.0

        input_dict = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": self.max_tokens,
            "response_format": response_format
        }
        return input_dict

    def generate_output(self, prompt: str, response_format: dict[str, Any]) -> str:

        input_dict = self.preprocess_input(prompt, response_format)

        try:
            response = self.client.chat_completion(
                messages=input_dict["messages"],
                response_format=input_dict["response_format"],
                temperature=input_dict["temperature"],
                max_tokens=input_dict["max_tokens"],
                model=self.model_name
            )
            output_text = response.choices[0].message.content
            return output_text
        
        except Exception as err:
            raise err