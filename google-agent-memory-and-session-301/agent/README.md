# Workspace - Mémoire d’agent et reprise de session (Google)

## Objectif

Ce workspace vous fait pratiquer une reprise de session minimale :

- un état de session explicite dans `agent/data/session-state.json`,
- une reprise guidée par Gemini via `agent/scripts/resume_session.py`,
- une preuve observable écrite dans `agent/session-report.json`.

## Fichiers

- `agent/data/session-state.json` : état de session de référence (objectif, décisions, contraintes).
- `agent/scripts/resume_session.py` : lit l’état, appelle Gemini, écrit un rapport JSON.

## Exécution

```bash
cd training/google/examples/google-agent-memory-and-session-301
python3 agent/scripts/resume_session.py
```

## Validation attendue

Après exécution, ouvrez `agent/session-report.json` et vérifiez :

- l’objectif repris,
- la décision précédente reprise,
- une prochaine action claire et actionnable.
