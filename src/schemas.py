from pydantic import BaseModel
from typing import Union, Optional

from easy_fnc.schemas import (
    FunctionCall,
    FunctionReturn,
    FunctionParameter,
    FunctionMetadata,
)
from easy_fnc.schemas import ModelResponse as ChainedFNCResponse

class FunctionsMetadata(BaseModel):
    """
    Pydantic model for functions metadata
    """
    functions_metadata: list[FunctionMetadata]

    @classmethod
    def from_list(cls, functions_metadata: list[FunctionMetadata]) -> 'FunctionsMetadata':
        """Create a FunctionsMetadata object from a list of FunctionMetadata objects"""
        return cls(functions_metadata=functions_metadata)

class UserMessage(BaseModel):
    """
    Pydantic model for user message
    """
    role: str = "user"
    content: Optional[str]

class SystemMessage(BaseModel):
    """
    Pydantic model for system message
    """
    role: str = "system"
    content: Optional[str]

class AssistantMessage(BaseModel):
    """
    Pydantic model for assistant message
    """
    role: str = "assistant"
    content: Optional[str]

class Conversation(BaseModel):
    """
    Pydantic model for conversation
    """
    system_prompt: Optional[str]
    messages: Optional[list[Optional[Union[SystemMessage, UserMessage, AssistantMessage]]]]

    def add_user_message(self, content: Union[str, UserMessage]):
        """Add a user message to the conversation"""
        if isinstance(content, str):
            self.messages.append(UserMessage(content=content))
        else:
            self.messages.append(content)

    def add_assistant_message(self, content: Union[str, AssistantMessage]):
        """Add an assistant message to the conversation"""
        if isinstance(content, str):
            self.messages.append(AssistantMessage(content=content))
        else:
            self.messages.append(content)