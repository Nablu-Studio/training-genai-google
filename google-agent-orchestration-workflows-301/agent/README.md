# Workspace - Orchestration d’agent et workflow (Google)

## Objectif

Ce workspace vous fait pratiquer une orchestration simple :

- un plan de workflow versionnable (`agent/data/workflow-plan.json`),
- un exécuteur minimal (`agent/scripts/run_workflow.py`),
- une preuve d’exécution (`agent/workflow-report.json`).

## Exécution

```bash
cd training/google/examples/google-agent-orchestration-workflows-301
python3 agent/scripts/run_workflow.py
```

## Validation

Ouvrez `agent/workflow-report.json` et vérifiez :

- une entrée `steps` avec une trace par étape,
- un statut par étape,
- une sortie de synthèse (prochaine action).
