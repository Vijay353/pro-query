"""
FastAPI routes for retrieval and portfolio queries.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from .store import load_portfolio, select_context, extract_links

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str
    section: Optional[str] = None
    conversationId: Optional[str] = None


@router.get("/sections")
async def get_sections():
    """
    Get all portfolio sections.
    Used by frontend to display available data.
    """
    # Load fresh portfolio data
    return load_portfolio()


@router.post("/chat/context")
async def get_chat_context(body: ChatRequest):
    """
    Get relevant context for a question.
    This is used internally by the main chat endpoint.
    """
    context = select_context(body.section, body.question)
    links = extract_links(context)
    
    return {
        "context": context,
        "links": links,
        "section": body.section or "Overview"
    }