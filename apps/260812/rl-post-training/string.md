---
title: Rl Post Training
name: rl-post-training
namespace: stringhub
type: app
version: 0.2.0
description: "Diagnostic guide for RL-based post-training of language models (GRPO, PPO, REINFORCE, DPO). Use proactively when debugging a training pipeline that shows no improvement, loss anomalies, reward stagnation, NaN gradients, or other unexpected behavior during reinforcement learning fine-tuning. Work through all pipeline stages — reward, advantages, log-probs, loss, generation/decoding — before concluding the diagnosis is complete; stopping after one or two fixes is a common failure mode. Covers log-probability math, advantage estimation, numerical stability, reward processing, and generation/decoding pipeline issues."
tags: [rl, debugging, grpo, training]
---

# RL Post-Training

Debug RL post-training pipelines (GRPO / PPO / REINFORCE / DPO) that show no
improvement, loss anomalies, reward stagnation, or NaN gradients. The pipeline is
`prompt → generate → reward → advantages → policy-gradient update`; a bug can live in
any stage. The action below runs the bundled numeric diagnostic so you compare real
values against the invariants instead of writing probe code yourself.

All flags listed inline below. The action prints its diagnostic to stdout; you should not
need `/act.verify_pipeline --help`.

## Diagnose
- **`/act.verify_pipeline`** (no flags) — run the bundled diagnostic; prints log-prob,
  advantage, and decoding values on small fixed inputs. Run it **before declaring a fix
  done** and inspect lines marked `?` (borderline) and `!!` (hard invariant violation).
  Takes no arguments — it exercises the TRL pipeline functions directly with fixed probes.

## How to work through it
Walk **every** stage in order before concluding — stopping after one or two fixes is the
common failure mode. At each stage check the relevant invariant:
1. **Reward** — rewards non-constant and correlated with completion quality; reward fn
   sees the right text (decode/strip didn't drop content it needs).
2. **Advantages** — non-zero when rewards vary; epsilons/clip bounds in range
   (`0 < eps << 1`); group size `G > 2` (small `G` makes `std` noisy/undefined).
3. **Log-probs** — non-positive; match `F.log_softmax`; dominant token's log-prob ≈ 0.
4. **Loss** — changes across steps; KL vs policy-gradient term balanced; clip fraction
   not near 100%.
5. **Generation/decoding** — padding/artefacts stripped; every completion shape
   (incl. degenerate: no markers, prefix-only, suffix-only) survives decode non-empty.

**Fix, don't rewrite.** A bug in a branched function is a bug in one branch — other
callers rely on the rest. Replace a wrong constant (epsilon, sign, clip bound) with a
correct one; don't delete the surrounding numerical-stability logic. If your diff
collapses a multi-branch function to a one-liner, you probably broke a contract.

`references/common-pitfalls.md` (pitfall catalog with symptoms) and
`references/diagnostic-workflow.md` (stage-by-stage procedures with snippets) are bundled
for deep reference; you shouldn't need them for the flow above.

```act.verify_pipeline
CLI python3 ./scripts/verify_pipeline.py
```
