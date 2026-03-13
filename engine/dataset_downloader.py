import os
import requests
from engine.config import DATASET_DIR

ESCO_RELATIONS_URL = (
    "https://esco.ec.europa.eu/sites/default/files/Releases/"
    "ESCO%20dataset%20-%20v1.2.0%20-%20classification%20-%20en%20-%20CSV.zip"
)

RELATIONS_FILE = "occupationSkillRelations_en.csv"


def download_relations_if_missing():
    """Download only the large relations CSV if not present."""
    target_path = os.path.join(DATASET_DIR, RELATIONS_FILE)

    if os.path.exists(target_path):
        print("✅ Relations CSV already present — skipping download")
        return

    import zipfile
    import io

    os.makedirs(DATASET_DIR, exist_ok=True)
    print("📥 Downloading ESCO relations dataset (~28MB)...")
    print("   This takes ~1-2 minutes on first run...")

    try:
        response = requests.get(ESCO_RELATIONS_URL, stream=True, timeout=300)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        chunks = []

        for chunk in response.iter_content(chunk_size=8192):
            chunks.append(chunk)
            downloaded += len(chunk)
            if total_size:
                percent = int((downloaded / total_size) * 100)
                print(f"\r   Downloading: {percent}%", end="", flush=True)

        print("\n✅ Download complete — extracting...")

        zip_data = b"".join(chunks)
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
            for file in zip_ref.namelist():
                if os.path.basename(file) == RELATIONS_FILE:
                    source = zip_ref.open(file)
                    with open(target_path, "wb") as target:
                        target.write(source.read())
                    print(f"✅ Extracted: {RELATIONS_FILE}")
                    return

        raise FileNotFoundError(f"❌ {RELATIONS_FILE} not found in zip!")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"❌ Failed to download: {e}")