"""
OpenAI provider for GPT models.
Paid API - requires OpenAI API key.
"""
import os
import httpx
from typing import List, Dict, Tuple
from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    Provider for OpenAI GPT models.
    
    Env vars:
        OPENAI_API_KEY: Your OpenAI API key (required)
        OPENAI_MODEL: Model name (default: gpt-4o-mini)
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.timeout = 60.0
    
    async def answer(self, question: str, context: str) -> Tuple[str, List[Dict]]:
        """Generate answer using OpenAI API."""
        system_prompt = (
            "You are a helpful AI assistant answering questions about a candidate's portfolio. "
            "Use ONLY the information provided in the context. "
            "Be concise, professional, and specific. "
            "If the context doesn't contain relevant information, politely say so."
        )
        
        user_prompt = f"Context:\n{context}\n\nQuestion: {question}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "temperature": 0.2,
                        "max_tokens": 400,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                )
                response.raise_for_status()
                result = response.json()
                answer_text = result["choices"][0]["message"]["content"].strip()
                
                return answer_text, []
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return "⚠️ Invalid OpenAI API key. Please check your OPENAI_API_KEY.", []
            elif e.response.status_code == 429:
                return "⚠️ OpenAI rate limit exceeded. Please try again later.", []
            else:
                return f"⚠️ OpenAI API error: {e.response.status_code}", []
        except Exception as e:
            return f"⚠️ Error connecting to OpenAI: {str(e)}", []