"""
Ollama local provider - Optimized for speed and reliability.
"""
import os
import httpx
from typing import List, Dict, Tuple
from .base import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Provider for local Ollama models.
    
    Requires:
        - Ollama installed and running (ollama serve)
        - Model pulled (e.g., ollama pull llama3.2)
    
    Env vars:
        OLLAMA_HOST: Host URL (default: http://localhost:11434)
        OLLAMA_MODEL: Model name (default: llama3.2)
        OLLAMA_TIMEOUT: Timeout in seconds (default: 120)
    """
    
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        # Increased timeout - first request can be slow
        self.timeout = float(os.getenv("OLLAMA_TIMEOUT", "120"))
        print(f"✅ Ollama: {self.host} | Model: {self.model} | Timeout: {self.timeout}s")
    
    async def answer(self, question: str, context: str) -> Tuple[str, List[Dict]]:
        """Generate answer using local Ollama model."""
        # Limit context size to avoid timeouts
        max_context = 2000  # characters
        if len(context) > max_context:
            context = context[:max_context] + "..."
            print(f"⚠️  Context truncated to {max_context} chars")
        
        prompt = self._build_prompt(question, context)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                print(f"🚀 Sending to Ollama... (timeout: {self.timeout}s)")
                
                response = await client.post(
                    f"{self.host}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 300,  # Reduced for speed
                            "top_k": 40,
                            "top_p": 0.9,
                        }
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer_text = result.get("response", "").strip()
                    
                    if answer_text:
                        print(f"✅ Got response ({len(answer_text)} chars)")
                        return answer_text, []
                    else:
                        return "I received an empty response. Please try again.", []
                
                elif response.status_code == 404:
                    # Try without tag
                    base_model = self.model.split(':')[0]
                    print(f"🔄 Retrying with model: {base_model}")
                    
                    response = await client.post(
                        f"{self.host}/api/generate",
                        json={
                            "model": base_model,
                            "prompt": prompt,
                            "stream": False,
                            "options": {
                                "temperature": 0.3,
                                "num_predict": 300,
                            }
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer_text = result.get("response", "").strip()
                        if answer_text:
                            self.model = base_model  # Update for next time
                            print(f"✅ Success with {base_model}")
                            return answer_text, []
                
                return f"⚠️ Ollama error (status {response.status_code})", []
                    
        except httpx.ConnectError:
            return (
                "⚠️ Cannot connect to Ollama. Make sure it's running:\n"
                "1. Run: ollama serve\n"
                "2. Check: curl http://localhost:11434/api/tags"
            ), []
            
        except httpx.TimeoutException:
            return (
                f"⚠️ Request timed out after {self.timeout}s. This can happen on first request.\n\n"
                "Solutions:\n"
                "1. Try again (first request loads model into memory)\n"
                "2. Increase timeout in .env: OLLAMA_TIMEOUT=180\n"
                "3. Use a smaller model: ollama pull llama3.2:1b\n"
                "4. Make sure you have enough RAM (4GB+ recommended)"
            ), []
            
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {e}")
            return f"⚠️ Error: {str(e)}", []
    
    def _build_prompt(self, question: str, context: str) -> str:
        """Build concise prompt for faster responses."""
        return (
            "Answer this question about a candidate using only the context below. "
            "Be brief and specific.\n\n"
            f"Context: {context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )