import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from engine.data_loader import (
    load_datasets,
    build_skill_maps,
    build_occupation_corpus,
    load_fallback_skill_map
)
from engine.embeddings import (
    load_model,
    load_or_generate_skill_embeddings,
    load_or_generate_occupation_embeddings
)
from api.state import app_state
from api.routes import router


# ── Startup & Shutdown ────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print("CAREER ENGINE — STARTUP")
    print("=" * 60)

    # ── Check datasets exist ──────────────────────────────
    from engine.config import OCCUPATIONS_PATH, SKILLS_PATH, RELATIONS_PATH
    missing = []
    for path in [OCCUPATIONS_PATH, SKILLS_PATH, RELATIONS_PATH]:
        if not os.path.exists(path):
            missing.append(path)

    if missing:
        print("❌ Missing dataset files:")
        for f in missing:
            print(f"   {f}")
        print("\nPlease upload datasets to Railway volume at /data/dataset/")
        raise FileNotFoundError(f"Missing datasets: {missing}")

    # rest of startup continues...
    print("\n[1/5] Loading datasets...")
    occupations_df, skills_df, relations_df = load_datasets()
    print(f"   Occupations : {len(occupations_df)}")
    print(f"   Skills      : {len(skills_df)}")
    print(f"   Relations   : {len(relations_df)}")

    # Build skill maps
    print("\n[2/5] Building skill maps...")
    essential_skills_map, all_skills_map = build_skill_maps(relations_df)
    print(f"   Essential skills map : {len(essential_skills_map)} occupations")

    # Build occupation corpus
    print("\n[3/5] Building occupation corpus...")
    occupation_corpus, occupation_uris, occupation_labels = build_occupation_corpus(
        occupations_df, all_skills_map
    )
    print(f"   Corpus size : {len(occupation_corpus)}")

    # Load model and embeddings
    print("\n[4/5] Loading model and embeddings...")
    model            = load_model()
    esco_skill_labels = skills_df["preferredLabel"].fillna("").tolist()
    skill_embeddings  = load_or_generate_skill_embeddings(model, esco_skill_labels)
    occupation_embeddings = load_or_generate_occupation_embeddings(model, occupation_corpus)

    # Load fallback skill map
    print("\n[5/5] Loading fallback skill map...")
    fallback_skill_map = load_fallback_skill_map()
    print(f"   Fallback entries : {len(fallback_skill_map)}")

    # Store everything in shared state
    app_state.update({
        "model":                 model,
        "esco_skill_labels":     esco_skill_labels,
        "skill_embeddings":      skill_embeddings,
        "occupation_embeddings": occupation_embeddings,
        "occupation_labels":     occupation_labels,
        "occupation_uris":       occupation_uris,
        "essential_skills_map":  essential_skills_map,
        "fallback_skill_map":    fallback_skill_map
    })

    print("\n" + "=" * 60)
    print("✅ Career Engine ready!")
    print("=" * 60)

    yield

    # Cleanup on shutdown
    app_state.clear()
    print("Career Engine shut down.")


# ── FastAPI App ───────────────────────────────────────────
app = FastAPI(
    title       = "Career Recommendation Engine",
    description = "Semantic career recommendation and skill gap analysis using ESCO dataset",
    version     = "1.0.0",
    lifespan    = lifespan
)

app.include_router(router, prefix="/api/v1")


# ── Root ──────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "name":    "Career Recommendation Engine",
        "version": "1.0.0",
        "docs":    "/docs",
        "health":  "/api/v1/health"
    }
