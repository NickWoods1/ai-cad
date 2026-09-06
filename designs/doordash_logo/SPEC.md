# DoorDash logo extrusion

## Original request

Create a new 3D model of the DoorDash logo shown in the user-supplied image.
The user clarified that it should be a direct 3D version of the image: preserve
the flat graphic silhouette and extend it uniformly in depth.

## Brief Gate

- Purpose: a general-purpose solid rendering of the pictured logo; no mating,
  fastening, load-bearing, or safety-critical use was requested.
- Visual character: faithful to the supplied red silhouette, including the long
  tapered inlet, rounded outer return, and internal horizontal negative space.
- Fixed appearance: the 2D proportions and silhouette visible in the reference.
- Expressive freedom: limited to choosing physical scale because this is a logo
  reproduction, not an open-ended form exploration.
- Acceptance criteria: one clean solid; top silhouette closely matches the
  supplied image; uniform depth; no bevel, base plate, border, or added detail.
- Manufacturing: assumed to be a generic CAD/3D-printable solid, printed flat on
  its largest face. No process-specific compensation is applied.

## Dimensions and assumptions

All physical dimensions are millimetres.

- Overall width: **120.0** (designer assumption; reference has no physical scale)
- Uniform extrusion depth: **8.0** (designer assumption)
- Overall height: **68.0**, derived from the reference silhouette ratio
  `(263 - 29) / (438 - 25) * 120`
- Coordinate convention: profile centred on X/Y; lower print-facing face on Z=0

## Image-derived geometry

The supplied raster is 470 x 299 pixels. The visible red silhouette occupies an
inferred pixel envelope from X=25 to 438 and Y=29 to 263. Those are image-derived
observations, not physical measurements. A closed sequence of cubic Bézier
segments reconstructs the silhouette using named reference-space control points
in `parameters.py`; it is then scaled uniformly to the assumed 120 mm width.

Anti-aliased edge pixels and raster resolution prevent literal sub-pixel recovery
of the source vector artwork. The intended result is a smooth visual match to
the supplied image rather than a claim of access to DoorDash's original vector.

