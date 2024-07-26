from typing import List, Dict, Any, Union, Optional
import json

from src.models import construct_model
from src.models.config import ModelConfig
from src.schemas import Curriculum, FunctionSchema
from src.utils import load_fn_generate_template, load_curriculum, save_function_schemas

class FunctionSchemaGenerator:
    """
    Class to generate function schemas based on a given category, subcategory, and tasks
    """
    def __init__(self, model_config: ModelConfig):
        self.model = construct_model(config=model_config)

    def generate_by_curriculum(
            self, 
            curriculum: Curriculum,
            verbose: bool = False
        ) -> List[Dict[str, Any]]:
        """
        Generate function schemas for each subcategory in the curriculum
        """
        schemas = []
        for subcategory in curriculum:
            tasks = [row.task for row in curriculum[subcategory]]
            category = curriculum[subcategory][0].category
            print(f"Generating schemas for subcategory: {subcategory}")
            print(f"Tasks: {tasks}")
            task_schemas = self.generate_schemas(category, subcategory, tasks)
            print(f"Generated {len(task_schemas)} schemas:")

            if verbose:
                for schema in task_schemas:
                    json_schema = json.dumps(schema, indent=2)
                    print(json_schema)
            schemas.extend(task_schemas)
        return schemas

    def generate_schemas(self, category: str, subcategory: str, tasks: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Generate function schemas for a given category, subcategory, and tasks
        """
        if isinstance(tasks, str):
            tasks = [tasks]
        
        prompt = self._create_prompt(category, subcategory, tasks)
        response = self.model.chat(prompt)
        return self._parse_response(response)

    def _create_prompt(self, category: str, subcategory: str, tasks: List[str]) -> str:
        tasks_str = "\n".join([f"- {task}" for task in tasks])
        return load_fn_generate_template(category=category, subcategory=subcategory, tasks=tasks_str)

    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
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
    
def function_generating_flow(model_config: Optional[ModelConfig] = None):
    """
    Flow for function schema generation.
    """
    if not model_config:
        model_config = ModelConfig(
            client="groq",
            system_prompt="You are a helpful assistant that generates function schemas.",
            temperature=0.7,
            fewshot_examples=None
        )
    generator = FunctionSchemaGenerator(model_config)

    # Load the curriculum
    curriculum = load_curriculum()
    
    # Generate schemas for each subcategory in the curriculum
    schemas = generator.generate_by_curriculum(curriculum, verbose=True)

    # Save the schemas to a JSON file
    save_function_schemas(schemas)

def generate_function_schemas(
        model_config: Optional[ModelConfig] = None,
        curriculum: Optional[Curriculum] = None,
        verbose: bool = False,
        save: bool = False
    ) -> List[FunctionSchema]:
    """
    Generate function schemas using a curriculum-based approach.

    Args:
        model_config (ModelConfig, optional): Model configuration. Defaults to None.
        curriculum (Curriculum, optional): Curriculum to generate schemas for. Defaults to None.
        verbose (bool, optional): Whether to print the generated schemas. Defaults to False.

    
    """
    if not model_config:
        model_config = ModelConfig(
            client="groq",
            system_prompt="You are a helpful assistant that generates function schemas.",
            temperature=0.7,
            fewshot_examples=None
        )

    if not curriculum:
        curriculum = load_curriculum()

    # Generate function schemas
    generator = FunctionSchemaGenerator(model_config)
    schemas = generator.generate_by_curriculum(curriculum, verbose=verbose)

    # Parse the schemas
    parsed_schemas: List[FunctionSchema] = [FunctionSchema.from_dict(schema) for schema in schemas]

    if save:
        save_function_schemas(schemas)

    return parsed_schemas