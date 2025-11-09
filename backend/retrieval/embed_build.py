#!/usr/bin/env python3
"""
Build vector embeddings index for RAG.
Run this once after setting up portfolio data.

Requirements:
    pip install sentence-transformers faiss-cpu

Usage:
    python retrieval/embed_build.py
"""
import json
import pathlib
import numpy as np


def build_index():
    """Build FAISS index from portfolio data."""
    
    print("=" * 60)
    print("Building Vector Index for Portfolio")
    print("=" * 60)
    
    # Paths
    ROOT = pathlib.Path(__file__).resolve().parents[1]
    DATA_PATH = ROOT / "portfolio" / "portfolio.json"
    INDEX_PATH = ROOT / "portfolio" / "pf.index"
    META_PATH = ROOT / "portfolio" / "pf.meta.json"
    
    # Check if portfolio exists
    if not DATA_PATH.exists():
        print(f"❌ Portfolio file not found: {DATA_PATH}")
        return
    
    print(f"📁 Loading portfolio from: {DATA_PATH}")
    
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            portfolio = json.load(f)
    except Exception as e:
        print(f"❌ Error loading portfolio: {e}")
        return
    
    # Create chunks
    print("\n📝 Creating text chunks...")
    chunks = []
    
    # About section
    if "about" in portfolio:
        chunks.append(("about", f"About: {portfolio['about']}"))
    
    # Skills
    if "skills" in portfolio:
        for idx, skill in enumerate(portfolio["skills"]):
            text = f"Skill: {skill.get('name', '')} - Level: {skill.get('level', '')} - Last used: {skill.get('lastUsed', '')}"
            if "category" in skill:
                text += f" - Category: {skill['category']}"
            chunks.append((f"skills:{idx}", text))
    
    # Projects
    if "projects" in portfolio:
        for idx, proj in enumerate(portfolio["projects"]):
            text = f"Project: {proj.get('name', '')}\n"
            text += f"Summary: {proj.get('summary', '')}\n"
            text += f"Stack: {', '.join(proj.get('stack', []))}\n"
            text += f"Impact: {proj.get('impact', '')}\n"
            if "highlights" in proj:
                text += f"Highlights: {' '.join(proj['highlights'])}"
            chunks.append((f"projects:{idx}", text))
    
    # Experience
    if "experience" in portfolio:
        for idx, exp in enumerate(portfolio["experience"]):
            text = f"Experience: {exp.get('role', '')} at {exp.get('company', '')}\n"
            text += f"Duration: {exp.get('duration', '')}\n"
            text += f"Description: {exp.get('description', '')}\n"
            if "achievements" in exp:
                text += f"Achievements: {' '.join(exp['achievements'])}"
            chunks.append((f"experience:{idx}", text))
    
    # Education
    if "education" in portfolio:
        for idx, edu in enumerate(portfolio["education"]):
            text = f"Education: {edu.get('degree', '')} in {edu.get('field', '')} from {edu.get('institution', '')}\n"
            text += f"Graduated: {edu.get('graduation', '')}"
            if "relevant_courses" in edu:
                text += f"\nCourses: {', '.join(edu['relevant_courses'])}"
            chunks.append((f"education:{idx}", text))
    
    # Certifications
    if "certifications" in portfolio:
        for idx, cert in enumerate(portfolio["certifications"]):
            text = f"Certification: {cert.get('name', '')} from {cert.get('issuer', '')} ({cert.get('date', '')})"
            chunks.append((f"certifications:{idx}", text))
    
    print(f"✓ Created {len(chunks)} chunks")
    
    # Load embedding model
    print("\n🤖 Loading embedding model...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("✓ Model loaded")
    except ImportError:
        print("❌ sentence-transformers not installed")
        print("   Install with: pip install sentence-transformers")
        return
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Generate embeddings
    print("\n🔢 Generating embeddings...")
    texts = [text for _, text in chunks]
    try:
        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        print(f"✓ Generated {len(embeddings)} embeddings")
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return
    
    # Build FAISS index
    print("\n📊 Building FAISS index...")
    try:
        import faiss
        
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)  # Inner product (cosine similarity)
        index.add(np.array(embeddings, dtype="float32"))
        
        # Save index
        faiss.write_index(index, str(INDEX_PATH))
        print(f"✓ Saved index to: {INDEX_PATH}")
        
        # Save metadata
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved metadata to: {META_PATH}")
        
    except ImportError:
        print("❌ faiss-cpu not installed")
        print("   Install with: pip install faiss-cpu")
        return
    except Exception as e:
        print(f"❌ Error building index: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✅ Index built successfully!")
    print("=" * 60)
    print("\nTo enable vector search, set in .env:")
    print("  ENABLE_RAG=true")
    print("\nRestart your backend to use the new index.")


if __name__ == "__main__":
    build_index()