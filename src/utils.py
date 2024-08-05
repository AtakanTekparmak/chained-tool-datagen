import tomllib
import csv
import json
import os

from src.schemas import CurriculumRow, Curriculum, FunctionSchema, Parameter, Return, DummyFunction
from src.settings import STATIC_DIR, CURRICULUM_PATH, FN_SCHEMAS_PATH

def load_toml(file_path: str) -> dict[str, any]:
    """Load a TOML file and return the parsed content"""
    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print(f"TOML file not found: {file_path}")
        return {}
    
def load_csv(file_path: str) -> list[dict[str, any]]:
    """Load a CSV file and return the parsed content"""
    try:
        with open(file_path, "r") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"CSV file not found: {file_path}")
        return []
    
def load_curriculum(file_path: str = CURRICULUM_PATH) -> Curriculum:
    """
    Load the curriculum from a CSV file and group it by subcategory
    """
    curriculum_data = load_csv(file_path)
    curriculum_list = [CurriculumRow.from_dict(row) for row in curriculum_data]

    return _group_curriculum_by_subcategory(curriculum_list)


def _group_curriculum_by_subcategory(curriculum: list[CurriculumRow]) -> Curriculum:
    """Group the curriculum by subcategory"""
    grouped_curriculum = {}
    
    for row in curriculum:
        if row.subcategory not in grouped_curriculum:
            grouped_curriculum[row.subcategory] = []
        grouped_curriculum[row.subcategory].append(row)
    
    return grouped_curriculum

def save_json(file_path: str, data: dict[str, any]):
    """Save a dictionary to a JSON file"""
    # Create the directory if it doesn't exist
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def save_function_schemas(schemas: list[dict[str, any]], file_path: str = FN_SCHEMAS_PATH):
    """Save function schemas to a JSON file"""
    save_json(file_path, schemas)

def load_function_schemas(file_path: str = FN_SCHEMAS_PATH) -> list[FunctionSchema]:
    """Load function schemas from a JSON file"""
    try:
        with open(file_path, "r") as f:
            list_of_schemas: list[dict[str, any]] = json.load(f)

            loaded_schemas = []
            for schema in list_of_schemas:
                name = schema["name"]
                description = schema["description"]
                parameters = [Parameter(**p) for p in schema["parameters"]]
                required = [r for r in schema["required"]]
                returns = [Return(**r) for r in schema["returns"]]

                loaded_schemas.append(FunctionSchema(
                    name=name, 
                    description=description, 
                    parameters=parameters, 
                    required=required, 
                    returns=returns
                    )
                )

            return loaded_schemas

    except FileNotFoundError:
        print(f"Function schemas file not found: {file_path}")
        return []
    
def save_dummy_functions(file_path: str, dummy_functions: list[DummyFunction]):
    """Save dummy functions to a Python file"""
    # Create the directory if it doesn't exist
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "w") as f:
            for dummy_function in dummy_functions:
                f.write(dummy_function.implementation)
                f.write("\n\n")
    except FileNotFoundError:
        print(f"File \"{file_path}\" does not exist")