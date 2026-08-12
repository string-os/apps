---
title: Threejs
name: threejs
namespace: stringhub
type: app
version: 0.2.0
description: "Three.js scene-graph parsing and export workflows: mesh baking, InstancedMesh expansion, part partitioning, per-link OBJ export, and URDF articulation."
tags: [threejs, 3d, scene-graph, urdf]
---

# Three.js Scene Graph + Export

Parse a Three.js scene module (`createScene()`) and export geometry. The actions
run the underlying Node/three.js code — bake world transforms, expand
InstancedMesh, partition named groups into parts/links — so you call an action with
file paths instead of writing the export logic yourself.

Every action's flags are listed inline below (required unless shown in `[...]`, which
marks an optional flag with its default). You should not need `/act.<name> --help`.

## Export
- **`/act.export_instanced_obj`** (no flags) — bake the whole scene (expanding every InstancedMesh) into one merged OBJ. Fixed I/O paths `/root/data/object.js` → `/root/output/object.obj` (hardcoded in the script). Use when you need a single combined mesh.
- **`/act.export_link_objs`** `--input <scene.js>` `--out_dir <dir>` `[--include_root]` (default off) — one OBJ per named group (link/part), meshes assigned to their nearest named ancestor. `--include_root` carries the literal sub-flag (pass `--include_root "--include-root"`) to also export the root group. Use when you need parts kept separate.
- **`/act.build_urdf_from_scene`** `--input <scene.js>` `--output <file.urdf>` `--mesh_dir <dir>` `[--robot_name <name>]` (default `object`) `[--joint_default fixed|revolute|prismatic]` (default `fixed`) — emit a minimal URDF treating named groups as links (parent = nearest named ancestor link), referencing per-link meshes in `--mesh_dir`. Run `export_link_objs` first to produce those meshes.

## Decision
- One combined mesh → `export_instanced_obj`. Separate parts → `export_link_objs`. Articulated robot (links + joints) → `export_link_objs` then `build_urdf_from_scene`.
- Joints default to `fixed`; override per-link only with structural evidence, not name guesses (see `references/joint-type-heuristics.md`).
- Link-selection / per-part export rules live in `references/link-export-rules.md`; the URDF schema in `references/urdf-minimal.md`. Bundled for deep reference — you shouldn't need to read them for the flow above.

```act.export_instanced_obj
CLI node ./scripts/export_instanced_obj.mjs
```
*Note: this script reads `/root/data/object.js` and writes `/root/output/object.obj`; those paths are hardcoded in the script. Edit the script to change them.*

```act.export_link_objs
CLI node ./scripts/export_link_objs.mjs --input "{input}" --out-dir "{out_dir}" {include_root}
  input: string (required) "Path to the scene .js module exporting createScene()"
  out_dir: string (required) "Directory to write per-link .obj files into"
  include_root: string (optional) "Pass --include-root to also export the root group" = ""
```

```act.build_urdf_from_scene
CLI node ./scripts/build_urdf_from_scene.mjs --input "{input}" --output "{output}" --mesh-dir "{mesh_dir}" --robot-name "{robot_name}" --joint-default "{joint_default}"
  input: string (required) "Path to the scene .js module exporting createScene()"
  output: string (required) "Output .urdf file path"
  mesh_dir: string (required) "Directory holding the per-link mesh files referenced by the URDF"
  robot_name: string (optional) "Robot name (default object)" = "object"
  joint_default: string (optional) "Default joint type: fixed|revolute|prismatic" = "fixed"
```
