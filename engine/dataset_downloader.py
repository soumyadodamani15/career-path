import os
import requests
from engine.config import DATASET_DIR

ESCO_RELATIONS_URL = (
    "https://huggingface.co/datasets/dodamanisoumya/esco-relations/resolve/main/"
    "occupationSkillRelations_en.csv"
)

RELATIONS_FILE = "occupationSkillRelations_en.csv"


def download_relations_if_missing():
    target_path = os.path.join(DATASET_DIR, RELATIONS_FILE)

    if os.path.exists(target_path):
        print("✅ Relations CSV already present — skipping download")
        return

    os.makedirs(DATASET_DIR, exist_ok=True)
    print("📥 Downloading relations dataset from HuggingFace (~28MB)...")

    try:
        response = requests.get(ESCO_RELATIONS_URL, stream=True, timeout=300)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(target_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = int((downloaded / total_size) * 100)
                    print(f"\r   Downloading: {percent}%", end="", flush=True)

        print("\n✅ Relations dataset ready!")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"❌ Failed to download: {e}")