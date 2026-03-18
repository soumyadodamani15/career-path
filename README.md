---
title: Career Path
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🚀 Career Path — Semantic Career Recommendation Engine

> An AI-powered career recommendation and learning roadmap engine built on the ESCO dataset, deployed as a live REST API.

[![Live API](https://img.shields.io/badge/API-Live%20on%20HuggingFace-blue)](https://dodamanisoumya-career-path.hf.space)
[![Docs](https://img.shields.io/badge/Docs-Swagger%20UI-green)](https://dodamanisoumya-career-path.hf.space/docs)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)](https://fastapi.tiangolo.com/)

---

## 📌 Overview

Career Path is a semantic career recommendation engine that matches users to relevant ESCO occupations based on their skills, experience, and interests. It also generates personalized week-by-week learning roadmaps for identified skill gaps using an AI language model.

Built as part of the **FutureYou project** at **TechLabs Berlin (WS 2025)**.

---

## ✨ Features

- **Semantic Skill Mapping** — Maps user skills to ESCO taxonomy using cosine similarity with `all-MiniLM-L6-v2`
- **Fallback Dictionary** — 276 hand-curated entries across 8 domains for modern skills not well represented in ESCO
- **Weighted Profile Embedding** — Combines skills (50%), experience (30%), and interests (20%) into a single profile vector
- **Occupation Ranking** — Ranks 3,043 ESCO occupations by semantic similarity to the user profile
- **Skill Gap Analysis** — Identifies missing essential skills for the top recommended occupation
- **AI Career Roadmap** — Generates a personalized week-by-week learning plan using an LLM
- **Embedding Cache** — Caches embeddings to disk for fast subsequent startups

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| **API Framework** | FastAPI |
| **ML Model** | SentenceTransformers (all-MiniLM-L6-v2) |
| **Dataset** | ESCO v1.2.0 (3,043 occupations, 13,960 skills) |
| **Roadmap LLM** | Llama 3.1 8B via HuggingFace Inference API |
| **Deployment** | HuggingFace Spaces (Docker) |
| **Language** | Python 3.11 |

---

## 🌐 Live API

**Base URL:** `https://dodamanisoumya-career-path.hf.space`

**Interactive Docs:** `https://dodamanisoumya-career-path.hf.space/docs`

> ⚠️ First request after inactivity may take 3-5 minutes (cold start — embeddings regenerating). Subsequent requests are fast (~1-2 seconds).

---

## 📡 API Endpoints

### `POST /api/v1/betaRecommendation`
Returns top 5 career recommendations and skill gap analysis.

**Request:**
```json
{
  "skills": ["Python", "data analysis", "machine learning"],
  "experience": "3 years working as a data analyst in finance",
  "interests": ["artificial intelligence", "automation", "statistics"]
}
```

**Response:**
```json
{
  "top_5_occupations": [
    { "rank": 1, "occupation": "data analyst", "similarity_score": 0.82 },
    { "rank": 2, "occupation": "business analyst", "similarity_score": 0.79 }
  ],
  "skill_gap_analysis": {
    "occupation": "data analyst",
    "total_essential": 12,
    "matched_skills": [...],
    "missing_skills": [...]
  }
}
```

---

### `POST /api/v1/careerRoadmap`
Generates a personalized week-by-week learning roadmap using an AI language model.

**Request:**
```json
{
  "target_occupation": "data analyst",
  "weak_skills": [
    { "skill": "Python", "score": 0.3 },
    { "skill": "SQL", "score": 0.5 }
  ],
  "missing_skills": [
    { "skill": "statistics" },
    { "skill": "data visualization" }
  ],
  "strong_skills": ["Excel", "data cleaning"]
}
```

**Response:**
```json
{
  "target_occupation": "data analyst",
  "total_weeks": 6,
  "summary": "Develop a strong foundation in data analysis...",
  "roadmap": [
    {
      "week": 1,
      "focus_skills": ["statistics"],
      "type": "missing",
      "priority": "high",
      "goal": "Understand basic statistical concepts",
      "resources": [
        {
          "title": "Statistics 101 by Khan Academy",
          "type": "course",
          "platform": "Khan Academy",
          "url": "https://www.khanacademy.org/math/statistics-probability",
          "free": true
        }
      ]
    }
  ]
}
```

---

### `GET /api/v1/health`
Health check endpoint. Returns API status.

---

## 🏗 Project Structure

```
career-path/
├── api/
│   ├── routes.py          # FastAPI endpoints
│   └── state.py           # Shared app state
├── engine/
│   ├── config.py          # Configuration and file paths
│   ├── data_loader.py     # ESCO dataset loading and processing
│   ├── embeddings.py      # Model loading and embedding generation
│   ├── skill_mapper.py    # User skill → ESCO skill mapping
│   ├── recommender.py     # Occupation ranking and skill gap analysis
│   ├── pipeline.py        # End-to-end orchestration
│   ├── roadmap_generator.py # AI-powered learning roadmap generation
│   └── dataset_downloader.py # Auto-download large dataset files
├── Dataset/
│   ├── occupations_en.csv
│   ├── skills_en.csv
│   └── fallback_skill_map.csv  # 276 curated skill mappings
├── main.py                # FastAPI app entry point
├── Dockerfile             # Docker configuration for HuggingFace Spaces
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

```
User Input (skills, experience, interests)
        ↓
Skill Mapping — semantic cosine similarity against 13,960 ESCO skills
        ↓
Fallback Dictionary — fixes low-quality or missing mappings
        ↓
Weighted Profile Embedding — 50% skills + 30% experience + 20% interests
        ↓
Occupation Ranking — cosine similarity against 3,043 ESCO occupations
        ↓
Top 5 Recommendations + Skill Gap Analysis
        ↓
AI Roadmap Generation — personalized week-by-week learning plan
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- ESCO dataset files (see below)

### 1. Clone the repo
```bash
git clone https://github.com/soumyadodamani15/career-path.git
cd career-path
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add dataset files
Place these files in the `Dataset/` folder:
- `occupations_en.csv`
- `skills_en.csv`
- `occupationSkillRelations_en.csv` ← auto-downloaded on startup

Download from: [ESCO Download Page](https://esco.ec.europa.eu/en/use-esco/download) (Version 1.2.0, CSV, English)

### 4. Set environment variables
Create a `.env` file:
```
HUGGINGFACE_API_KEY=your_hf_token_here
```

### 5. Run the server
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open API docs
```
http://localhost:8000/docs
```

> First run generates embeddings (~2 minutes). Subsequent runs load from cache (~30 seconds).

---

## 📊 Performance

Tested across 5 domains with the following results:

| Domain | Top Match | Similarity Score |
|---|---|---|
| Creative Arts | graphic designer | 0.73 ✅ |
| Finance | asset manager | 0.72 ✅ |
| Healthcare | doctors' surgery assistant | 0.68 ✅ |
| Education | e-learning developer | 0.67 ✅ |
| Software / Tech | database developer | 0.65 ✅ |

---

## 🔮 Roadmap

- [ ] React demo frontend for standalone demo
- [ ] Auto fallback improvement pipeline using Claude API
- [ ] Integration with DL track skill scoring model
- [ ] Skill proficiency scoring from user assessment

---

## 👤 Author

**Soumya Dodamani**
Data Science Track — FutureYou Project
TechLabs Berlin, Winter Semester 2025

[![GitHub](https://img.shields.io/badge/GitHub-soumyadodamani15-black)](https://github.com/soumyadodamani15)

---

## 📄 License

This project is licensed under the MIT License.
