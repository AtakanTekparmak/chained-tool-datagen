import tomllib
from os.path import join
import csv
import json
import os

from jinja2 import Environment, FileSystemLoader

from src.schemas import FunctionsMetadata, CurriculumRow, Curriculum
from src.settings import STATIC_DIR, CURRICULUM_PATH, FN_CALL_TEMPLATE_PATH, FN_GENERATE_TEMPLATE_PATH, RESULT_DIR, FN_SCHEMAS_PATH

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(join(STATIC_DIR, "templates")))

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
    
def load_jinja_template(template_name: str, context: dict[str, any]) -> str:
    """Load a Jinja2 template and render it with the given context"""
    template = env.get_template(template_name)
    return template.render(context)
    
def load_fn_call_template(
        template_name: str = FN_CALL_TEMPLATE_PATH,
        fnc_metadata: FunctionsMetadata = None
    ) -> str:
    """Load the function template from the Jinja2 template file"""
    context = {"functions_metadata": fnc_metadata} if fnc_metadata else {"functions_metadata": []}
    return load_jinja_template(template_name, context)

def load_fn_generate_template(
        template_name: str = FN_GENERATE_TEMPLATE_PATH,
        category: str = None,
        subcategory: str = None,
        tasks: list[str] = []
    ) -> str:
    """Load the function generation template from the Jinja2 template file"""
    context = {"category": category, "subcategory": subcategory, "tasks": tasks}
    return load_jinja_template(template_name, context)
    
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
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def save_function_schemas(schemas: list[dict[str, any]], file_path: str = FN_SCHEMAS_PATH):
    """Save function schemas to a JSON file"""
    save_json(file_path, schemas)