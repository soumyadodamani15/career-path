---
title: Career Path
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Career Recommendation Engine

Semantic career recommendation and skill gap analysis using the ESCO dataset.

## API Endpoints

### POST `/api/v1/betaRecommendation`
Returns top 5 career recommendations and skill gap analysis.

**Request:**
```json
{
  "skills": ["Python", "data analysis", "machine learning"],
  "experience": "3 years working as a data analyst in finance",
  "interests": ["artificial intelligence", "automation", "statistics"]
}
```

### GET `/api/v1/health`
Health check endpoint.