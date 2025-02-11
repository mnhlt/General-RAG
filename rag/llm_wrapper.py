from openai import OpenAI
from typing import List, Dict, Generator, Union
import logging

logger = logging.getLogger(__name__)

class DeepSeekR1:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="http://192.168.1.11:1234/v1",
            api_key=api_key,
        )
        self.model = "deepseek-r1-distill-llama-8b"
        self.provider = {"order": ["chutes", "targon"]}

    def generate(self, messages: List[Dict[str, str]], stream: bool = False) -> Union[str, Generator]:
        """
        Generate a response from the model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            stream: Whether to stream the response
            
        Returns:
            Either a string response or a generator for streaming
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream
            )
            
            if stream:
                return self._process_stream(completion)
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in generate: {str(e)}")
            logger.error(f"Messages: {messages}")
            raise

    def _process_stream(self, completion) -> Generator:
        """
        Process streaming response from the model.
        
        Args:
            completion: The streaming completion object
            
        Yields:
            Content chunks from the stream
        """
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content 