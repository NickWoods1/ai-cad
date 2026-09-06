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
- Before creating or substantially revising geometry, complete the Brief Gate
  in `DESIGN_LOOP.md`. Ask focused questions until the design intent and every
  decision that materially affects appearance, fit, use, manufacturing, or
  safety is resolved. Do not substitute a generic aesthetic when the user's
  taste is still ambiguous. Do not ask the user to choose implementation
  details that can be derived from the agreed intent.
- Preserve the original request, selected references, assumptions, and visual
  acceptance criteria in `SPEC.md` so later renders can be compared with the
  initial intent rather than judged in isolation.

## Visual design loop

- Follow `DESIGN_LOOP.md` for every new design and every change whose success
  depends on appearance, ergonomics, or surface quality.
- For an expressive design without an established direction, explore at least
  three materially different silhouette or form variants before committing to
  detail. Variants must differ in concept, not only in fillet radius or scale.
- After each meaningful geometry pass, build and then render with
  `uv run python scripts/render.py <design-name>`.
- Ingest `output/<design-name>/renders/contact_sheet.png` with an image-viewing
  tool. Merely creating the PNG is not visual inspection. Inspect relevant
  reference images alongside it and explicitly compare the model with the
  original brief and the previous accepted iteration.
- Record the visual review using the rubric in `DESIGN_LOOP.md`. Name concrete
  strengths, defects, and the next geometric changes. If a material visual
  defect remains, revise the model and repeat the build-render-inspect-review
  cycle. Do not call a design complete because the solid is valid.
- Ask the user for a taste decision when two or more viable directions remain
  and the choice would materially change the design. Present rendered variants
  for that decision whenever practical.

## Build and verification

- Build with `uv run python scripts/build.py <design-name>`.
- A successful build must validate solids and design-specific checks, then export
  `output/<design-name>/part.step` and `part.stl`.
- Do not claim a model is verified until the build has run successfully. Report
  its bounding box, validation results, and assumptions.
- Do not claim an appearance-dependent model is complete until its latest
  contact sheet has been visually inspected and its review has no unresolved
  material defects, or the user has explicitly accepted those tradeoffs.
- View an exported STL with `uv run python scripts/view.py output/<design-name>/part.stl`.
