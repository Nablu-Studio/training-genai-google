from google import genai
from pathlib import Path
import json
import os


def main():
    thresholds = json.loads(
        Path("monitoring/config/alert-thresholds.json").read_text(encoding="utf-8")
    )

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "demo-key"))

    prompt = (
        "Tu es un assistant SRE. À partir de seuils, propose un état de santé.\n"
        f"Seuils: {json.dumps(thresholds, ensure_ascii=False)}\n"
        "Retourne une synthèse courte et une action recommandée."
    )

    response = client.models.generate_content(
        model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )

    report = {
        "lab": "google-prod-monitoring-and-alerting-301",
        "thresholds": thresholds,
        "sampleMetrics": {"p95LatencyMs": 1350, "errorRatePct": 0.7, "tokens": 9800},
        "status": "alert",
        "recommendedAction": getattr(response, "text", ""),
    }

    Path("monitoring/health-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ok")


if __name__ == "__main__":
    main()
