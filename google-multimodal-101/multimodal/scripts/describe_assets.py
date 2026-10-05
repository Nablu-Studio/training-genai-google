from google import genai
from pathlib import Path
import json
import os

client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1"),
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Prépare un artefact pour Multimodal avec Gemini.",
)

Path("multimodal/analysis-summary.json").write_text(
    json.dumps({"lab": "google-multimodal-101", "script": "describe_assets.py", "content": getattr(response, "text", "")}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print("ok")
