# AI CAD

This repository stores editable, parametric CadQuery designs. All dimensions are
millimetres. Python source, parameters, and each design's specification are the
source of truth; STEP and STL are reproducible exports.

## Commands

Build a design from the repository root:

```bash
uv run python scripts/build.py test_plate
```

Inspect the exported STL interactively:

```bash
uv run python scripts/view.py output/test_plate/part.stl
```

The viewer opens a VTK window. Drag to rotate, use the mouse wheel to zoom, and
shift-drag to pan. Close the window to return to the terminal.

## Design layout

Each design lives in `designs/<design-name>/` and contains:

- `SPEC.md` — known, derived, and inferred requirements
- `parameters.py` — named dimensions and design choices
- `part.py` — a `build_model()` function returning a CadQuery solid
- `refs/` — user-provided reference images or documents

Exports are written to `output/<design-name>/` and are intentionally ignored by
Git.

