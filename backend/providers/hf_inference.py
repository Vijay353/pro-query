"""
HuggingFace Inference API provider.
Free tier available, can also train custom models.
"""
import os
import httpx
import asyncio
from typing import List, Dict, Tuple
from .base import BaseProvider


class HFInferenceProvider(BaseProvider):
    """
    Provider for HuggingFace Inference API (serverless).
    
    Env vars:
        HF_API_KEY: HuggingFace token (optional for public models)
        HF_MODEL: Model name (default: meta-llama/Llama-3.2-3B-Instruct)
    
    Supports:
        - Free tier for public models
        - Custom fine-tuned models
        - Any model on HuggingFace Hub
    """
    
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.model = os.getenv("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
        self.timeout = 120.0  # HF can be slow on cold start
        
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    async def answer(self, question: str, context: str) -> Tuple[str, List[Dict]]:
        """Generate answer using HuggingFace Inference API."""
        prompt = self._build_hf_prompt(question, context)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 400,
                "temperature": 0.3,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        answer_text = result[0]["generated_text"]
                    else:
                        answer_text = str(result[0])
                elif isinstance(result, dict) and "generated_text" in result:
                    answer_text = result["generated_text"]
                else:
                    answer_text = str(result)
                
                # Clean up the response
                answer_text = answer_text.strip()
                
                # Remove the prompt if it's included in response
                if answer_text.startswith(prompt):
                    answer_text = answer_text[len(prompt):].strip()
                
                if not answer_text:
                    return "I couldn't generate a response. Please try again.", []
                
                return answer_text, []
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 503:
                # Model is loading
                return (
                    "⚠️ The model is loading. This can take 20-30 seconds on first request. "
                    "Please try again in a moment."
                ), []
            elif e.response.status_code == 401:
                return "⚠️ Invalid HuggingFace API key. Please check your HF_API_KEY.", []
            elif e.response.status_code == 429:
                return "⚠️ Rate limit exceeded. Please try again later.", []
            else:
                return f"⚠️ HuggingFace API error: {e.response.status_code}", []
        except httpx.TimeoutException:
            return (
                "⚠️ Request timed out. The model might be loading. "
                "Please try again in a moment."
            ), []
        except Exception as e:
            return f"⚠️ Error connecting to HuggingFace: {str(e)}", []
    
    def _build_hf_prompt(self, question: str, context: str) -> str:
        """Build prompt optimized for HuggingFace models."""
        # Format for instruction-tuned models
        return (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            "You are a helpful AI assistant answering questions about a candidate's portfolio. "
            "Use only the provided context. Be concise and professional."
            "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}"
            "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        )


class HFReplicateProvider(BaseProvider):
    """
    Provider for Replicate API (for llama-3.1-70B and other large models).
    
    Env vars:
        REPLICATE_API_TOKEN: Your Replicate API token (required)
        REPLICATE_MODEL: Model name (default: meta/meta-llama-3.1-70b-instruct)
    """
    
    def __init__(self):
        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN environment variable is required")
        
        self.model = os.getenv(
            "REPLICATE_MODEL", 
            "meta/meta-llama-3.1-70b-instruct"
        )
        self.timeout = 120.0
    
    async def answer(self, question: str, context: str) -> Tuple[str, List[Dict]]:
        """Generate answer using Replicate API."""
        prompt = self._build_prompt(question, context)
        
        headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "version": self.model,
            "input": {
                "prompt": prompt,
                "temperature": 0.2,
                "max_tokens": 400,
                "top_p": 0.9
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Start prediction
                response = await client.post(
                    "https://api.replicate.com/v1/predictions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                prediction = response.json()
                prediction_url = prediction["urls"]["get"]
                
                # Poll for completion
                max_attempts = 60
                for _ in range(max_attempts):
                    await asyncio.sleep(2)
                    
                    poll_response = await client.get(
                        prediction_url,
                        headers=headers
                    )
                    poll_response.raise_for_status()
                    result = poll_response.json()
                    
                    status = result["status"]
                    
                    if status == "succeeded":
                        output = result.get("output", [])
                        if isinstance(output, list):
                            answer_text = "".join(output).strip()
                        else:
                            answer_text = str(output).strip()
                        
                        return answer_text, []
                    
                    elif status in ("failed", "cancelled"):
                        error = result.get("error", "Unknown error")
                        return f"⚠️ Replicate prediction failed: {error}", []
                
                return "⚠️ Request timed out waiting for Replicate response.", []
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return "⚠️ Invalid Replicate API token. Please check your REPLICATE_API_TOKEN.", []
            elif e.response.status_code == 429:
                return "⚠️ Rate limit exceeded. Please try again later.", []
            else:
                return f"⚠️ Replicate API error: {e.response.status_code}", []
        except Exception as e:
            return f"⚠️ Error connecting to Replicate: {str(e)}", []