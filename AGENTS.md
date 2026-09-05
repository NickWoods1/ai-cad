# CAD repository instructions

## Source and outputs

- Use CadQuery for all CAD geometry. Dimensions are millimetres.
- Treat `parameters.py`, `part.py`, and `SPEC.md` as editable source of truth.
  STEP and STL are derived exports.
- Each design implements `build_model()` in `part.py` and has named,
  concept-level parameters. Do not hide important dimensions in geometry calls.
- Keep all geometry centred on X/Y where practical and put the print-facing base
  on Z=0. Record an exception in the design specification.

## Requirements and assumptions

- Write exact dimensions, derived dimensions, and image-based inferences in
  `SPEC.md`. Never describe inferred dimensions as measured facts.
- Do not alter an explicit dimension for print clearance without making the
  compensation a named parameter and recording it in the specification.
- Ask for missing decisions that materially affect fit, use, or safety.

## Build and verification

- Build with `uv run python scripts/build.py <design-name>`.
- A successful build must validate solids and design-specific checks, then export
  `output/<design-name>/part.step` and `part.stl`.
- Do not claim a model is verified until the build has run successfully. Report
  its bounding box, validation results, and assumptions.
- View an exported STL with `uv run python scripts/view.py output/<design-name>/part.stl`.

