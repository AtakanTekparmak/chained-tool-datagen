from typing import List, Optional, Union
from ast import literal_eval
import re
import time

from pydantic import ValidationError

from src.models import construct_model
from src.models.config import ModelConfig
from src.schemas import FunctionSchema, DummyFunction, DummyReturn
from src.settings import DUMMY_FUNCTIONS_PATH
from src.utils import save_dummy_functions
from src.templates import load_dummy_fn_template

class DummyFunctionParser:
    """
    Class to parse the generated dummy functions from the model response
    """
    @staticmethod
    def parse(generated_text: str) -> List[DummyFunction]:
        dummy_functions = []
        function_blocks = re.split(r'#~+', generated_text)
        
        for block in function_blocks:
            block = block.strip()
            if not block:
                continue
            
            name_match = re.search(r'def (\w+)', block)
            if not name_match:
                continue
            
            name = name_match.group(1)
            
            return_type_match = re.search(r'-> ([\w\[\]]+):', block)
            return_type = return_type_match.group(1) if return_type_match else "Any"
            
            return_value_match = re.search(r'return (.+)', block)
            if not return_value_match:
                continue
            
            return_value_str = return_value_match.group(1).strip()
            
            try:
                return_value = DummyFunctionParser.parse_return_value(return_value_str, return_type)
                
                dummy_return = DummyReturn(value=return_value, type=return_type)
                
                dummy_function = DummyFunction(
                    name=name,
                    returns=dummy_return,
                    implementation=block.strip()
                )
                dummy_functions.append(dummy_function)
            
            except (ValueError, SyntaxError, ValidationError) as e:
                print(f"Error parsing function {name}: {e}")
                continue
        
        return dummy_functions

    @staticmethod
    def parse_return_value(value_str: str, return_type: str) -> Union[str, int, float, bool, list, dict]:
        if return_type == 'str':
            # Remove quotes if present
            return value_str.strip('\'"')
        elif return_type == 'int':
            return int(value_str)
        elif return_type == 'float':
            return float(value_str)
        elif return_type == 'bool':
            return value_str.lower() == 'true'
        elif return_type.startswith('list') or return_type.startswith('dict'):
            try:
                return literal_eval(value_str)
            except (ValueError, SyntaxError):
                # If literal_eval fails, return as string
                return value_str
        else:
            return value_str

class DummyFunctionGenerator:
    """
    Class to generate dummy functions based on a given list of function schemas
    """
    def __init__(self, model_config: ModelConfig):
        self.model = construct_model(config=model_config)

    def generate_dummy_functions(
            self, 
            function_schemas: List[FunctionSchema],
            verbose: bool = False
        ) -> List[DummyFunction]:
        print(f"Generating dummy functions for {len(function_schemas)} function schemas")
        query = self._create_prompt(function_schemas=function_schemas)
        response = self.model.chat(query)

        if verbose:
            print(response)

        return self._parse_response(response)

    def _create_prompt(self, function_schemas: List[FunctionSchema]) -> str:
        return load_dummy_fn_template(schemas=function_schemas)

    def _parse_response(self, response: str) -> List[DummyFunction]:
        # Extract the content between <dummy_functions> tags
        match = re.search(r'<dummy_functions>(.*?)</dummy_functions>', response, re.DOTALL)
        if not match:
            return []
        
        dummy_functions_text = match.group(1).strip()
        
        parser = DummyFunctionParser()
        return parser.parse(dummy_functions_text)

def generate_dummy_functions(
        function_schemas: List[FunctionSchema],
        model_config: Optional[ModelConfig] = None,
        save: bool = False,
        verbose: bool = False,
        sleep_time: int = 10
    ) -> List[DummyFunction]:
    """
    Generate dummy functions for the given function schemas
    """

    if not model_config:
        model_config = model_config = ModelConfig(
            client="groq",
            system_prompt="You are an helpful assistant that generates dummy functions in the desired format.",
            temperature=0.4,
            fewshot_examples=None
        )

    generator = DummyFunctionGenerator(model_config)
    #dummy_functions = generator.generate_dummy_functions(function_schemas, verbose=verbose)
    dummy_functions = []

    # Go over the curriculum 10 schemas at a time and generate dummy functions with
    # 10 seconds of sleep in between
    for i in range(0, len(function_schemas), 10):
        schemas_batch = function_schemas[i:i+10]
        dummy_functions_batch = generator.generate_dummy_functions(schemas_batch, verbose=verbose)
        dummy_functions.extend(dummy_functions_batch)
        time.sleep(sleep_time)

    if save:
        save_dummy_functions(
            file_path=DUMMY_FUNCTIONS_PATH,
            dummy_functions=dummy_functions
        )

    return dummy_functions