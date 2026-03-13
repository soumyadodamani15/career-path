import os

# ── Detect environment ────────────────────────────────────
IS_PRODUCTION = os.getenv("RENDER") is not None

if IS_PRODUCTION:
    # On Render — datasets on persistent disk
    DATASET_DIR = "/data/dataset"
    CACHE_DIR   = "/data/cache"
else:
    # Local — datasets in project folder
    BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_DIR = os.path.join(BASE_DIR, "Dataset")
    CACHE_DIR   = os.path.join(BASE_DIR, "cache")

# ── Dataset paths ─────────────────────────────────────────
OCCUPATIONS_PATH = os.path.join(DATASET_DIR, "occupations_en.csv")
SKILLS_PATH      = os.path.join(DATASET_DIR, "skills_en.csv")
RELATIONS_PATH   = os.path.join(DATASET_DIR, "occupationSkillRelations_en.csv")
FALLBACK_PATH    = os.path.join(DATASET_DIR, "fallback_skill_map.csv")

# ── Cache paths ───────────────────────────────────────────
SKILL_EMB_PATH    = os.path.join(CACHE_DIR, "skill_embeddings.npy")
SKILL_LABELS_PATH = os.path.join(CACHE_DIR, "skill_labels.npy")
OCC_EMB_PATH      = os.path.join(CACHE_DIR, "occupation_embeddings.npy")

# ── Model ─────────────────────────────────────────────────
MODEL_NAME = "all-MiniLM-L6-v2"

# ── Pipeline ──────────────────────────────────────────────
SIMILARITY_THRESHOLD = 0.5
TOP_K_SKILL_MATCHES  = 3
FALLBACK_THRESHOLD   = 0.80
TOP_N_OCCUPATIONS    = 5

# ── Weights ───────────────────────────────────────────────
SKILL_WEIGHT      = 0.5
EXPERIENCE_WEIGHT = 0.3
INTEREST_WEIGHT   = 0.2