import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from engine.config import (
    SIMILARITY_THRESHOLD, TOP_K_SKILL_MATCHES, FALLBACK_THRESHOLD
)


def map_user_skills_to_esco(
    user_skills,
    esco_skill_labels,
    skill_embeddings,
    model,
    fallback_skill_map,
    threshold=SIMILARITY_THRESHOLD,
    top_k=TOP_K_SKILL_MATCHES,
    fallback_threshold=FALLBACK_THRESHOLD
):
    """
    Maps user skills to ESCO skills via semantic similarity.
    Falls back to fallback_skill_map for unknown/tool-specific terms.

    Returns:
        mapped_skills : dict {user_skill: [(esco_skill, score), ...]}
    """
    user_skill_embeddings = model.encode(user_skills, show_progress_bar=False)
    similarity_matrix     = cosine_similarity(user_skill_embeddings, skill_embeddings)
    mapped_skills         = {}

    for i, user_skill in enumerate(user_skills):
        scores       = similarity_matrix[i]
        top_indices  = np.argsort(scores)[::-1][:top_k]
        fallback_key = user_skill.lower().strip()
        matches      = []

        for idx in top_indices:
            score = scores[idx]
            if score >= threshold:
                matches.append((esco_skill_labels[idx], round(float(score), 4)))

        # Fallback Case 1: No matches above threshold
        if not matches and fallback_key in fallback_skill_map:
            fallback_skill = fallback_skill_map[fallback_key]
            matches = [(fallback_skill, 0.0)]

        # Fallback Case 2: Low quality semantic match
        elif matches and fallback_key in fallback_skill_map:
            best_score = matches[0][1]
            if best_score < fallback_threshold:
                fallback_skill = fallback_skill_map[fallback_key]
                matches = [(fallback_skill, 0.0)]

        mapped_skills[user_skill] = matches

    return mapped_skills


def collect_unique_mapped_skills(mapped_skills, user_skills_fallback=None):
    """
    Collect unique ESCO skills from mapped_skills dict.
    Falls back to raw user skills if nothing mapped.

    Returns:
        unique_mapped_skills : list of unique ESCO skill labels
    """
    seen   = set()
    unique = []

    for matches in mapped_skills.values():
        for esco_skill, _ in matches:
            if esco_skill not in seen:
                seen.add(esco_skill)
                unique.append(esco_skill)

    if not unique and user_skills_fallback:
        return user_skills_fallback

    return unique
