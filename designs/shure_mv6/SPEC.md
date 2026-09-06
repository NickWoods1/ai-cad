# Shure MV6 desk microphone reconstruction

## Original request

Reconstruct the user's desk microphone from the seven photographs named
`mic1.jpg` through `mic7.jpg` in Downloads. Analyse all views, build a 3D model,
and iterate through rendered comparisons until the reconstruction is convincing.

## Brief Gate

- Purpose: full-scale static visual/printable reconstruction, not a working
  microphone, replacement housing, or load-rated stand.
- User/environment: personal desk object photographed in its normal desktop pose.
- Manufacturing assumption: single-solid FDM/resin-printable display model.
- Character: faithful industrial-product reconstruction; no stylistic redesign.
- Fixed features: microphone, foam windscreen, green collar, mute button,
  ventilation recesses, tilt mount, post, and circular base.
- Expressive freedom: only in simplifying sub-millimetre surface texture,
  connectors, fasteners, and internal construction that photographs cannot show.
- Success criteria: the side, front, rear, top, and three-quarter silhouettes
  must agree with the supplied views; feature spacing must read unmistakably as
  the photographed MV6; the final output must be one valid solid with its base
  on Z=0.

## References and evidence

- User photographs: `/home/nick/Downloads/mic1.jpg` ... `mic7.jpg`. These cover
  both sides, front, rear, top, and elevated three-quarter views.
- The rear face visibly carries an `MV6` mark, establishing the product identity.
- Shure's published specification gives microphone length 169 mm, nominal
  microphone diameter 51 mm, and assembled dimensions 295 x 169 x 127 mm.
- Shure's product page describes the included base as 12 cm round.

## Exact manufacturer dimensions

- Microphone length: 169 mm.
- Nominal microphone diameter: 51 mm.
- Included round base diameter: 120 mm.
- Published mounted assembly height: 295 mm.

The ordering of all three published assembly axes is not used as a measured
constraint because the product literature does not provide a dimensioned
orthographic drawing. The known 169 mm length and 120 mm base anchor the model.

## User-directed proportional refinement

After inspecting the first reconstruction, the user requested a slightly larger
base, shorter arm/post, and clearly raised SHURE lettering. The revised display
model intentionally departs from the manufacturer envelope:

- Base diameter: 134 mm, increased from the published 120 mm.
- Overall height: 275 mm, reduced from the published 295 mm by lowering the
  microphone, mount, post top, and adjustment collar together by 20 mm.
- SHURE lettering: 11.5 mm nominal text size with 1.2 mm visible relief and a
  1.3 mm embedded root.

## Image-derived dimensions and assumptions

The following are proportional inferences from perspective photographs, not
measurements:

- Windshield length 70 mm and maximum rounded-square section 58 x 58 mm,
  formed through five named superellipse stations to reproduce the taper.
- Green collar length 4 mm and section 54 x 54 mm.
- Shell starts at X=-14.5 mm and ends at X=84.5 mm. Four named superellipse
  stations soften it toward a 46.4 mm rear cap.
- Microphone axis Z=246 mm, chosen so the 58 mm windscreen reaches the revised
  275 mm assembly height.
- Base height 10 mm, post diameter 17 mm, post top Z=198 mm, and a 19.5 mm
  adjustment collar at the post/fork transition.
- Vent, mute-button, rear-port, mount, pivot, seam, and logo sizes/locations are
  inferred by reconciling all seven views.
- The shell and foam are modeled as smoothly rounded solids. Foam pores, paint
  grain, cables, rubber underside texture, screw drives, and internal parts are
  omitted because they do not improve printable macro-form fidelity.
- The SHURE wordmark uses DejaVu Sans Bold as a legible geometric approximation;
  it is not represented as the exact trademark artwork. It has 1.2 mm visible
  relief and a named 1.3 mm root embed so all glyphs fuse to the curved shell.

## Coordinate and print convention

- Z is vertical; the circular base rests on Z=0.
- X follows the microphone axis, negative toward the foam/front.
- Y spans the base and microphone sides.
- The microphone is centred on X=0, while the stand axis is at X=17.5 mm beneath
  the photographed pivot location. This deliberate centring exception captures
  the microphone's forward overhang while keeping the dominant body centred.
- The full assembly is fused into one solid for robust export. This intentionally
  makes the tilt joint static and non-functional.
- The horizontal microphone and underside mount will require supports for a
  one-piece print. Splitting for support-free manufacturing is outside this
  reconstruction brief.

## Visual acceptance checks

- Side: 169 mm long body with the foam/collar/shell rhythm and four side dimples.
- Front: softly squared foam, not a circular cylinder.
- Top: green pill button and fine axial seam centered on the shell.
- Rear: rounded shell end with distinct USB-C and headphone recesses.
- Stand: low 120 mm disc, slim post, compact fork and visible pivot heads.
- Three-quarter: microphone appears balanced over the base like the photographed
  object, without blocky transitions or detached-looking details.
