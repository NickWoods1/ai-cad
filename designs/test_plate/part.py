"""Parametric two-hole plate used to verify the CAD pipeline."""

from __future__ import annotations

import cadquery as cq

from parameters import CORNER_RADIUS, DEPTH, HOLE_DIAMETER, HOLE_SPACING, THICKNESS, WIDTH


def build_model() -> cq.Workplane:
    """Return one plate solid, centred in X/Y with its bottom on Z=0."""
    plate = (
        cq.Workplane("XY")
        .rect(WIDTH, DEPTH)
        .extrude(THICKNESS)
        .edges("|Z")
        .fillet(CORNER_RADIUS)
    )
    hole_x = HOLE_SPACING / 2.0
    return plate.faces(">Z").workplane().pushPoints([(-hole_x, 0), (hole_x, 0)]).hole(HOLE_DIAMETER)

