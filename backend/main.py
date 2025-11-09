"""
FastAPI backend for AI Portfolio.

Features:
- Auto-reload portfolio.json on file change
- Manual reload endpoint
- Multiple LLM providers
"""
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Import providers
from providers.base import BaseProvider
from providers.rule_based import RuleBasedProvider
from providers.ollama_local import OllamaProvider
from providers.openai_provider import OpenAIProvider
from providers.hf_inference import HFInferenceProvider, HFReplicateProvider

# Import retrieval
from retrieval.router import router as retrieval_router
from retrieval.store import select_context, extract_links, reload_portfolio, load_portfolio

# ========================================
# App setup
# ========================================

app = FastAPI(
    title="AI Portfolio Backend",
    description="Backend API for AI-powered portfolio with multiple LLM providers",
    version="1.0.0"
)

# CORS configuration
origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include retrieval routes
app.include_router(retrieval_router, prefix="/api")

# ========================================
# Provider factory
# ========================================

def get_provider() -> BaseProvider:
    """
    Factory function to get the configured LLM provider.
    """
    provider_name = os.getenv("PROVIDER", "ollama").lower()
    
    try:
        if provider_name == "rule_based":
            return RuleBasedProvider()
        
        elif provider_name == "ollama":
            return OllamaProvider()
        
        elif provider_name == "openai":
            return OpenAIProvider()
        
        elif provider_name == "replicate":
            return HFReplicateProvider()
        
        elif provider_name == "hf_inference":
            return HFInferenceProvider()
        
        elif provider_name == "hf_local":
            from providers.hf_local import HFLocalProvider
            return HFLocalProvider()
        
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
    
    except Exception as e:
        print(f"❌ Error initializing provider '{provider_name}': {e}")
        print("ℹ️  Falling back to rule_based provider")
        return RuleBasedProvider()


# ========================================
# Request/Response models
# ========================================

class ChatRequest(BaseModel):
    question: str
    section: Optional[str] = None
    conversationId: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    links: list[dict]
    chips: list[str]


# ========================================
# Main chat endpoint
# ========================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    provider: BaseProvider = Depends(get_provider)
):
    """
    Main chat endpoint.
    """
    try:
        # Get relevant context (auto-reloads if portfolio.json changed)
        context = select_context(body.section, body.question)
        
        # Generate answer using provider
        answer_text, provider_links = await provider.answer(body.question, context)
        
        # Extract links from context
        context_links = extract_links(context)
        
        # Combine links (prefer provider links, then context links)
        all_links = provider_links + context_links
        unique_links = []
        seen_urls = set()
        for link in all_links:
            if link["url"] not in seen_urls:
                unique_links.append(link)
                seen_urls.add(link["url"])
        
        # Create chips (section tags)
        chips = [body.section] if body.section else ["Overview"]
        
        return ChatResponse(
            answer=answer_text,
            links=unique_links[:4],
            chips=chips
        )
    
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


# ========================================
# Reload endpoint - NEW!
# ========================================

@app.post("/api/reload")
async def reload():
    """
    Manually reload portfolio data.
    Visit: http://localhost:8000/api/reload
    """
    try:
        portfolio_data = reload_portfolio()
        return {
            "status": "success",
            "message": "Portfolio data reloaded",
            "sections": list(portfolio_data.keys()),
            "timestamp": os.path.getmtime("portfolio/portfolio.json")
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reloading portfolio: {str(e)}"
        )


# ========================================
# Health check
# ========================================

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    provider_name = os.getenv("PROVIDER", "ollama")
    portfolio_data = load_portfolio()
    
    return {
        "status": "ok",
        "provider": provider_name,
        "rag_enabled": os.getenv("ENABLE_RAG", "false"),
        "portfolio_sections": list(portfolio_data.keys()) if portfolio_data else [],
        "timeout": os.getenv("OLLAMA_TIMEOUT", "120")
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "AI Portfolio Backend",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "sections": "/api/sections",
            "health": "/api/health",
            "reload": "/api/reload (POST)"
        },
        "provider": os.getenv("PROVIDER", "ollama"),
        "docs": "/docs",
        "features": [
            "Auto-reload portfolio on file change",
            "Manual reload via /api/reload",
            "Multiple LLM providers",
            "Optional RAG support"
        ]
    }


# ========================================
# Startup event
# ========================================

@app.on_event("startup")
async def startup_event():
    """Print startup information."""
    provider_name = os.getenv("PROVIDER", "ollama")
    rag_enabled = os.getenv("ENABLE_RAG", "false")
    timeout = os.getenv("OLLAMA_TIMEOUT", "120")
    
    print("\n" + "=" * 60)
    print("🚀 AI Portfolio Backend Started")
    print("=" * 60)
    print(f"Provider: {provider_name}")
    print(f"RAG Enabled: {rag_enabled}")
    print(f"Timeout: {timeout}s")
    print(f"CORS Origins: {os.getenv('CORS_ORIGINS', '*')}")
    print(f"Auto-reload: ✅ Enabled")
    print("=" * 60 + "\n")
    
    # Load portfolio on startup
    portfolio_data = load_portfolio()
    print(f"📦 Loaded {len(portfolio_data)} portfolio sections")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )