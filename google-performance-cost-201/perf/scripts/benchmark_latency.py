"""Measures real-world latency of Gemini models (Vertex AI) under a load profile.

Parent lab: google-performance-cost-201.
Entrees : perf/data/load-profile.json (rps, promptTokens)
          perf/data/model-matrix.json (modeles a comparer).
Artefact : perf/latency-report.json (p50/p95, erreurs, throttling, tokens).

Environment variables:
  GOOGLE_CLOUD_PROJECT (obligatoire), GOOGLE_CLOUD_LOCATION (defaut europe-west1)
  BENCH_REQUESTS nombre d'appels par modele (defaut 10)
  BENCH_MODEL    limite le benchmark a un seul modele
"""
import json
import math
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import errors, types

PERF_DIR = Path(__file__).resolve().parents[1]
CHARS_PER_TOKEN = 4  # heuristic approximation to estimate prompt token length


def percentile(values: list[float], pct: float) -> float | None:
    """Nearest-rank percentile: discrete non-interpolated latency measurement."""
    if not values:
        return None
    ordered = sorted(values)
    rank = max(1, math.ceil(pct / 100 * len(ordered)))
    return round(ordered[rank - 1], 1)


def build_prompt(prompt_tokens: int) -> str:
    filler = "Contexte de test pour le benchmark de latence. " * (
        prompt_tokens * CHARS_PER_TOKEN // 48 + 1
    )
    return filler[: prompt_tokens * CHARS_PER_TOKEN] + "\nResume ce contexte en une phrase."


def bench_model(client: genai.Client, model: str, profile: dict, requests: int) -> dict:
    prompt = build_prompt(profile["promptTokens"])
    interval = 1 / profile["rps"]
    latencies, prompt_tokens, completion_tokens = [], [], []
    errors_count = throttled = 0

    for _ in range(requests):
        started = time.perf_counter()
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(max_output_tokens=60),
            )
            latencies.append((time.perf_counter() - started) * 1000)
            usage = response.usage_metadata
            if usage:
                prompt_tokens.append(usage.prompt_token_count or 0)
                completion_tokens.append(usage.candidates_token_count or 0)
        except errors.APIError as exc:
            # HTTP 429 (quota limit) is a capacity signal: track it separately.
            if getattr(exc, "code", None) == 429:
                throttled += 1
            else:
                errors_count += 1
                print(f"[{model}] erreur API : {exc}", file=sys.stderr)
        # Pace requests to adhere to target load RPS.
        time.sleep(max(0.0, interval - (time.perf_counter() - started)))

    def mean(values: list[int]) -> float | None:
        return round(sum(values) / len(values), 1) if values else None

    return {
        "modelId": model,
        "requests": requests,
        "succeeded": len(latencies),
        "errors": errors_count,
        "throttled": throttled,
        "p50Ms": percentile(latencies, 50),
        "p95Ms": percentile(latencies, 95),
        "avgPromptTokens": mean(prompt_tokens),
        "avgCompletionTokens": mean(completion_tokens),
    }


def main() -> None:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        sys.exit("Set GOOGLE_CLOUD_PROJECT (and authenticate via gcloud) before running the benchmark.")

    profile = json.loads((PERF_DIR / "data/load-profile.json").read_text(encoding="utf-8"))
    matrix = json.loads((PERF_DIR / "data/model-matrix.json").read_text(encoding="utf-8"))
    only = os.getenv("BENCH_MODEL")
    requests = int(os.getenv("BENCH_REQUESTS", "10"))

    client = genai.Client(
        vertexai=True,
        project=project,
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1"),
    )
    results = []
    for model, traits in matrix.items():
        if only and model != only:
            continue
        result = bench_model(client, model, profile, requests)
        results.append({**result, "expectedCost": traits["cost"], "expectedLatency": traits["latency"]})

    report = {"loadProfile": profile, "results": results}
    output = PERF_DIR / "latency-report.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
