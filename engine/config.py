import os

# ── Detect environment ────────────────────────────────────
# On Railway, datasets and cache are stored in /data volume
# Locally, they are in the project folder

IS_RAILWAY = os.getenv("RAILWAY_ENVIRONMENT") is not None

if IS_RAILWAY:
    DATA_DIR    = "/data"
    DATASET_DIR = "/data/dataset"
    CACHE_DIR   = "/data/cache"
else:
    BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR    = BASE_DIR
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