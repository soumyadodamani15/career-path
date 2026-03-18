from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from api.state import app_state
from pydantic import BaseModel
from typing import Optional
from engine.roadmap_generator import generate_roadmap

router = APIRouter()


# ── Request Model ─────────────────────────────────────────
class CareerRequest(BaseModel):
    skills:     List[str] = Field(..., min_items=1, max_items=20, description="List of user skills")
    experience: str       = Field(..., min_length=5, max_length=500, description="One sentence about experience")
    interests:  List[str] = Field(..., min_items=1, max_items=10, description="List of interests")

    class Config:
        json_schema_extra = {
            "example": {
                "skills":     ["Python", "data analysis", "machine learning"],
                "experience": "3 years working as a data analyst in the finance industry",
                "interests":  ["artificial intelligence", "automation", "statistics"]
            }
        }
class WeakSkill(BaseModel):
    skill: str
    score: float

class MissingSkill(BaseModel):
    skill: str

class RoadmapRequest(BaseModel):
    target_occupation: str
    weak_skills: list[WeakSkill] = []
    missing_skills: list[MissingSkill] = []
    strong_skills: list[str] = []

# ── Health Check ──────────────────────────────────────────
@router.get("/health")
def health_check():
    return {
        "status":  "ok",
        "message": "Career Recommendation Engine is running"
    }


# ── Main Recommendation Endpoint ─────────────────────────
@router.post("/betaRecommendation")
def recommend_careers(request: CareerRequest):
    """
    Returns top 5 career recommendations and skill gap analysis
    based on user skills, experience and interests.
    """
    try:
        from engine.pipeline import run_pipeline

        result = run_pipeline(
            user_skills          = request.skills,
            user_experience      = request.experience,
            user_interests       = request.interests,
            model                = app_state["model"],
            esco_skill_labels    = app_state["esco_skill_labels"],
            skill_embeddings     = app_state["skill_embeddings"],
            occupation_embeddings= app_state["occupation_embeddings"],
            occupation_labels    = app_state["occupation_labels"],
            occupation_uris      = app_state["occupation_uris"],
            essential_skills_map = app_state["essential_skills_map"],
            fallback_skill_map   = app_state["fallback_skill_map"]
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Reload Fallback Map Endpoint ──────────────────────────
@router.post("/admin/reload-fallback")
def reload_fallback():
    """
    Reloads fallback_skill_map.csv without restarting the server.
    Useful when new skills are added to the CSV.
    """
    try:
        from engine.data_loader import load_fallback_skill_map
        app_state["fallback_skill_map"] = load_fallback_skill_map()
        return {
            "status":  "ok",
            "message": f"Fallback map reloaded: {len(app_state['fallback_skill_map'])} entries"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.post("/careerRoadmap")
def career_roadmap(request: RoadmapRequest):
    """Generate a personalized career learning roadmap."""
    try:
        roadmap = generate_roadmap(
            target_occupation=request.target_occupation,
            weak_skills=[s.dict() for s in request.weak_skills],
            missing_skills=[s.dict() for s in request.missing_skills],
            strong_skills=request.strong_skills
        )
        return roadmap
    except Exception as e:
        return {"error": str(e)}