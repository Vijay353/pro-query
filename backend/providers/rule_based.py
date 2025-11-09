"""
Rule-based provider (no LLM required).
Free fallback option using keyword matching and templates.
"""
import json
from typing import List, Dict, Tuple
from .base import BaseProvider


class RuleBasedProvider(BaseProvider):
    """
    Simple rule-based provider that doesn't require an LLM.
    Uses keyword matching to generate responses.
    Perfect for testing or as a free fallback.
    """
    
    async def answer(self, question: str, context: str) -> Tuple[str, List[Dict]]:
        """Generate rule-based answer using keyword matching."""
        q_lower = question.lower()
        
        try:
            ctx_data = json.loads(context)
        except:
            ctx_data = {}
        
        # Skills questions
        if any(word in q_lower for word in ["skill", "tech", "stack", "technology"]):
            return self._answer_skills(ctx_data, q_lower)
        
        # Projects questions
        if any(word in q_lower for word in ["project", "built", "develop", "work on"]):
            return self._answer_projects(ctx_data, q_lower)
        
        # Experience questions
        if any(word in q_lower for word in ["experience", "work", "job", "company"]):
            return self._answer_experience(ctx_data, q_lower)
        
        # Education questions
        if any(word in q_lower for word in ["education", "degree", "university", "study"]):
            return self._answer_education(ctx_data, q_lower)
        
        # Certifications
        if any(word in q_lower for word in ["certification", "certified", "cert"]):
            return self._answer_certifications(ctx_data, q_lower)
        
        # Default: general overview
        return self._answer_overview(ctx_data)
    
    def _answer_skills(self, data: Dict, question: str) -> Tuple[str, List[Dict]]:
        skills = data.get("skills", [])
        if not skills:
            return "I don't have skills information available.", []
        
        skill_list = ", ".join([s.get("name", "") for s in skills[:6]])
        categories = {}
        for s in skills:
            cat = s.get("category", "other")
            categories.setdefault(cat, []).append(s.get("name"))
        
        response = f"I have expertise in {len(skills)} technologies including {skill_list}."
        if categories:
            response += "\n\n"
            for cat, techs in categories.items():
                response += f"• {cat.title()}: {', '.join(techs[:3])}\n"
        
        return response.strip(), []
    
    def _answer_projects(self, data: Dict, question: str) -> Tuple[str, List[Dict]]:
        projects = data.get("projects", [])
        if not projects:
            return "I don't have project information available.", []
        
        links = []
        response = f"I've built {len(projects)} notable projects:\n\n"
        
        for proj in projects[:3]:
            name = proj.get("name", "Unnamed Project")
            summary = proj.get("summary", "")
            stack = ", ".join(proj.get("stack", [])[:4])
            impact = proj.get("impact", "")
            
            response += f"**{name}**\n"
            if summary:
                response += f"{summary}\n"
            if stack:
                response += f"Stack: {stack}\n"
            if impact:
                response += f"Impact: {impact}\n"
            
            if proj.get("repo"):
                links.append({"label": f"{name} - GitHub", "url": proj["repo"]})
            if proj.get("demo"):
                links.append({"label": f"{name} - Demo", "url": proj["demo"]})
            
            response += "\n"
        
        return response.strip(), links[:4]
    
    def _answer_experience(self, data: Dict, question: str) -> Tuple[str, List[Dict]]:
        experience = data.get("experience", [])
        if not experience:
            return "I don't have work experience information available.", []
        
        response = f"I have {len(experience)} professional experiences:\n\n"
        
        for exp in experience[:3]:
            company = exp.get("company", "")
            role = exp.get("role", "")
            duration = exp.get("duration", "")
            description = exp.get("description", "")
            
            response += f"**{role}** at {company}\n"
            if duration:
                response += f"{duration}\n"
            if description:
                response += f"{description}\n"
            
            achievements = exp.get("achievements", [])
            if achievements:
                response += "Key achievements:\n"
                for ach in achievements[:2]:
                    response += f"• {ach}\n"
            
            response += "\n"
        
        return response.strip(), []
    
    def _answer_education(self, data: Dict, question: str) -> Tuple[str, List[Dict]]:
        education = data.get("education", [])
        if not education:
            return "I don't have education information available.", []
        
        response = "Education:\n\n"
        
        for edu in education:
            degree = edu.get("degree", "")
            field = edu.get("field", "")
            institution = edu.get("institution", "")
            graduation = edu.get("graduation", "")
            
            response += f"**{degree} in {field}**\n"
            response += f"{institution}"
            if graduation:
                response += f" ({graduation})"
            response += "\n\n"
        
        return response.strip(), []
    
    def _answer_certifications(self, data: Dict, question: str) -> Tuple[str, List[Dict]]:
        certs = data.get("certifications", [])
        if not certs:
            return "I don't have certification information available.", []
        
        response = "Certifications:\n\n"
        links = []
        
        for cert in certs:
            name = cert.get("name", "")
            issuer = cert.get("issuer", "")
            date = cert.get("date", "")
            
            response += f"• {name}"
            if issuer:
                response += f" - {issuer}"
            if date:
                response += f" ({date})"
            response += "\n"
            
            if cert.get("url"):
                links.append({"label": name, "url": cert["url"]})
        
        return response.strip(), links[:3]
    
    def _answer_overview(self, data: Dict) -> Tuple[str, List[Dict]]:
        about = data.get("about", "")
        if about:
            return about, []
        
        # Build a quick summary
        skills_count = len(data.get("skills", []))
        projects_count = len(data.get("projects", []))
        exp_count = len(data.get("experience", []))
        
        return (
            f"I'm a professional with {exp_count} work experiences, "
            f"{projects_count} notable projects, and expertise in {skills_count} technologies. "
            "Feel free to ask about my skills, projects, or experience!"
        ), []