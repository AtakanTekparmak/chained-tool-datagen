# components/function_schema_generator.py

from typing import List, Dict, Any
from src.models import construct_model
from src.models.config import ModelConfig
from src.schemas import FunctionsMetadata

class FunctionSchemaGenerator:
    def __init__(self, model_config: ModelConfig):
        self.model = construct_model(config=model_config)

    def generate_schema(self, category: str, strategy: str, task: str) -> List[Dict[str, Any]]:
        prompt = self._create_prompt(category, strategy, task)
        response = self.model.chat(prompt)
        return self._parse_response(response)

    def _create_prompt(self, category: str, strategy: str, task: str) -> str:
        return f"""
        Given the following curriculum details:
        Category: {category}
        Strategy: {strategy}
        Task: {task}

        Generate a JSON schema for a function that could be used to accomplish this task.
        The schema should include:
        - name: A descriptive name for the function
        - description: A brief description of what the function does
        - parameters: A list of parameters the function accepts, including their names and types
        - required: A list of required parameter names
        - returns: A list of return values, including their names and types

        Provide the schema in valid JSON format. In between <schema> and </schema> tags.
        """

    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        # Implement parsing logic here to convert the model's response
        # into a list of function schemas
        # This is a placeholder and should be replaced with actual parsing logic
        import json
        print(response) 
        # Extract the response between the <schema> and </schema> tags
        response = response.split("<schema>")[1].split("</schema>")[0].strip()
        return json.loads(response)