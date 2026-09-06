# CAD design loop

This workflow keeps geometric validity and visual quality as separate gates.
Passing the build checks is necessary, but it does not establish that a design
is expressive, coherent, ergonomic, or faithful to its brief.

## 1. Brief Gate

Before modelling, place the original request and the current answers in
`designs/<design-name>/SPEC.md`. Ask focused questions until all material items
below are either answered or explicitly recorded as designer assumptions.

- Purpose, user, environment, and intended manufacturing process
- Exact envelope, interfaces, clearances, loads, and safety-sensitive details
- Desired character, emotional qualities, and visual references
- Preferred and disliked forms, motifs, proportions, and surface treatments
- Important viewing angles, silhouettes, negative spaces, and touch points
- Which requirements are fixed and where expressive freedom is welcome
- The criteria by which the user will decide that the design is successful

Questions should expose consequential choices. The user need not prescribe
CadQuery operations, spline control points, or other implementation details.
When a reference image is supplied, distinguish visible evidence from inferred
dimensions and record that distinction in the specification.

The Brief Gate passes only when another competent designer could explain what
the object should feel like, what it must do, and how success will be judged.

## 2. Divergent form exploration

For appearance-led work whose form is not already fixed, create at least three
meaningfully different form directions. Explore the dominant silhouette,
proportional rhythm, negative space, and how features grow out of the primary
body before adding small details.

Concept images may be generated to explore shape language. Treat them as
inspiration unless the specification explicitly identifies a dimension as
known. Generated views may be geometrically inconsistent with one another.

Prefer named section curves, spline profiles, guide paths, changing
cross-sections, lofts, sweeps, revolves, and deliberate blends where they serve
the brief. Primitive solids remain appropriate when the intended form calls for
them; they should not be the automatic design vocabulary.

If several directions satisfy the brief and choosing among them is a matter of
taste, render the variants and ask the user to select or combine them.

## 3. Build and render

Run both commands after each meaningful geometry pass:

```bash
uv run python scripts/build.py <design-name>
uv run python scripts/render.py <design-name>
```

The renderer writes fixed orthographic, perspective, silhouette, edge, and
clipped-section views plus `output/<design-name>/renders/contact_sheet.png`.
Fixed cameras make regressions and subtle proportional changes easier to see.

## 4. Visual inspection

The agent must open and ingest the contact sheet with an image-viewing tool.
When concept or reference images exist in `designs/<design-name>/refs/`, inspect
the relevant images in the same review. Compare the current geometry against:

1. The original request and explicit visual acceptance criteria in `SPEC.md`
2. The selected concept or reference images
3. The previous accepted iteration, when one exists

Do not infer hidden geometry from a beauty view. Use the orthographic, top, rear,
and clipped-section views to inspect occluded regions and transitions.

## 5. Review rubric

Write a short review with evidence from named views. Score each applicable item
from 1 (poor) to 5 (excellent), and explain scores below 4.

- Fidelity to the brief and selected references
- Primary silhouette and proportion
- Surface flow and continuity
- Feature integration and transitions
- Negative space and visual balance
- Detail hierarchy and distinctiveness
- Ergonomics and apparent usability
- Manufacturability and print orientation

Then record:

- The strongest aspect worth preserving
- Up to three highest-impact defects
- The precise geometric or parameter changes proposed next
- Any choice that requires the user's taste rather than engineering judgment

A valid solid, a plausible render, or an average rubric score is not a stopping
condition. Any unresolved defect that materially contradicts the brief requires
another iteration or explicit user acceptance.

## 6. Iterate and converge

Change the smallest coherent set of parameters or construction decisions that
addresses the review. Rebuild, rerender, and reinspect. Compare rather than
judging the new render from memory. Avoid polishing secondary details while the
silhouette or primary transitions remain unresolved.

The loop ends when:

- Build and design-specific validations pass
- The latest contact sheet has been ingested and reviewed
- No material visual defect remains against the recorded brief, or the user has
  explicitly accepted the tradeoff
- Assumptions and any image-based inferences are current in `SPEC.md`

The completion report includes the bounding box, validation results, visual
review outcome, number of visual iterations, and remaining assumptions.
