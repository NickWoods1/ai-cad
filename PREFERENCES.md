# Shared CAD preferences

These are defaults for new designs. Exact requirements in a design's `SPEC.md`
override them.

- Units: millimetres.
- Coordinate convention: centre geometry on X/Y where practical; use Z=0 as the
  intended print-facing base.
- Geometry: prefer named, semantic CadQuery operations over mesh manipulation.
- Outputs: export one STEP and one STL from the same validated CadQuery model.
- Repository policy: do not track generated STEP/STL files unless a design later
  needs release artifacts committed deliberately.
- Manufacturing: do not add clearance, wall thickness, support, or orientation
  assumptions unless they are named and recorded for the specific design.

