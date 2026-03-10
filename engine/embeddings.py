import os
import numpy as np
from sentence_transformers import SentenceTransformer
from engine.config import (
    MODEL_NAME, CACHE_DIR,
    SKILL_EMB_PATH, SKILL_LABELS_PATH, OCC_EMB_PATH
)


def load_model():
    """Load SentenceTransformer model."""
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    print("✅ Model loaded")
    return model


def load_or_generate_skill_embeddings(model, esco_skill_labels):
    """
    Load skill embeddings from cache or generate and save.
    Returns numpy array of shape (num_skills, 384).
    """
    os.makedirs(CACHE_DIR, exist_ok=True)

    if os.path.exists(SKILL_EMB_PATH) and os.path.exists(SKILL_LABELS_PATH):
        print("Loading skill embeddings from cache...")
        skill_embeddings = np.load(SKILL_EMB_PATH)
        print(f"✅ Skill embeddings loaded: {skill_embeddings.shape}")
    else:
        print("Generating skill embeddings (first run)...")
        skill_embeddings = model.encode(
            esco_skill_labels, show_progress_bar=True, batch_size=64
        )
        np.save(SKILL_EMB_PATH, skill_embeddings)
        np.save(SKILL_LABELS_PATH, np.array(esco_skill_labels, dtype=object))
        print(f"✅ Skill embeddings saved: {skill_embeddings.shape}")

    return skill_embeddings


def load_or_generate_occupation_embeddings(model, occupation_corpus):
    """
    Load occupation embeddings from cache or generate and save.
    Returns numpy array of shape (num_occupations, 384).
    """
    os.makedirs(CACHE_DIR, exist_ok=True)

    if os.path.exists(OCC_EMB_PATH):
        print("Loading occupation embeddings from cache...")
        occupation_embeddings = np.load(OCC_EMB_PATH)
        print(f"✅ Occupation embeddings loaded: {occupation_embeddings.shape}")
    else:
        print("Generating occupation embeddings (first run)...")
        occupation_embeddings = model.encode(
            occupation_corpus, show_progress_bar=True, batch_size=64
        )
        np.save(OCC_EMB_PATH, occupation_embeddings)
        print(f"✅ Occupation embeddings saved: {occupation_embeddings.shape}")

    return occupation_embeddings
