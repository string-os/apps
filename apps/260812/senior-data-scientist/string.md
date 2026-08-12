---
title: Senior Data Scientist
name: senior-data-scientist
namespace: stringhub
type: app
version: 0.1.0
description: World-class data science skill for statistical modeling, experimentation, causal inference, and advanced analytics. Expertise in Python (NumPy, Pandas, Scikit-learn), R, SQL, statistical methods, A/B testing, time series, and business intelligence. Includes experiment design, feature engineering, model evaluation, and stakeholder communication. Use when designing experiments, building predictive models, performing causal analysis, or driving data-driven decisions.
tags: [data-science, ml, experimentation, modeling]
---

# Senior Data Scientist

Data-science helpers. Each action runs a bundled Python tool over an input path and
writes results to an output path — call the action instead of writing the code yourself.
The three actions produce *different* artifacts from the same `--input`: an **experiment
design** (A/B / causal setup), an **engineered-features** dataset, or a **model-evaluation
report**. Pick by which deliverable you need.

**Shared interface (identical fields on all three):**
- `--input <path>` (String field `input`, required) — source dataset/results.
- `--output <path>` (String field `output`, required) — where the result is written.
- `[--config <path>]` — pass via the `config_flag` field as the **full flag string**
  `--config <path>` (NOT just the path); leave empty to skip.
- `[--verbose]` — pass via the `verbose_flag` field as the literal `--verbose`; leave empty to skip.

## Actions
- **`/act.experiment_designer`** `--input <path>` `--output <path>` `[config_flag="--config <path>"]`
  `[verbose_flag="--verbose"]` — design an experiment (A/B test / causal setup), write to output.
- **`/act.feature_engineering_pipeline`** `--input <path>` `--output <path>` `[config_flag="--config <path>"]`
  `[verbose_flag="--verbose"]` — run feature engineering over the input dataset, write engineered features.
- **`/act.model_evaluation_suite`** `--input <path>` `--output <path>` `[config_flag="--config <path>"]`
  `[verbose_flag="--verbose"]` — evaluate model results, write the evaluation report.

Deep-reference docs are bundled under `references/` (advanced statistical methods,
experiment-design frameworks, feature-engineering patterns) — the flags above are complete,
so you shouldn't need them.

```act.experiment_designer
CLI ./scripts/_argshim.sh ./scripts/experiment_designer.py --input "{input}" --output "{output}" "{config_flag}" "{verbose_flag}"
  input: string (required) "Input path"
  output: string (required) "Output path"
  config_flag: string (optional) "Pass as: --config <path> (leave empty to skip)" = ""
  verbose_flag: string (optional) "Pass --verbose to enable verbose output (leave empty to skip)" = ""
```

```act.feature_engineering_pipeline
CLI ./scripts/_argshim.sh ./scripts/feature_engineering_pipeline.py --input "{input}" --output "{output}" "{config_flag}" "{verbose_flag}"
  input: string (required) "Input path"
  output: string (required) "Output path"
  config_flag: string (optional) "Pass as: --config <path> (leave empty to skip)" = ""
  verbose_flag: string (optional) "Pass --verbose to enable verbose output (leave empty to skip)" = ""
```

```act.model_evaluation_suite
CLI ./scripts/_argshim.sh ./scripts/model_evaluation_suite.py --input "{input}" --output "{output}" "{config_flag}" "{verbose_flag}"
  input: string (required) "Input path"
  output: string (required) "Output path"
  config_flag: string (optional) "Pass as: --config <path> (leave empty to skip)" = ""
  verbose_flag: string (optional) "Pass --verbose to enable verbose output (leave empty to skip)" = ""
```
