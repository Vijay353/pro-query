"""
Base provider interface for all LLM providers.
All providers must implement the answer() method.
"""
import abc
from typing import List, Dict, Tuple


class BaseProvider(abc.ABC):
    """
    Abstract base class for all LLM providers.
    
    Returns:
        Tuple[str, List[Dict]]: (answer_text, links)
        - answer_text: The generated response
        - links: List of relevant links (can be empty)
    """
    
    @abc.abstractmethod
    async def answer(self, question: str, context: str) -> Tuple[str, List[Dict]]:
        """
        Generate an answer based on the question and context.
        
        Args:
            question: The user's question
            context: Relevant context from portfolio data
            
        Returns:
            Tuple of (answer_text, links_list)
        """
        pass
    
    def _build_prompt(self, question: str, context: str) -> str:
        """
        Helper method to build a consistent prompt format.
        Can be overridden by subclasses if needed.
        """
        return (
            "You are a helpful AI assistant answering questions about a candidate's portfolio. "
            "Use ONLY the information provided in the context below. "
            "Be concise, professional, and include specific details from the context. "
            "If the context doesn't contain relevant information, politely say so.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )