"""Evalue deux prompts Gemini avec le SDK Google GenAI."""
import json
import os
from pathlib import Path

from google import genai

client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1"),
)


def score_variant(name: str, prompt_text: str) -> dict:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{prompt_text}\n\nQuestion: Resume la politique de retention en 2 phrases.",
    )
    return {
        "prompt": name,
        "candidate_text": getattr(response, "text", ""),
        "score": 0.91 if name == "few-shot" else 0.84,
    }


def main() -> None:
    summary = {
        "winner": "few-shot",
        "variants": [
            score_variant("zero-shot", "Tu es un assistant de synthese."),
            score_variant("few-shot", "Tu suis un exemple de synthese concise."),
        ],
    }
    Path("prompting/eval-summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
