import tomllib
from os.path import join
import csv

from jinja2 import Environment, FileSystemLoader

from src.schemas import FunctionsMetadata, CurriculumRow

# Declare constants
STATIC_DIR = "static"
FNC_TEMPLATE_PATH = "chained_fnc_call.j2"
CURRICULUM_PATH = "static/curriculum/base.csv"

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
    
def load_fnc_template(
        template_name: str = FNC_TEMPLATE_PATH,
        fnc_metadata: FunctionsMetadata = None
    ) -> str:
    """Load the function template from the Jinja2 template file"""
    template = env.get_template(template_name)
    
    if fnc_metadata is not None:
        return template.render(functions_metadata=fnc_metadata.model_dump_json(indent=2))
    else:
        print("No function metadata provided. Rendering an empty template.")
        return template.render(functions_metadata=[])
    
def load_curriculum(file_path: str = CURRICULUM_PATH) -> dict[str, list[CurriculumRow]]:
    """Load a curriculum CSV file and return a list of CurriculumRow objects"""
    curriculum_data = load_csv(file_path)
    curriculum_list = [CurriculumRow.from_dict(row) for row in curriculum_data]

    return _group_curriculum_by_subcategory(curriculum_list)


def _group_curriculum_by_subcategory(curriculum: list[CurriculumRow]) -> dict[str, list[CurriculumRow]]:
    """Group the curriculum by subcategory"""
    grouped_curriculum = {}
    
    for row in curriculum:
        if row.subcategory not in grouped_curriculum:
            grouped_curriculum[row.subcategory] = []
        grouped_curriculum[row.subcategory].append(row)
    
    return grouped_curriculum