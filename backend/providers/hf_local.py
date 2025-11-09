"""
HuggingFace local transformers provider.
Runs models locally on your GPU/CPU (no API calls).
"""
import os
import asyncio
from typing import List, Dict, Tuple
from .base import BaseProvider


class HFLocalProvider(BaseProvider):
    """
    Provider for running HuggingFace models locally.
    
    Requires:
        pip install transformers torch
    
    Env vars:
        HF_MODEL: Model name (default: meta-llama/Llama-3.2-3B-Instruct)
        HF_DEVICE: Device to use (auto, cuda, cpu, mps)
    
    First run will download the model (~6GB for Llama 3.2 3B).
    After that, it runs entirely locally with no internet needed.
    """
    
    def __init__(self):
        self.model_name = os.getenv("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
        self.device = os.getenv("HF_DEVICE", "auto")
        
        print(f"Loading HuggingFace model: {self.model_name}")
        print(f"Device: {self.device}")
        print("(First run will download model, please wait...)")
        
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Load model with pipeline
            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                tokenizer=self.tokenizer,
                device_map=self.device,
                torch_dtype="auto",
                trust_remote_code=True
            )
            
            print("✓ Model loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    async def answer(self, question: str, context: str) -> Tuple[str, List[Dict]]:
        """Generate answer using local HuggingFace model."""
        prompt = self._build_hf_prompt(question, context)
        
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            output = await loop.run_in_executor(
                None,
                self._generate,
                prompt
            )
            
            # Extract generated text
            if isinstance(output, list) and len(output) > 0:
                generated_text = output[0].get("generated_text", "")
            else:
                generated_text = str(output)
            
            # Remove prompt from output
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            # Clean up
            answer_text = generated_text.strip()
            
            if not answer_text:
                return "I couldn't generate a response. Please try again.", []
            
            return answer_text, []
            
        except Exception as e:
            return f"⚠️ Error generating response: {str(e)}", []
    
    def _generate(self, prompt: str) -> list:
        """Synchronous generation (called in thread pool)."""
        return self.pipe(
            prompt,
            max_new_tokens=400,
            temperature=0.3,
            top_p=0.9,
            do_sample=True,
            return_full_text=False
        )
    
    def _build_hf_prompt(self, question: str, context: str) -> str:
        """Build prompt for HuggingFace instruction models."""
        return (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            "You are a helpful AI assistant answering questions about a candidate's portfolio. "
            "Use only the provided context. Be concise and professional."
            "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}"
            "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        )