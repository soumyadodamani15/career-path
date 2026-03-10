# Career Recommendation Engine

Semantic career recommendation and skill gap analysis using the ESCO dataset.

## Project Structure

```
career_engine/
├── dataset/                        # ESCO CSV files + fallback map
│   ├── occupations_en.csv
│   ├── skills_en.csv
│   ├── occupationSkillRelations_en.csv
│   └── fallback_skill_map.csv
├── cache/                          # Auto-generated embedding cache
├── engine/
│   ├── config.py                   # All configuration constants
│   ├── data_loader.py              # Dataset loading and processing
│   ├── embeddings.py               # Model loading and embedding generation
│   ├── skill_mapper.py             # User skill → ESCO skill mapping
│   ├── recommender.py              # Occupation ranking and skill gap analysis
│   └── pipeline.py                 # End-to-end orchestration
├── api/
│   ├── routes.py                   # FastAPI endpoints
│   └── state.py                    # Shared app state
├── main.py                         # FastAPI app entry point
├── requirements.txt
└── README.md
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add datasets
Place these files in the `dataset/` folder:
- `occupations_en.csv`
- `skills_en.csv`
- `occupationSkillRelations_en.csv`
- `fallback_skill_map.csv`

### 3. Run locally
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. API Docs
Visit: `http://localhost:8000/docs`

---

## API Endpoints

### POST `/api/v1/recommend`
Returns top 5 career recommendations and skill gap analysis.

**Request:**
```json
{
  "skills": ["Python", "data analysis", "machine learning"],
  "experience": "3 years working as a data analyst in the finance industry",
  "interests": ["artificial intelligence", "automation", "statistics"]
}
```

**Response:**
```json
{
  "user_profile": {
    "input_skills": ["Python", "data analysis", "machine learning"],
    "experience": "3 years working as a data analyst in the finance industry",
    "interests": ["artificial intelligence", "automation", "statistics"],
    "mapped_esco_skills": { ... },
    "unique_esco_skills": [ ... ]
  },
  "top_5_occupations": [
    {
      "rank": 1,
      "occupation": "data analyst",
      "uri": "http://data.europa.eu/esco/occupation/...",
      "similarity_score": 0.6116
    }
  ],
  "skill_gap_analysis": {
    "occupation": "data analyst",
    "uri": "http://...",
    "total_essential": 12,
    "matched_skills": [ ... ],
    "missing_skills": [ ... ]
  }
}
```

### GET `/api/v1/health`
Health check endpoint.

### POST `/api/v1/admin/reload-fallback`
Reloads `fallback_skill_map.csv` without restarting the server.

---

## Configuration

All settings are in `engine/config.py`:

| Setting | Default | Description |
|---|---|---|
| `SIMILARITY_THRESHOLD` | 0.5 | Min score for semantic skill match |
| `TOP_K_SKILL_MATCHES` | 3 | Top K ESCO skills per user skill |
| `FALLBACK_THRESHOLD` | 0.80 | Override semantic match if score below this |
| `TOP_N_OCCUPATIONS` | 5 | Number of occupations to return |
| `SKILL_WEIGHT` | 0.5 | Weight for skills in profile embedding |
| `EXPERIENCE_WEIGHT` | 0.3 | Weight for experience in profile embedding |
| `INTEREST_WEIGHT` | 0.2 | Weight for interests in profile embedding |

---

## Adding New Skills to Fallback Map

Add a row to `dataset/fallback_skill_map.csv`:
```
user_skill,esco_skill,domain
"new tool","esco equivalent skill","Domain Name"
```

Then call the reload endpoint (no restart needed):
```bash
curl -X POST http://localhost:8000/api/v1/admin/reload-fallback
```

---

## Deployment (Railway — Free Tier)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. New Project → Deploy from GitHub
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `PORT=8000`
