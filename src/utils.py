import tomllib
import csv
import json
import os

from src.schemas import CurriculumRow, Curriculum
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
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def save_function_schemas(schemas: list[dict[str, any]], file_path: str = FN_SCHEMAS_PATH):
    """Save function schemas to a JSON file"""
    save_json(file_path, schemas)