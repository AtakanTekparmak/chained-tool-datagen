from pydantic import BaseModel
from typing import Optional

from src.schemas import Conversation

class ModelConfig(BaseModel):
    """
    Pydantic model for model configuration
    """
    client: str
    system_prompt: Optional[str]
    temperature: float
    fewshot_examples: Optional[Conversation]

    # Method to set the system prompt
    def set_system_prompt(self, system_prompt: str):
        """Set the system prompt"""
        self.system_prompt = system_prompt

    def set_fewshot_examples(self, fewshot_examples: Conversation):
        """Set the fewshot examples"""
        self.fewshot_examples = fewshot_examples