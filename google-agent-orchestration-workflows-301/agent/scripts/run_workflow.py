from google import genai
from pathlib import Path
import json
import os


def main():
    plan = json.loads(
        Path("agent/data/workflow-plan.json").read_text(encoding="utf-8")
    )

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "demo-key"))

    steps_report = []
    for step in plan.get("steps", []):
        prompt = (
            "You are executing a step in an agent workflow.\n"
            f"Étape: {json.dumps(step, ensure_ascii=False)}\n"
            f"Objectif: {plan.get('goal')}\n"
            "Produce a concise output."
        )
        response = client.models.generate_content(
            model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
            contents=prompt,
        )
        steps_report.append(
            {
                "id": step.get("id"),
                "status": "ok",
                "output": getattr(response, "text", ""),
            }
        )

    report = {
        "lab": "google-agent-orchestration-workflows-301",
        "workflowId": plan.get("workflowId"),
        "steps": steps_report,
        "nextAction": steps_report[-1]["output"] if steps_report else "",
    }

    Path("agent/workflow-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ok")


if __name__ == "__main__":
    main()
