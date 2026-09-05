"""CadQuery model for a miniature generic bicycle delivery backpack."""

from __future__ import annotations

import cadquery as cq

from parameters import (
    BODY_DEPTH,
    BODY_HEIGHT,
    BODY_WIDTH,
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
    WORDMARK_CENTER_Z,
    WORDMARK_FONT,
    WORDMARK_FONT_SIZE,
    WORDMARK_FUSION_OVERLAP,
    WORDMARK_TEXT,
    WORDMARK_THICKNESS,
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

    # Raised branded wordmark. Its small overlap embeds it in the flap instead
    # of merely touching the face, producing one robust printable solid.
    front_outer_y = front_y - FRONT_FLAP_THICKNESS / 2.0
    wordmark = (
        cq.Workplane("XZ")
        .text(
            WORDMARK_TEXT,
            WORDMARK_FONT_SIZE,
            WORDMARK_THICKNESS,
            font=WORDMARK_FONT,
            kind="bold",
            halign="center",
            valign="center",
        )
        .translate((0, front_outer_y + WORDMARK_FUSION_OVERLAP, WORDMARK_CENTER_Z))
    )
    bag = bag.union(wordmark)

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
