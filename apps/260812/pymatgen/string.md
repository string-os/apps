---
title: Pymatgen
name: pymatgen
namespace: stringhub
type: app
version: 0.2.0
description: "Materials science toolkit. Crystal structures (CIF, POSCAR), phase diagrams, band structure, DOS, Materials Project integration, format conversion, for computational materials science."
tags: [pymatgen, materials, crystal, wyckoff]
---

# Pymatgen

Analyze and convert crystal structures and compute phase diagrams via three bundled
pymatgen tools. The daemon runs the pymatgen code — call an action with file paths/flags
instead of writing the library calls yourself. Actions print results to stdout (and can
export to a file). Needs pymatgen installed; phase diagrams also need a Materials Project
API key (`MP_API_KEY`).

Every action's flags are listed inline below (required unless shown in `[...]`, which
marks an optional flag with its default). Toggle flags carry the literal sub-flag as their
value, so you pass them with the `=` form (e.g. `--symmetry=--symmetry`). You should not
need `/act.<name> --help`.

## Convert
- **`/act.structure_converter`** `--input <file|glob>` `[--output <file>]` (default empty)
  `[--format_flag "<--format fmt>"]` (default empty) `[--output_dir_flag "<--output-dir dir>"]`
  (default empty) — convert a structure file between formats (CIF, POSCAR, XYZ, JSON, YAML, …).
  Single file → set `--output`; batch a wildcard `--input` pattern → set
  `--output_dir_flag "--output-dir <dir>"`. Set format with `--format_flag "--format cif"`.

## Analyze
- **`/act.structure_analyzer`** `--structure_file <file>` `[--symmetry=--symmetry]`
  `[--neighbors=--neighbors]` `[--distances=--distances]` `[--export_flag "<--export json|yaml>"]`
  (all default off/empty) — inspect one structure. The three toggles each carry the literal
  sub-flag as their value, so pass them with the `=` form: `--symmetry=--symmetry` (space
  group + symmetry), `--neighbors=--neighbors` (coordination environment),
  `--distances=--distances` (distance matrix, ≤20 atoms). Export results with
  `--export_flag "--export json"`.

## Phase diagram / stability
- **`/act.phase_diagram_generator`** `--chemsys <A-B-O>` `[--output_flag "<--output file>"]`
  `[--analyze_flag "<--analyze composition>"]` (both default empty) — build a phase diagram
  for a chemical system (e.g. `Li-Fe-O`) from Materials Project data. `--analyze_flag "--analyze LiFeO2"`
  checks a composition's stability; `--output_flag "--output pd.png"` saves the plot.
  (Needs an `MP_API_KEY` and network — not required for the Wyckoff path below.)

## Wyckoff positions (this task's key path)
Run `/act.structure_analyzer --structure_file <cif> --symmetry=--symmetry` to get the space
group, then read Wyckoff letters / multiplicities / representative fractional coordinates.
Gotcha worth knowing: use `get_symmetry_dataset().wyckoffs`, NOT
`get_symmetrized_structure().wyckoff_symbols`. Full recipe is in
`references/wyckoff-positions-from-cif.md`.

`references/` (core_classes, analysis_modules, io_formats, transformations_workflows,
materials_project_api, wyckoff-positions-from-cif) are bundled for deep reference; you
shouldn't need them beyond the Wyckoff note above.

```act.structure_converter
CLI python3 ./scripts/structure_converter.py "{input}" "{output}" {format_flag} {output_dir_flag}
  input: string (required) "Input structure file (CIF, POSCAR, etc.); supports wildcards for batch conversion"
  output: string (optional) "Output structure file (ignored if --output-dir is used)" = ""
  format_flag: string (optional) "Pass --format <fmt> to set output format (e.g. cif, poscar, json)" = ""
  output_dir_flag: string (optional) "Pass --output-dir <dir> for batch conversion" = ""
```

```act.structure_analyzer
CLI python3 ./scripts/structure_analyzer.py "{structure_file}" {symmetry} {neighbors} {distances} {export_flag}
  structure_file: string (required) "Structure file to analyze (CIF, POSCAR, etc.)"
  symmetry: string (optional) "Pass --symmetry to perform symmetry analysis" = ""
  neighbors: string (optional) "Pass --neighbors to analyze coordination environment" = ""
  distances: string (optional) "Pass --distances to show the distance matrix" = ""
  export_flag: string (optional) "Pass --export json|yaml to export results" = ""
```

```act.phase_diagram_generator
CLI python3 ./scripts/phase_diagram_generator.py "{chemsys}" {output_flag} {analyze_flag}
  chemsys: string (required) "Chemical system, e.g. Li-Fe-O"
  output_flag: string (optional) "Pass --output <file> to save the phase diagram plot" = ""
  analyze_flag: string (optional) "Pass --analyze <composition> to analyze stability, e.g. --analyze LiFeO2" = ""
```
