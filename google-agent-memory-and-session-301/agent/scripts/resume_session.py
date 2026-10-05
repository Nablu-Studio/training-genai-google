from google import genai
from pathlib import Path
import json
import os


def main():
    state = json.loads(
        Path("agent/data/session-state.json").read_text(encoding="utf-8")
    )

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "demo-key"))

    prompt = (
        "Tu es un agent. Reprends la session et propose une prochaine action.\n"
        f"Etat de session: {json.dumps(state, ensure_ascii=False)}\n"
        "Réponds en JSON avec les clés: resumedGoal, resumedDecision, nextAction, rationale."
    )

    response = client.models.generate_content(
        model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )

    report = {
        "lab": "google-agent-memory-and-session-301",
        "resumedGoal": state.get("goal"),
        "resumedDecision": state.get("lastDecision"),
        "nextAction": getattr(response, "text", ""),
        "rationale": "Synthèse produite à partir de l’état et d’une réponse Gemini.",
    }

    Path("agent/session-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ok")


if __name__ == "__main__":
    main()
