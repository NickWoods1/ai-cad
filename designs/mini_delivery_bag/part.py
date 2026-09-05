"""CadQuery model for a miniature generic bicycle delivery backpack."""

from __future__ import annotations

import cadquery as cq

from parameters import (
    BADGE_SIZE,
    BODY_DEPTH,
    BODY_HEIGHT,
    BODY_WIDTH,
    DETAIL_BAND_HEIGHT,
    DETAIL_BAND_SPACING,
    DETAIL_RECESS_DEPTH,
    FRONT_FLAP_CENTER_Z,
    FRONT_FLAP_HEIGHT,
    FRONT_FLAP_THICKNESS,
    FRONT_FLAP_WIDTH,
    FUSION_OVERLAP,
    HANDLE_DEPTH,
    HANDLE_HEIGHT,
    HANDLE_WIDTH,
    STRAP_CENTER_Z,
    STRAP_CROSSBAR_CENTER_Z,
    STRAP_CROSSBAR_HEIGHT,
    STRAP_HEIGHT,
    STRAP_THICKNESS,
    STRAP_WIDTH,
    STRAP_X_OFFSET,
    VERTICAL_CORNER_RADIUS,
)


def box_at(width: float, depth: float, height: float, center_x: float, center_y: float, center_z: float) -> cq.Workplane:
    """Create an axis-aligned box positioned by its centre."""
    return cq.Workplane("XY").box(width, depth, height).translate((center_x, center_y, center_z))


def build_model() -> cq.Workplane:
    """Return one printable display solid, centred in X/Y with base at Z=0."""
    body = (
        cq.Workplane("XY")
        .box(BODY_WIDTH, BODY_DEPTH, BODY_HEIGHT)
        .translate((0, 0, BODY_HEIGHT / 2.0))
        .edges("|Z")
        .fillet(VERTICAL_CORNER_RADIUS)
    )

    front_y = -BODY_DEPTH / 2.0 - FRONT_FLAP_THICKNESS / 2.0 + FUSION_OVERLAP
    flap = box_at(
        FRONT_FLAP_WIDTH,
        FRONT_FLAP_THICKNESS,
        FRONT_FLAP_HEIGHT,
        0,
        front_y,
        FRONT_FLAP_CENTER_Z,
    )
    bag = body.union(flap)

    # Recessed horizontal bands and a diamond badge make a graphic front panel
    # without copying a delivery company logo.
    front_outer_y = front_y - FRONT_FLAP_THICKNESS / 2.0
    detail_y = front_outer_y + DETAIL_RECESS_DEPTH / 2.0
    for z_offset in (-DETAIL_BAND_SPACING / 2.0, DETAIL_BAND_SPACING / 2.0):
        band = box_at(
            FRONT_FLAP_WIDTH * 0.62,
            DETAIL_RECESS_DEPTH,
            DETAIL_BAND_HEIGHT,
            0,
            detail_y,
            FRONT_FLAP_CENTER_Z + z_offset,
        )
        bag = bag.cut(band)

    badge = box_at(BADGE_SIZE, DETAIL_RECESS_DEPTH, BADGE_SIZE, 0, detail_y, FRONT_FLAP_CENTER_Z + 21.0)
    badge = badge.rotate((0, 0, 0), (0, 1, 0), 45)
    bag = bag.cut(badge)

    # These raised rear straps and crossbar are fused cosmetic details.  They
    # give the reverse side a wearable-rider backpack character.
    rear_y = BODY_DEPTH / 2.0 + STRAP_THICKNESS / 2.0 - FUSION_OVERLAP
    for x in (-STRAP_X_OFFSET, STRAP_X_OFFSET):
        bag = bag.union(box_at(STRAP_WIDTH, STRAP_THICKNESS, STRAP_HEIGHT, x, rear_y, STRAP_CENTER_Z))
    bag = bag.union(
        box_at(BODY_WIDTH - 18.0, STRAP_THICKNESS, STRAP_CROSSBAR_HEIGHT, 0, rear_y, STRAP_CROSSBAR_CENTER_Z)
    )

    # A simple, robust solid carry handle: it rises above the top but remains
    # fully fused to the body, so it prints reliably as part of the model.
    bag = bag.union(
        box_at(HANDLE_WIDTH, HANDLE_DEPTH, HANDLE_HEIGHT, 0, 0, BODY_HEIGHT + HANDLE_HEIGHT / 2.0 - FUSION_OVERLAP)
    )
    return bag
