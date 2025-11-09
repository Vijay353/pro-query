"""
Central retrieval store with keyword and optional vector search.
AUTO-RELOADS portfolio.json when file changes!
"""
import json
import pathlib
import os
from typing import List, Dict
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
PORTFOLIO_PATH = ROOT / "portfolio" / "portfolio.json"
INDEX_PATH = ROOT / "portfolio" / "pf.index"
META_PATH = ROOT / "portfolio" / "pf.meta.json"

# Cache for portfolio data with timestamp
_portfolio_cache = {
    "data": None,
    "last_modified": 0
}


def load_portfolio() -> dict:
    """
    Load portfolio with auto-reload on file change.
    No restart needed when you update portfolio.json!
    """
    global _portfolio_cache
    
    try:
        # Get current file modification time
        current_mtime = PORTFOLIO_PATH.stat().st_mtime
        
        # Reload if file changed or not loaded yet
        if _portfolio_cache["data"] is None or current_mtime > _portfolio_cache["last_modified"]:
            with open(PORTFOLIO_PATH, encoding="utf-8") as f:
                _portfolio_cache["data"] = json.load(f)
                _portfolio_cache["last_modified"] = current_mtime
                print(f"🔄 Portfolio reloaded at {datetime.now().strftime('%H:%M:%S')}")
        
        return _portfolio_cache["data"]
    
    except Exception as e:
        print(f"❌ Error loading portfolio: {e}")
        return {}


# Use function instead of loading once
portfolio = property(lambda self: load_portfolio())


# ========================================
# Keyword-based retrieval (always works)
# ========================================

def keyword_context(section: str | None, question: str) -> str:
    """
    Route to appropriate context based on section or keywords.
    Fast and works without any setup.
    """
    # Get fresh portfolio data
    portfolio_data = load_portfolio()
    
    q = question.lower()
    
    # Section-based routing
    if section == "PROJECTS" or any(word in q for word in ["project", "built", "develop"]):
        return json.dumps(portfolio_data.get("projects", []), ensure_ascii=False, indent=2)
    
    if section == "SKILLS" or any(word in q for word in ["stack", "skill", "tech", "language", "framework"]):
        return json.dumps(portfolio_data.get("skills", []), ensure_ascii=False, indent=2)
    
    if section == "EXPERIENCE" or any(word in q for word in ["work", "job", "company", "experience", "role"]):
        return json.dumps(portfolio_data.get("experience", []), ensure_ascii=False, indent=2)
    
    if section == "EDUCATION" or any(word in q for word in ["degree", "university", "education", "study", "college"]):
        return json.dumps(portfolio_data.get("education", []), ensure_ascii=False, indent=2)
    
    if section == "CERTIFICATIONS" or any(word in q for word in ["cert", "certification", "certified"]):
        return json.dumps(portfolio_data.get("certifications", []), ensure_ascii=False, indent=2)
    
    # Default: return everything
    return json.dumps(portfolio_data, ensure_ascii=False, indent=2)


# ========================================
# Vector-based retrieval (optional, better)
# ========================================

class DenseRetriever:
    """
    Dense retrieval using sentence-transformers + FAISS.
    Only loads if index files exist.
    """
    
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            
            self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            self.index = faiss.read_index(str(INDEX_PATH))
            
            with open(META_PATH, encoding="utf-8") as f:
                self.chunks = json.load(f)  # List of (id, text) tuples
            
            print(f"✓ Loaded vector index with {len(self.chunks)} chunks")
            
        except Exception as e:
            print(f"⚠ Could not load vector index: {e}")
            raise
    
    def search(self, question: str, top_k: int = 5) -> str:
        """
        Find most relevant chunks using semantic search.
        Returns concatenated context string.
        """
        # Encode query
        query_embedding = self.model.encode(
            [question], 
            normalize_embeddings=True
        )
        
        # Search index
        scores, indices = self.index.search(query_embedding, top_k)
        
        # Get matching chunks
        selected_chunks = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                chunk_id, chunk_text = self.chunks[idx]
                selected_chunks.append(chunk_text)
        
        return "\n\n".join(selected_chunks)


# Global instance (lazy loaded)
_dense_retriever = None

def dense_context(question: str, top_k: int = 5) -> str:
    """
    Get context using vector search.
    Returns empty string if index doesn't exist.
    """
    global _dense_retriever
    
    # Check if index exists
    if not INDEX_PATH.exists() or not META_PATH.exists():
        return ""
    
    # Lazy load retriever
    if _dense_retriever is None:
        try:
            _dense_retriever = DenseRetriever()
        except Exception:
            return ""
    
    try:
        return _dense_retriever.search(question, top_k)
    except Exception as e:
        print(f"⚠ Vector search error: {e}")
        return ""


# ========================================
# Public API
# ========================================

def select_context(section: str | None, question: str) -> str:
    """
    Main entry point for context selection.
    
    Priority:
    1. Try vector search (if index exists)
    2. Fall back to keyword matching
    
    Args:
        section: Optional section filter (PROJECTS, SKILLS, etc.)
        question: User's question
    
    Returns:
        Relevant context as JSON string
    """
    # Try vector search first
    if os.getenv("ENABLE_RAG", "false").lower() == "true":
        vector_context = dense_context(question)
        if vector_context:
            print("✓ Using vector search")
            return vector_context
    
    # Fall back to keyword matching
    print("✓ Using keyword matching")
    return keyword_context(section, question)


def extract_links(context: str) -> List[Dict[str, str]]:
    """
    Extract links from context JSON.
    Returns list of {label, url} dicts.
    """
    try:
        data = json.loads(context)
        links = []
        
        # Handle list of items (projects, etc.)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    # Projects have repo and demo links
                    if "repo" in item:
                        name = item.get("name", "Project")
                        links.append({
                            "label": f"{name} - GitHub",
                            "url": item["repo"]
                        })
                    if "demo" in item:
                        name = item.get("name", "Project")
                        links.append({
                            "label": f"{name} - Live Demo",
                            "url": item["demo"]
                        })
                    # Certifications have URLs
                    if "url" in item and "name" in item:
                        links.append({
                            "label": item["name"],
                            "url": item["url"]
                        })
        
        # Limit to 4 links
        return links[:4]
    
    except Exception:
        return []


# ========================================
# Manual reload function (if needed)
# ========================================

def reload_portfolio():
    """
    Force reload portfolio data.
    Useful if you want to manually refresh.
    """
    global _portfolio_cache
    _portfolio_cache["last_modified"] = 0
    return load_portfolio()