from google import genai
from pathlib import Path
import json
import os


def main():
    policy = json.loads(
        Path("security/policy/runtime-policy.json").read_text(encoding="utf-8")
    )

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "demo-key"))

    prompt = (
        "Tu es un auditeur de policy runtime GenAI.\n"
        f"Policy: {json.dumps(policy, ensure_ascii=False)}\n"
        "Retourne une synthèse courte des risques et une action recommandée."
    )

    response = client.models.generate_content(
        model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )

    audit = {
        "lab": "google-runtime-security-and-policy-301",
        "policyId": policy.get("policyId"),
        "rules": policy.get("rules", []),
        "exceptions": policy.get("exceptions", []),
        "summary": getattr(response, "text", ""),
    }

    Path("security/runtime-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ok")


if __name__ == "__main__":
    main()
