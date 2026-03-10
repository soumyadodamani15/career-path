import pandas as pd
from engine.config import (
    OCCUPATIONS_PATH, SKILLS_PATH, RELATIONS_PATH, FALLBACK_PATH
)


def load_datasets():
    """Load all 3 ESCO datasets."""
    occupations_df = pd.read_csv(OCCUPATIONS_PATH)
    skills_df      = pd.read_csv(SKILLS_PATH)
    relations_df   = pd.read_csv(RELATIONS_PATH)
    return occupations_df, skills_df, relations_df


def build_skill_maps(relations_df):
    """
    Build occupation → essential skills and occupation → all skills maps.
    Returns:
        essential_skills_map : dict {occupationUri: [skillLabel, ...]}
        all_skills_map       : dict {occupationUri: [skillLabel, ...]}
    """
    essential_skills_map = (
        relations_df[relations_df["relationType"] == "essential"]
        .groupby("occupationUri")["skillLabel"]
        .apply(list)
        .to_dict()
    )
    all_skills_map = (
        relations_df
        .groupby("occupationUri")["skillLabel"]
        .apply(list)
        .to_dict()
    )
    return essential_skills_map, all_skills_map


def build_occupation_corpus(occupations_df, all_skills_map):
    """
    Build occupation text corpus by combining:
    label + definition + description + all skills.
    Returns:
        occupation_corpus : list of strings
        occupation_uris   : list of URIs
        occupation_labels : list of labels
    """
    occupation_corpus = []
    occupation_uris   = []
    occupation_labels = []

    for _, row in occupations_df.iterrows():
        uri         = row["conceptUri"]
        label       = str(row["preferredLabel"]) if pd.notna(row["preferredLabel"]) else ""
        definition  = str(row["definition"])     if pd.notna(row["definition"])     else ""
        description = str(row["description"])    if pd.notna(row["description"])    else ""
        skills      = all_skills_map.get(uri, [])
        skills_text = ", ".join(skills)

        corpus_text = f"{label}. {definition}. {description}. Skills: {skills_text}"

        occupation_corpus.append(corpus_text)
        occupation_uris.append(uri)
        occupation_labels.append(label)

    return occupation_corpus, occupation_uris, occupation_labels


def load_fallback_skill_map(csv_path=FALLBACK_PATH):
    """
    Load fallback skill map from CSV.
    Returns dict: {user_skill_lowercase: esco_skill}
    """
    df = pd.read_csv(csv_path)
    fallback_map = dict(zip(
        df["user_skill"].str.lower().str.strip(),
        df["esco_skill"]
    ))
    return fallback_map
