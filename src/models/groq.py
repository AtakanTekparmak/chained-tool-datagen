import os

from groq import Groq

from src.models.model import Model

class GroqModel(Model):
    """A class to interact with the Groq API and chat with the model"""
    def __init__(self, config):
        super().__init__(config)
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = config.name

    def format_user_input(self, user_input: str) -> str:
        """Format the user input"""
        return "<user_query>\n" + user_input + "\n</user_query>\n"
    
    def _get_chat_completion(self, messages) -> str:
        """Get the chat completion from the model"""
        # Get the messages as a list of dictionaries
        messages_list = [message.model_dump() for message in messages.messages]
        return self.client.chat.completions.create(messages=messages_list, model=self.model_name).choices[0].message.content