from typing import List, Optional
import json

from src.models import construct_model
from src.models.config import ModelConfig
from src.schemas import FunctionSchema, UserQuery
from src.settings import USER_QUERIES_PATH
from src.utils import save_json
from src.templates import load_query_generate_template

class UserQueryGenerator:
    """
    Class to generate user queries based on a given list of function schemas
    """
    def __init__(self, model_config: ModelConfig):
        self.model = construct_model(config=model_config)

    def generate_queries(
            self, 
            function_schemas: List[FunctionSchema],
            num_examples: int = 10,
            verbose: bool = False
        ) -> List[UserQuery]:
        """
        Generate user queries for the given function schemas
        """
        print(f"Generating user queries for {len(function_schemas)} function schemas")
        query = self._create_prompt(function_schemas, num_examples)
        response = self.model.chat(query)

        if verbose:
            print(response)

        return self._parse_response(response)

    def _create_prompt(self, function_schemas: List[FunctionSchema], num_examples: int) -> str:
        return load_query_generate_template(schemas=function_schemas, num_examples=num_examples)

    def _parse_response(self, response: str) -> List[UserQuery]:
        queries = []
        # The queries are in between <examples> and </examples> tags
        if "<examples>" not in response or "</examples>" not in response:
            return []
        response = response.split("<examples>")[1].split("</examples>")[0]
        
        try:
            examples = json.loads(response)
            for example in examples:
                queries.append(UserQuery.from_dict(example))

            return queries
        except json.JSONDecodeError:
            return []
        

def generate_user_queries(
        function_schemas: List[FunctionSchema],
        model_config: Optional[ModelConfig] = None,
        num_examples: int = 10,
        save: bool = False,
        verbose: bool = False
    ) -> List[UserQuery]:
    """
    Generate user queries for the given function schemas
    """

    if not model_config:
        model_config = ModelConfig(
            client="groq",
            system_prompt="You are an helpful assistant that generates user queries in the desired format.",
            temperature=0.4,
            fewshot_examples=None
        )
    generator = UserQueryGenerator(model_config)
    queries = generator.generate_queries(
        function_schemas=function_schemas, 
        num_examples=num_examples,
        verbose=verbose
    )

    if save:
        save_json(
            data=[query.model_dump() for query in queries],
            file_path=USER_QUERIES_PATH
        )

    return queries
