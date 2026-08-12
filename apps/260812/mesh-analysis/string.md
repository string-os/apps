---
title: Mesh Analysis
name: mesh-analysis
namespace: stringhub
type: app
version: 0.2.0
description: "Analyzes 3D mesh files (STL) to calculate geometric properties (volume, components) and extract attribute data. Use this skill to process noisy 3D scan data and filter debris."
tags: [mesh, stl, 3d-scan, geometry, volume]
---

# Mesh Analysis

Analyze 3D-scan STL meshes through actions — the daemon runs the mesh tool, so you call
an action with the STL path instead of importing the module. Binary STL (including the
2-byte attribute used for material/color ID) is handled automatically; ASCII STL falls
back to no material IDs. All actions print JSON.

## Actions
- **`/act.analyze`** `--stl <path>` — the main operation for a noisy scan: isolate the **largest
  connected component** (filters out scan debris) and return its volume + material ID, plus the
  total component count.
- **`/act.components`** `--stl <path>` — list **every** connected component with its volume,
  material ID, and triangle count, largest first — useful to see how dirty the scan is.
- **`/act.volume`** `--stl <path>` — signed-mesh volume of the whole file, no component filtering.

## Computing mass
The tool returns **Volume** and **Material ID**, not mass. To get mass:
1. Read `material_id` from `/act.analyze`.
2. Look up that ID's density in the task's material / density reference data.
3. `mass = volume × density`.

**Units:** the volume is in the STL's own coordinate units, **cubed** — do not assume mm or
inches; check the task instructions for the coordinate system. If the density table uses the
same unit (e.g. g/cm³ with cm³), multiply directly — no conversion needed.

```act.analyze
CLI python3 ./scripts/mesh_cli.py analyze "{stl}"
  stl: string (required) "Path to the STL file to analyze"
```

```act.components
CLI python3 ./scripts/mesh_cli.py components "{stl}"
  stl: string (required) "Path to the STL file"
```

```act.volume
CLI python3 ./scripts/mesh_cli.py volume "{stl}"
  stl: string (required) "Path to the STL file"
```
