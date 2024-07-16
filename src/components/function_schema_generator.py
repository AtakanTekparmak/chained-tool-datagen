from typing import List, Dict, Any, Union
from src.models import construct_model
from src.models.config import ModelConfig
from src.schemas import FunctionsMetadata

class FunctionSchemaGenerator:
    def __init__(self, model_config: ModelConfig):
        self.model = construct_model(config=model_config)

    def generate_schemas(self, category: str, strategy: str, tasks: Union[str, List[str]]) -> List[Dict[str, Any]]:
        if isinstance(tasks, str):
            tasks = [tasks]
        
        prompt = self._create_prompt(category, strategy, tasks)
        response = self.model.chat(prompt)
        return self._parse_response(response)

    def _create_prompt(self, category: str, strategy: str, tasks: List[str]) -> str:
        tasks_str = "\n".join([f"- {task}" for task in tasks])
        return f"""
        Given the following curriculum details:
        Category: {category}
        Strategy: {strategy}
        Tasks:
        {tasks_str}

        Generate JSON schemas for functions that could be used to accomplish these tasks.
        For each task, generate at least one function schema.
        Each schema should include:
        - name: A descriptive name for the function
        - description: A brief description of what the function does
        - parameters: A list of parameters the function accepts, including their names and types
        - required: A list of required parameter names
        - returns: A list of return values, including their names and types

        Provide the schemas in valid JSON format. Wrap each schema in <schema> and </schema> tags.
        Separate each schema with a newline.
        """

    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        import json
        schemas = []
        # Split the response by </schema> to handle multiple schemas
        if "<schema>" not in response or "</schema>" not in response:
            return []
        
        raw_schemas = response.split("</schema>")
        for raw_schema in raw_schemas:
            if "<schema>" in raw_schema:
                # Extract the schema between the <schema> and </schema> tags
                schema_json = raw_schema.split("<schema>")[1].strip()
                try:
                    schema = json.loads(schema_json)
                    schemas.append(schema)
                except json.JSONDecodeError:
                    print(f"Failed to parse schema: {schema_json}")
        return schemas