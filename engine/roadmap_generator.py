import os
import json
import requests

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"


def generate_roadmap(
    target_occupation: str,
    weak_skills: list,
    missing_skills: list,
    strong_skills: list = []
) -> dict:

    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY environment variable not set")

    weak_str = "\n".join([
        f"  - {s['skill']} (score: {s['score']:.2f}/1.0)"
        for s in weak_skills
    ]) or "  None"

    missing_str = "\n".join([
        f"  - {s['skill']}"
        for s in missing_skills
    ]) or "  None"

    strong_str = ", ".join(strong_skills) if strong_skills else "Not specified"

    prompt = f"""You are a career development expert. Create a learning roadmap for someone targeting "{target_occupation}".

Strong skills: {strong_str}
Weak skills (need improvement):
{weak_str}
Missing skills (not learned yet):
{missing_str}

Rules:
1. Prioritize missing skills first, then weak skills
2. Max 2 skills per week
3. Provide 2 free learning resources per week
4. Total: 4-8 weeks

Respond ONLY with valid JSON, no markdown, no extra text:
{{
  "target_occupation": "{target_occupation}",
  "total_weeks": 6,
  "summary": "brief summary here",
  "roadmap": [
    {{
      "week": 1,
      "focus_skills": ["skill1"],
      "type": "missing",
      "priority": "high",
      "goal": "measurable goal",
      "resources": [
        {{
          "title": "resource title",
          "type": "course",
          "platform": "platform name",
          "url": null,
          "free": true
        }}
      ]
    }}
  ]
}}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/Llama-3.1-8B-Instruct:cerebras",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.3
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=body, timeout=60)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:300]}")
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"].strip()

        # Extract JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON found in response")

        return json.loads(content[start:end])

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"HuggingFace API request failed: {e}")
    except (json.JSONDecodeError, ValueError) as e:
        raise RuntimeError(f"Failed to parse response as JSON: {e}")