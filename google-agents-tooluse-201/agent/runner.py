"""Execute un agent Gemini outille et ecrit une trace JSON."""
import json
import os
from pathlib import Path

from google import genai

from tools.weather_tool import get_weather

client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1"),
)


def main() -> None:
    weather = get_weather("Paris")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "Tu es un agent outille. Utilise la sortie outil pour repondre au voyageur.\n"
            f"Tool result: {json.dumps(weather)}"
        ),
    )
    Path("agent/run-trace.json").write_text(
        json.dumps(
            {
                "toolResult": weather,
                "finalAnswer": getattr(response, "text", ""),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
