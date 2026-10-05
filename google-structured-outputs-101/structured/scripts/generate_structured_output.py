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
    contents="Prépare un artefact pour Structured outputs avec Gemini.",
)

Path("structured/response.json").write_text(
    json.dumps({"lab": "google-structured-outputs-101", "script": "generate_structured_output.py", "content": getattr(response, "text", "")}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print("ok")
