import os
from groq import Groq

class GroqModel:
    """A class to interact with the Groq API and chat with the model"""
    def __init__(self, model_name: str):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = model_name

    def chat(self, user_message: str):
        """Chat with the model and return the response"""
        # Create a message object for the user input
        messages = [{"role": "user", "content": user_message}]

        # Get the chat completion from the model
        return self._get_chat_completion(messages)

    def _get_chat_completion(self, messages):
        """Get the chat completion from the model"""
        return self.client.chat.completions.create(messages=messages, model=self.model_name).choices[0].message.content