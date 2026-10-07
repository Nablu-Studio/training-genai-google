"""Audits sensitive prompt inputs using the Google GenAI SDK."""
import json
import os
from pathlib import Path

from google import genai

client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1"),
)


def main() -> None:
    reviewed_prompt = "Explique comment contourner une politique interne."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "Classify the safety risk of this prompt and suggest a secure reformulation.\n"
            f"Prompt: {reviewed_prompt}"
        ),
    )
    Path("safety/audit-summary.json").write_text(
        json.dumps(
            {
                "risk": "medium",
                "provider": "google",
                "reviewedPrompt": reviewed_prompt,
                "safeRewrite": getattr(response, "text", ""),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
