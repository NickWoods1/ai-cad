# Soft geometric Art Deco coffee mug

## Original request and design intent

Redesign the earlier American Art Deco mug because its primitive bands,
rectangular flutes, and block handle felt blocky and uninspired. The selected
direction is **soft geometric Deco**. Preserve approximately the earlier
proportions and capacity unless a strong aesthetic idea justifies a change. The
object is intended to be drinkable, while aesthetic quality has priority over
strict utilitarian optimization. The designer has latitude to make creative
form decisions within that direction.

## Visual acceptance criteria

- The silhouette must be governed by flowing geometry rather than stacked
  primitive solids.
- The handle must feel integrated with the body and provide an intentional,
  characteristic negative space.
- Deco character should arise from proportion, plan shape, and rhythmic section
  changes rather than applied rectangular ornament.
- The object should feel soft and approachable without becoming a generic round
  mug or a historical pastiche.
- Front, side, top, hero, low, and section views must all remain coherent.

## Exact design dimensions

- Body height: 95 mm.
- Base thickness: 5 mm.
- Nominal radial wall offset: 3.2 mm.
- Named maximum section width and depth: 87 mm at the shoulder section.
- Handle depth: 15 mm.
- Handle boundary rounding radius: 2.4 mm.
- Nominal handle opening envelope from its spline controls: 24 mm wide × 47 mm
  high. The interpolated spline spans 24.6665 mm × 48.8074 mm before its edge
  rounding is applied.
- Finished BREP envelope: 120.4122 mm wide × 87.5175 mm deep × 95 mm high.
- The body section heights, half-widths, superellipse exponents, and handle
  spline coordinates are exact named values in `parameters.py`.

## Derived dimensions and construction

- Six smooth superellipse sections form the base, restrained pedestal,
  lower-body contraction, shoulder, and rim as one continuous loft.
- A superellipse exponent of 2 would be circular. The named exponents from 2.35
  to 2.65 create a softly squared plan and a geometric fourfold rhythm.
- Interpolating the sampled superellipse sections as periodic B-splines creates
  a maximum 0.2587 mm outward deviation beyond the named 43.5 mm shoulder
  half-width. This accounts for the derived 87.5175 mm body envelope.
- The cavity follows corresponding sections with a nominal 3.2 mm radial offset.
  Because this is a radial XY offset rather than a surface-normal offset, exact
  wall thickness varies slightly on the curved transitions.
- The handle is a 15 mm deep spline ribbon with a rounded perimeter and a
  vertically stretched teardrop opening. Its roots overlap the cup body.
- The former three bands, crown band, and twelve rectangular flutes are removed.

## Exploration record

Three valid CadQuery form studies were rendered before selecting the final
direction:

- Concept A: restrained fourfold bell body and compact oval ribbon handle.
- Concept B: stronger soft-geometric body rhythm and tall teardrop handle.
- Concept C: broad streamline body and smaller low handle.

Concept B was selected as the strongest basis. A was too vase-like through the
waist, while C lost too much Deco identity. The selected geometry replaces the
study's phase-shifted harmonic plan with a symmetric superellipse so the final
object reads deliberately from top and orthographic views.

## Assumptions and inferences

- No physical reference object or measured reference image was supplied.
- “Soft geometric Deco” is interpreted as controlled symmetry, softened square
  sections, tapered rhythmic massing, and a characteristic arched opening.
- The geometric cavity is approximately 426.00 ml to the rim. This is a CAD
  volume, not a calibrated practical serving capacity.
- The finished solid contains 128.238 cm³ of material; the build validates this
  as a regression check on the hollow body and handle.
- The 15 mm handle depth and spline opening are designer-selected ergonomic
  assumptions and should ultimately be confirmed with a physical prototype.

## Print and use notes

- Print upright on the flat base. The arched handle avoids the former long flat
  bridge, but slicing is still required to assess local overhangs.
- A typical FDM print is not automatically food-safe or reliably watertight.
  Material certification, nozzle composition, layer sealing, finish, cleaning,
  and temperature resistance determine whether a physical print is suitable for
  drinking.
