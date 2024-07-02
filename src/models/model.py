from abc import ABC, abstractmethod

from src.models.config import ModelConfig
from src.schemas import Conversation, UserMessage, AssistantMessage, SystemMessage

class Model(ABC):
    """Abstract class for models"""
    def __init__(self, config: ModelConfig):
        self.config = config
        self.messages = None

    def _setup_messages(self, user_message: UserMessage):
        """Setup the messages for the conversation"""        
        if self.config.system_prompt:
            self.messages = Conversation(
                system_prompt=self.config.system_prompt,
                messages=[SystemMessage(content=self.config.system_prompt), user_message] 
            )
        else:
            print("No system prompt provided. Using only the user message.")
            self.messages = Conversation(messages=[user_message])


    @abstractmethod
    def format_user_input(self, user_input: str) -> str:
        """Format the user input"""
        pass

    @abstractmethod
    def _get_chat_completion(self, messages: Conversation) -> str:
        """Get the chat completion from the model"""
        pass

    def chat(self, user_message: str):
        """Chat with the model and return the response"""   
        # Format the user input and add it to the conversation
        formatted_input = self.format_user_input(user_message)
        user_message = UserMessage(content=formatted_input)
        
        # Setup the messages for the conversation if not already setup
        if not self.messages:
            self._setup_messages(user_message)
        else:
            self.messages.add_user_message(user_message)
        
        # Get the chat completion from the model
        assistant_response = self._get_chat_completion(self.messages)
        self.messages.add_assistant_message(assistant_response)

        return assistant_response
