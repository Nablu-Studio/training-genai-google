from google import genai
from pathlib import Path
import json
import os
from datetime import datetime, timezone


def parse_iso(value: str):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main():
    policy = json.loads(
        Path("rag/config/ingestion-policy.json").read_text(encoding="utf-8")
    )
    catalog = json.loads(
        Path("rag/data/source-catalog.json").read_text(encoding="utf-8")
    )

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "demo-key"))

    now = datetime.now(timezone.utc)
    max_age = policy.get("maxAgeHours", 24)
    statuses = []
    for source in catalog.get("sources", []):
        updated = parse_iso(source.get("updatedAt", now.isoformat()))
        age_hours = (now - updated).total_seconds() / 3600
        statuses.append(
            {
                "id": source.get("id"),
                "source": source.get("source"),
                "ageHours": round(age_hours, 2),
                "stale": age_hours > max_age,
            }
        )

    prompt = (
        "Tu es un assistant d’exploitation RAG.\n"
        f"Politique: {json.dumps(policy, ensure_ascii=False)}\n"
        f"Statuts: {json.dumps(statuses, ensure_ascii=False)}\n"
        "Propose une action de synchronisation prioritaire."
    )

    response = client.models.generate_content(
        model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )

    report = {
        "lab": "google-rag-ingestion-and-freshness-301",
        "policy": policy,
        "sources": statuses,
        "recommendedAction": getattr(response, "text", ""),
    }

    Path("rag/freshness-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ok")


if __name__ == "__main__":
    main()
