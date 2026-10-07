from google import genai
from pathlib import Path
import json
import os


def main():
    plan = json.loads(
        Path("rag/config/hybrid-search-plan.json").read_text(encoding="utf-8")
    )
    corpus = json.loads(Path("rag/data/corpus.json").read_text(encoding="utf-8"))

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "demo-key"))

    prompt = (
        "Rerank candidate documents for hybrid search retrieval.\n"
        f"Requête: {plan.get('query')}\n"
        f"Documents: {json.dumps(corpus.get('documents', []), ensure_ascii=False)}\n"
        "Return an ordered list of document IDs from most relevant to least relevant."
    )

    response = client.models.generate_content(
        model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )

    report = {
        "lab": "google-hybrid-search-and-reranking-301",
        "query": plan.get("query"),
        "signals": plan.get("signals"),
        "topK": plan.get("topK"),
        "rerankTopK": plan.get("rerankTopK"),
        "reranked": getattr(response, "text", ""),
    }

    Path("rag/search-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ok")


if __name__ == "__main__":
    main()
