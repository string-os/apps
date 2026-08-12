---
title: Senior Data Engineer
name: senior-data-engineer
namespace: stringhub
type: app
version: 0.1.0
description: World-class data engineering skill for building scalable data pipelines, ETL/ELT systems, real-time streaming, and data infrastructure. Expertise in Python, SQL, Spark, Airflow, dbt, Kafka, Flink, Kinesis, and modern data stack. Includes data modeling, pipeline orchestration, data quality, streaming quality monitoring, and DataOps. Use when designing data architectures, building batch or streaming data pipelines, optimizing data workflows, or implementing data governance.
tags: [data-engineering, etl, streaming, kafka, flink, data-quality]
---

# Senior Data Engineer

Data-engineering helpers for batch + streaming pipelines. Each action runs a bundled
Python generator/validator — call the action instead of writing the code yourself.
The fixed String field of each action holds its required arg; **all other flags go in
`extra_args` as ONE space-separated string** (e.g. `--config pipeline.yaml --output json`).
**Passthrough gotcha:** an `extra_args` value cannot begin with `--` — every flag below takes a
normal value, so this only bites if you invent one.

## Batch pipelines (these three share one interface)
Each takes `--input <path>` (the String field) and analyzes/generates from it. extra_args
flags (identical for all three): `[--output text|json|csv]` (default `text` — this is the
output *format*, not a path) `[--config <file> | -c <file>]` `[--file <path> | -f <path>]`
(write output to a file) `[--verbose | -v]`. There is no `--validate`/`--template`/`--rules`/
`--threshold` flag on these — drive them by `--input` + `--output` + `--config`.
- **`/act.pipeline_orchestrator`** `--input <path>` `[--output text|json|csv]` `[--config <file>]`
  `[--file <path>]` `[--verbose]` — orchestrate / inspect an Airflow-style pipeline from the input.
- **`/act.data_quality_validator`** `--input <csv/table>` `[--output text|json|csv]` `[--config <file>]`
  `[--file <path>]` `[--verbose]` — multi-dimensional quality checks (completeness, accuracy,
  consistency, timeliness, validity).
- **`/act.etl_performance_optimizer`** `--input <path>` `[--output text|json|csv]` `[--config <file>]`
  `[--file <path>]` `[--verbose]` — profile executions, find bottlenecks, emit recommendations.

## Streaming pipelines
- **`/act.stream_processor`** — validate a streaming YAML and/or generate job artifacts. All flags
  via extra_args: `[--config <yaml/json> | -c]` `[--validate]` (validate only) `[--generate]` (emit
  artifacts) `[--mode kafka|flink|kinesis|docker]` `[--output-dir <dir> | -o]` (default
  `./streaming-output`) `[--output text|json]` (default `text`) `[--topics <csv>]` `[--partitions <n>]`
  (default 12) `[--replication-factor <n>]` (default 3) `[--retention-days <n>]` (default 7)
  `[--job-name <name>]` `[--parallelism <n>]` (default 4) `[--input kafka|kinesis|file]` `[--stream <name>]`
  `[--shards <n>]` `[--verbose]`.
- **`/act.kafka_config_generator`** `--mode topic|producer|consumer|streams|connect|security|cluster`
  (String field, required) — extra_args: `[--bootstrap-servers <s> | -b]` `[--output json|yaml|properties]`
  (default `json`, this is the *format*) `[--output-dir <dir>]` (write files) `[--name <topic> | -n]`
  `[--partitions <n> | -p]` (default 12) `[--replication-factor <n> | -r]` (default 3) `[--retention-days <n>]`
  (default 7) `[--cleanup-policy delete|compact|delete,compact]` `[--compression none|gzip|snappy|lz4|zstd]`
  (default `lz4`) `[--profile <default|high-throughput|exactly-once|low-latency|ordered>]`
  `[--transactional-id <id>]` `[--group <id> | -g]` `[--app-id <id>]` `[--state-dir <dir>]`
  `[--processing-guarantee at_least_once|exactly_once|exactly_once_v2]` (default `exactly_once_v2`)
  `[--connector-type source|sink]` `[--connector-class <c>]` `[--tasks-max <n>]`
  `[--auth none|sasl-plain|sasl-scram|sasl-oauthbearer|mtls]` `[--ssl]` `[--principal <p>]`
  `[--brokers <n>]` `[--zookeepers <n>]` `[--environment development|staging|production]` `[--verbose]`.
- **`/act.streaming_quality_validator`** `--topic <name>` (String field, required) — extra_args:
  `[--kafka <servers> | -k]` `[--schema-registry <url>]` `[--group <id> | -g]` and check toggles
  `[--lag] [--freshness] [--throughput] [--drift] [--late-data] [--dlq] [--all]`; thresholds
  `[--max-delay <s>]` `[--lag-warning <n>]` (default 10000) `[--lag-critical <n>]` (default 100000)
  `[--window <s>]` (default 60); `[--rules <file> | -r]` `[--output text|json]` (default `text`)
  `[--file <path> | -f]` (write to file) `[--verbose]`. (No `--threshold`; use the specific
  `--lag-warning`/`--lag-critical`/`--max-delay`.)

Deep-reference docs are bundled under `references/` (frameworks: Lambda/Kappa/Medallion, modeling,
exactly-once, windowing; templates: Airflow/Spark/dbt/Flink/Kafka; tool docs) — the flags above
are complete, so you shouldn't need them.

```act.pipeline_orchestrator
CLI ./scripts/_argshim.sh ./scripts/pipeline_orchestrator.py --input "{input}" "{extra_args}"
  input: string (required) "Input file or target path to process (--input)"
  extra_args: string (optional) "Additional flags passed raw (e.g. --config pipeline_config.yaml --output dags/)" = ""
```

```act.data_quality_validator
CLI ./scripts/_argshim.sh ./scripts/data_quality_validator.py --input "{input}" "{extra_args}"
  input: string (required) "Input file or target path to validate (--input)"
  extra_args: string (optional) "Additional flags passed raw (e.g. --output report.html --rules rules.yaml)" = ""
```

```act.etl_performance_optimizer
CLI ./scripts/_argshim.sh ./scripts/etl_performance_optimizer.py --input "{input}" "{extra_args}"
  input: string (required) "Input file or target path to analyze (--input)"
  extra_args: string (optional) "Additional flags passed raw (e.g. --output json)" = ""
```

```act.kafka_config_generator
CLI ./scripts/_argshim.sh ./scripts/kafka_config_generator.py --mode "{mode}" "{extra_args}"
  mode: string (required) "Generation mode (--mode), e.g. topic, producer, consumer, streams, connect, cluster, security"
  extra_args: string (optional) "Additional flags passed raw (e.g. --topic events --partitions 12)" = ""
```

```act.stream_processor
CLI ./scripts/_argshim.sh ./scripts/stream_processor.py "{extra_args}"
  extra_args: string (optional) "Flags passed raw (e.g. --config streaming_config.yaml --mode flink --generate)" = ""
```

```act.streaming_quality_validator
CLI ./scripts/_argshim.sh ./scripts/streaming_quality_validator.py --topic "{topic}" "{extra_args}"
  topic: string (required) "Topic name to validate (--topic)"
  extra_args: string (optional) "Additional flags passed raw (e.g. --kafka localhost:9092 --lag --freshness)" = ""
```
