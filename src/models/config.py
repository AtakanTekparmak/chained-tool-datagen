from pydantic import BaseModel
from typing import Optional

from src.schemas import Conversation

class ModelConfig(BaseModel):
    """
    Pydantic model for model configuration
    """
    client: str
    name: str
    system_prompt: Optional[str]
    temperature: float
    fewshot_examples: Optional[Conversation]
    