"""Builds a grounded response with Vertex AI and Gemini."""
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
    selected_docs = [
        {"id": "doc-1", "title": "Grounding policy"},
        {"id": "doc-2", "title": "Latency budget"},
    ]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "You only answer using information from the context.\n"
            f"Contexte: {json.dumps(selected_docs)}\n"
            "Question: How to connect grounding and latency budget?"
        ),
    )
    Path("rag/selected-docs.json").write_text(
        json.dumps(selected_docs, indent=2),
        encoding="utf-8",
    )
    Path("rag/grounded-answer.json").write_text(
        json.dumps(
            {
                "answer": getattr(response, "text", ""),
                "sourceIds": [doc["id"] for doc in selected_docs],
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
