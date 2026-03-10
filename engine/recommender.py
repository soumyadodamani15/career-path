import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from engine.config import (
    TOP_N_OCCUPATIONS,
    SKILL_WEIGHT, EXPERIENCE_WEIGHT, INTEREST_WEIGHT,
    SIMILARITY_THRESHOLD
)


def build_user_profile_embedding(
    mapped_esco_skills,
    experience,
    interests,
    model,
    skill_weight=SKILL_WEIGHT,
    experience_weight=EXPERIENCE_WEIGHT,
    interest_weight=INTEREST_WEIGHT
):
    """
    Builds weighted profile embedding from skills, experience and interests.
    Returns numpy array of shape (1, 384).
    """
    skills_text     = "Skills and competences: " + ", ".join(mapped_esco_skills)
    experience_text = "Work experience: " + experience
    interests_text  = "Professional interests: " + ", ".join(interests)

    skills_emb     = model.encode([skills_text])[0]
    experience_emb = model.encode([experience_text])[0]
    interests_emb  = model.encode([interests_text])[0]

    weighted_emb = (
        skill_weight      * skills_emb +
        experience_weight * experience_emb +
        interest_weight   * interests_emb
    )

    return weighted_emb.reshape(1, -1)


def rank_occupations(
    user_profile_embedding,
    occupation_embeddings,
    occupation_labels,
    occupation_uris,
    top_n=TOP_N_OCCUPATIONS
):
    """
    Ranks occupations by cosine similarity to user profile.
    Returns list of top_n occupation dicts.
    """
    similarities = cosine_similarity(
        user_profile_embedding, occupation_embeddings
    )[0]
    top_indices  = np.argsort(similarities)[::-1][:top_n]

    results = []
    for rank, idx in enumerate(top_indices, 1):
        results.append({
            "rank":             rank,
            "occupation":       occupation_labels[idx],
            "uri":              occupation_uris[idx],
            "similarity_score": round(float(similarities[idx]), 4)
        })

    return results


def skill_gap_analysis(
    top_occupation,
    essential_skills_map,
    unique_mapped_skills,
    model,
    top_n=5
):
    """
    For the given occupation:
    - Retrieve essential skills
    - Compare with user mapped skills
    - Return matched and missing essential skills

    Returns dict with matched_skills and missing_skills.
    """
    top_uri          = top_occupation["uri"]
    top_label        = top_occupation["occupation"]
    essential_skills = essential_skills_map.get(top_uri, [])

    if not essential_skills:
        return {
            "occupation":      top_label,
            "uri":             top_uri,
            "total_essential": 0,
            "matched_skills":  [],
            "missing_skills":  []
        }

    # Embed essential skills and user skills
    essential_embeddings  = model.encode(essential_skills, show_progress_bar=False)
    user_skill_embeddings = model.encode(unique_mapped_skills, show_progress_bar=False)

    # Cosine similarity matrix
    match_matrix = cosine_similarity(essential_embeddings, user_skill_embeddings)

    matched = []
    missing = []

    for i, ess_skill in enumerate(essential_skills):
        best_score      = float(np.max(match_matrix[i]))
        best_user_skill = unique_mapped_skills[int(np.argmax(match_matrix[i]))]

        if best_score >= SIMILARITY_THRESHOLD:
            matched.append({
                "essential_skill": ess_skill,
                "matched_by":      best_user_skill,
                "score":           round(best_score, 4)
            })
        else:
            missing.append({
                "essential_skill": ess_skill,
                "score":           round(best_score, 4)
            })

    # Sort matched by score desc, missing by score asc
    matched.sort(key=lambda x: x["score"], reverse=True)
    missing.sort(key=lambda x: x["score"])

    return {
        "occupation":      top_label,
        "uri":             top_uri,
        "total_essential": len(essential_skills),
        "matched_skills":  matched[:top_n],
        "missing_skills":  missing[:top_n]
    }
