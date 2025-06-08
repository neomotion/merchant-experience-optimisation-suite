# This module is for multimodal inputs with multiple images.

import os
import boto3
import json
from openai import AzureOpenAI
from handlers.logger import logger
from retry_logic import retry_with_exponential_backoff


class BaseModelClient:
    """Base class for all model clients"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.last_token_usage = 0
        self.last_completion_token_usage = 0
        self.last_prompt_token_usage = 0

    def send_request(self, prompt: str, image_base64: str = None) -> str:
        """Send request to model with optional image support"""
        raise NotImplementedError("Subclasses must implement send_request")

    def get_token_usage(self) -> int:
        """Get token usage from last request"""
        return self.last_token_usage


class AzureOpenAIClient(BaseModelClient):
    """Client for Azure OpenAI models"""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        try:
            self.client = AzureOpenAI(
                azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
                api_key=os.environ.get("AZURE_OPENAI_KEY"),
                api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
            )
            self.deployment_name = model_name  # Make sure model_name is stored as deployment_name
            logger.info(f"Initialized Azure OpenAI client for deployment {model_name}")
        except ImportError:
            logger.error("azure-openai package not installed. Install with: pip install openai>=1.0.0")
            raise
        except Exception as e:
            logger.error(f"Error initializing Azure OpenAI client: {str(e)}")
            raise

    # @retry_with_exponential_backoff(max_retries=5, initial_delay=2, max_delay=120)
    def send_request(self, prompt: str, images_base64: List[str] = None) -> str:
        """
        Sends the prompt to Azure OpenAI and returns the completion.
        Supports multimodal inputs with multiple images in a single request.
        """
        if images_base64 and len(images_base64) > 0:
            # For multimodal requests with one or more images
            content = [{"type": "text", "text": prompt}]

            # Add images to the content
            for idx, img_base64 in enumerate(images_base64):
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_base64}"
                    }
                })
            
            messages = [{"role": "user", "content": content}]
            else:
                # For text-only requests
                messages = [{"role": "user", "content": prompt}]
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.3,
            )
            self.last_token_usage = response.usage.total_tokens
            self.last_completion_token_usage = response.usage.completion_tokens
            self.last_prompt_token_usage = response.usage.prompt_tokens
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling Azure OpenAI: {str(e)}")
            return f"AzureOpenAI Error: {str(e)}"


class AWSBedrockClient(BaseModelClient):
    """Client for AWS Bedrock models"""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        try:
            self.client = boto3.client('bedrock-runtime', region_name='ap-south-1')
            logger.info(f"Initialized AWS Bedrock client for model {model_name}")
        except ImportError:
            logger.error("boto3 package not installed. Install with: pip install boto3")
            raise
        except Exception as e:
            logger.error(f"Error initializing AWS Bedrock client: {str(e)}")
            raise

    def send_request(self, prompt: str, images_base64: List[str] = None) -> str:
        """
        Sends the prompt to an AWS Bedrock model (like Claude) with image support.
        """
        if images_base64 and len(images_base64) > 0 and "claude" in self.model_name.lower():
            # For Claude models with image support
            content = [{"type": "text", "text": prompt}]
            
            # Add all images to the content array
            for img_base64 in images_base64:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": img_base64
                    }
                })
            
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": 0.3,
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            }
        else:
            # Standard text-only payload
            payload = {
                "prompt": prompt,
                "temperature": 0.3,
                "max_tokens_to_sample": 1024,
                "stop_sequences": [],
            }

        try:
            response = self.client.invoke_model(
                body=json.dumps(payload),
                modelId=self.model_name,
                contentType="application/json",
                accept="application/json",
            )
            response_body = json.loads(response["body"].read())
            
            # Handle different response formats based on model
            if "claude" in self.model_name.lower() and "messages" in payload:
                self.last_token_usage = response_body.get("usage", {}).get("total_tokens", 0)
                return response_body.get("content", [{}])[0].get("text", "")
            else:
                return response_body.get("completion", "").strip()
        except Exception as e:
            return f"AWSBedrock Error: {str(e)}"


class GeminiClient(BaseModelClient):
    """Client for Google's Gemini models"""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        try:
            # Initialize Gemini with API key
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"Initialized Gemini client for model {model_name}")
        except ImportError:
            logger.error("google-generativeai package not installed. Install with: pip install google-generativeai")
            raise
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {str(e)}")
            raise

    def send_request(self, prompt: str, images_base64: List[str] = None) -> str:
        """
        Sends the prompt to Gemini model and returns the completion.
        Supports multimodal inputs with images.
        """
        try:
            if images_base64 and len(images_base64) > 0 and "gemini" in self.model_name.lower():
                # For multimodal requests with images
                image_data = {
                    "mime_type": "image/jpeg",
                    "data": image_base64
                }
                response = self.model.generate_content(
                    contents=[prompt, image_data],
                    generation_config={
                        "temperature": 0.3,
                        "max_output_tokens": 4000,
                    }
                )
            else:
                # For text-only requests
                response = self.model.generate_content(
                    contents=prompt,
                    generation_config={
                        "temperature": 0.3,
                        "max_output_tokens": 4000,
                    }
                )
            
            # Update token usage (Gemini doesn't provide exact token counts)
            self.last_token_usage = len(prompt.split()) + len(response.text.split())
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error calling Gemini: {str(e)}")
            return f"Gemini Error: {str(e)}"


def create_model_client(model_name: str) -> BaseModelClient:
    """
    Factory function to create appropriate model client

    Args:
        model_name: Name of the model

    Returns:
        Appropriate model client instance
    """
    if model_name.startswith("Azure-gpt-"):
        return AzureOpenAIClient(model_name)
    elif model_name.startswith("Bedrock-claude") or model_name.startswith("AWS-claude"):
        return AWSBedrockClient(model_name)
    elif model_name.startswith("gemini-"):
        return GeminiClient(model_name)
    else:
        raise ValueError(f"Unknown model type: {model_name}")
