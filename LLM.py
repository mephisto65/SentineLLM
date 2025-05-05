import openai
import mistralai
import anthropic
from typing import List, Dict, Any, Optional

class LLM():

    def __init__(self,model : str, context_window_size: int = 12):
        self.model=model
        self.conversation_history=[]
        self.context_window_size=max(1, context_window_size)  # Minimum 1 message
        self.api_key = None
        self.internal_prompt = "You are a helpful assistant."
        self.answer = None
        self.client = None

    def set_internal_prompt(self, internal_prompt: str) -> None:
        """
        Sets the internal prompt for the model
        
        Args:
        internal_prompt: Internal prompt to be set
        """
        self.internal_prompt = internal_prompt
        self.conversation_history.append({"role": "system", "content": self.internal_prompt})

    def retrieve_key(self,key_file) -> Optional[str] :
        """
        Retrieves the API key from a file
        
        Args:
        key_file: Name of the file containing the API key
                    
        Returns:
        Error message on failure, None on success
        """
        try:
            with open(f"{key_file}", "r") as file:
                self.api_key = file.read().strip()
                return None
        except Exception as e:
            return f"Error while retrieving key : {str(e)}"
    
    def create_answer(self, prompt_to_respond: str) -> str:
        """
        Abstract method to be implemented in child classes
        to generate a response from the prompt
        """
        raise NotImplementedError("This method must be implemented in the derived classes")
    
    def update_history(self,prompt_to_respond: str = None) -> None:
        """
        update conversation history
        
        Args:
        prompt_to_respond: Attacker's prompt
        """
        # Appel de la méthode spécifique à la classe enfant pour ajouter les messages
        self._add_to_history(prompt_to_respond)

        max_messages = self.context_window_size

        if len(self.conversation_history) > max_messages + 1:
                excess = len(self.conversation_history) - (max_messages + 1)
                self.conversation_history = self.conversation_history[excess:]
                preserved = self.conversation_history[0:1] # To keep the internal prompt into the history
                remaining = self.conversation_history[1:]
                self.conversation_history = preserved + remaining[excess:]
    
    def _add_to_history(self,prompt_to_respond=None):
        """
        Abstract method to be implemented in child classes
        to add messages with a specific format to the conversation history
        """
        raise NotImplementedError("This method must be implemented in the derived classes")


    def reset_history(self) -> None:
        """Resets conversation history while retaining system prompt"""
        self.conversation_history = [{"role": "system", "content": self.internal_prompt}]


class OpenAIModel(LLM):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        super().__init__(model)

    def initialize_client(self):
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            return None
        except Exception as e:
            return f"Error while initializing OpenAI Client: {str(e)}"

    def create_answer(self) -> str:
        try:
            response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history)

            self.answer = response.choices[0].message.content.strip()
            return self.answer
        except Exception as e:
            return f"Error with OpenAI API: {str(e)}"
        
    def _add_to_history(self, prompt_to_respond=None):
        if prompt_to_respond==None :
            self.conversation_history.append({"role": "assistant", "content": self.answer})
        else:
            self.conversation_history.append({"role": "user", "content": prompt_to_respond})

class DeepSeekModel(LLM):
    def __init__(self, model: str = "deepseek-chat"):
        super().__init__(model)

    def initialize_client(self):
        try:
            self.client = openai.OpenAI(api_key=self.api_key,base_url="https://api.deepseek.com")
            return None
        except Exception as e:
            return f"Error while initializing OpenAI (deepseek) Client: {str(e)}"
        
    def create_answer(self) -> str:
        try:
            response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history)

            self.answer=response.choices[0].message.content.strip()
            return self.answer
        except Exception as e:
            return f"Error with OpenAI API: {str(e)}"
        
    def _add_to_history(self, prompt_to_respond=None):
        if prompt_to_respond==None :
            self.conversation_history.append({"role": "assistant", "content": self.answer})
        else:
            self.conversation_history.append({"role": "user", "content": prompt_to_respond})

        
class MistralModel(LLM):
    def __init__(self, model: str = "mistral-large-latest"):
        super().__init__(model)

    def initialize_client(self):
        try:
            self.client = mistralai.Mistral(api_key=self.api_key)
            return None
        except Exception as e:
            return f"Error while initializing Mistral Client: {str(e)}"

    def update_history(self, prompt_to_respond = None):
        return super().update_history(prompt_to_respond)
        
    def create_answer(self) -> str:
        try:
            response = self.client.chat.complete(
            model=self.model,
            messages=self.conversation_history)
            self.answer = response.choices[0].message.content.strip()
            return self.answer
        except Exception as e:
            return f"Error with Mistral API: {str(e)}"
        
    def _add_to_history(self, prompt_to_respond=None): 
        if prompt_to_respond==None :
            self.conversation_history.append({"role": "assistant", "content": self.answer})
        else:
            self.conversation_history.append({"role": "user", "content": prompt_to_respond})

class ClaudeModel(LLM):
    def __init__(self, model: str = "claude-3-7-sonnet-20250219"):
        super().__init__(model)
        self.conversation_history = [{"role": "user", "content": "Follow your system prompt"}]

    def initialize_client(self):
        try:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            return None
        except Exception as e:
            return f"Error while initializing Claude Client: {str(e)}"
        
    def create_answer(self) -> str:
        try:
            response = self.client.messages.create(
            model=self.model,
            max_tokens=5000,
            system = self.internal_prompt if self.internal_prompt else "You are a helpful assistant.",
            messages=self.conversation_history)
            self.answer = response.content[0].text.strip()
            return self.answer
        except Exception as e:
            return f"Error with Claude API: {str(e)}"
        
    def _add_to_history(self, prompt_to_respond=None):
        if prompt_to_respond==None :
            self.conversation_history.append({"role": "assistant", "content": self.answer})
        else:
            self.conversation_history.append({"role": "user", "content": prompt_to_respond})

            
    def set_internal_prompt(self, internal_prompt):
        self.internal_prompt = internal_prompt

    def reset_history(self):
        self.conversation_history = [{"role": "user", "content": "Follow your system prompt"}]

    def update_history(self, prompt_to_respond = None):
        max_messages = self.context_window_size
        self._add_to_history(prompt_to_respond)

        if len(self.conversation_history) > max_messages:
                excess = len(self.conversation_history) - (max_messages)
                self.conversation_history = self.conversation_history[excess:]
    