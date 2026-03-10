from engine.skill_mapper import map_user_skills_to_esco, collect_unique_mapped_skills
from engine.recommender import build_user_profile_embedding, rank_occupations, skill_gap_analysis


def run_pipeline(
    user_skills,
    user_experience,
    user_interests,
    model,
    esco_skill_labels,
    skill_embeddings,
    occupation_embeddings,
    occupation_labels,
    occupation_uris,
    essential_skills_map,
    fallback_skill_map
):
    """
    Full end-to-end career recommendation pipeline.

    Returns:
        dict with:
            - user_profile
            - top_5_occupations
            - skill_gap_analysis (for top occupation)
    """

    # ── Step 1: Map user skills to ESCO ───────────────────
    mapped_skills = map_user_skills_to_esco(
        user_skills,
        esco_skill_labels,
        skill_embeddings,
        model,
        fallback_skill_map
    )

    unique_mapped_skills = collect_unique_mapped_skills(
        mapped_skills,
        user_skills_fallback=user_skills
    )

    # ── Step 2: Build weighted profile embedding ──────────
    profile_embedding = build_user_profile_embedding(
        unique_mapped_skills,
        user_experience,
        user_interests,
        model
    )

    # ── Step 3: Rank occupations ──────────────────────────
    top_occupations = rank_occupations(
        profile_embedding,
        occupation_embeddings,
        occupation_labels,
        occupation_uris
    )

    # ── Step 4: Skill gap for top occupation ──────────────
    gap_analysis = skill_gap_analysis(
        top_occupations[0],
        essential_skills_map,
        unique_mapped_skills,
        model
    )

    # ── Step 5: Build mapped skills summary ───────────────
    mapped_skills_output = {}
    for user_skill, matches in mapped_skills.items():
        mapped_skills_output[user_skill] = [
            {
                "esco_skill": esco_skill,
                "similarity_score": score,
                "source": "fallback" if score == 0.0 else "semantic"
            }
            for esco_skill, score in matches
        ]

    # ── Step 6: Assemble final response ───────────────────
    return {
        "user_profile": {
            "input_skills":       user_skills,
            "experience":         user_experience,
            "interests":          user_interests,
            "mapped_esco_skills": mapped_skills_output,
            "unique_esco_skills": unique_mapped_skills
        },
        "top_5_occupations": top_occupations,
        "skill_gap_analysis": gap_analysis
    }
