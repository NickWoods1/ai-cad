"""CadQuery model for a faceted aero-tech coffee mug."""

from __future__ import annotations

import cadquery as cq

from parameters import (
    BASE_OUTER_RADIUS,
    BASE_THICKNESS,
    BODY_HEIGHT,
    CUFF_HEIGHT,
    CUFF_INNER_DIAMETER,
    CUFF_OUTER_DIAMETER,
    CUFF_SIDES,
    FIN_ANGLE,
    FIN_CENTER_Z,
    FIN_COUNT,
    FIN_DEPTH,
    FIN_HEIGHT,
    FIN_WIDTH,
    FIN_X_SPACING,
    HANDLE_CENTER_X,
    HANDLE_CENTER_Z,
    HANDLE_CORNER_RADIUS,
    HANDLE_INNER_HEIGHT,
    HANDLE_INNER_WIDTH,
    HANDLE_OUTER_DEPTH,
    HANDLE_OUTER_HEIGHT,
    HANDLE_OUTER_WIDTH,
    TOP_OUTER_RADIUS,
    WALL_THICKNESS,
)


def box_at(width: float, depth: float, height: float, center_x: float, center_y: float, center_z: float) -> cq.Workplane:
    """Create an axis-aligned box positioned by its centre."""
    return cq.Workplane("XY").box(width, depth, height).translate((center_x, center_y, center_z))


def build_model() -> cq.Workplane:
    """Return a hollow, single-solid mug centred in X/Y with base at Z=0."""
    outer_cup = (
        cq.Workplane("XY")
        .circle(BASE_OUTER_RADIUS)
        .workplane(offset=BODY_HEIGHT)
        .circle(TOP_OUTER_RADIUS)
        .loft(combine=True)
    )
    inner_cup = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .circle(BASE_OUTER_RADIUS - WALL_THICKNESS)
        .workplane(offset=BODY_HEIGHT - BASE_THICKNESS)
        .circle(TOP_OUTER_RADIUS - WALL_THICKNESS)
        .loft(combine=True)
    )
    mug = outer_cup.cut(inner_cup)

    # A wide octagonal cuff gives the lower half a protective, technical
    # silhouette while the round cup remains comfortable to hold.
    cuff_outer = cq.Workplane("XY").polygon(CUFF_SIDES, CUFF_OUTER_DIAMETER).extrude(CUFF_HEIGHT)
    cuff_inner = cq.Workplane("XY").polygon(CUFF_SIDES, CUFF_INNER_DIAMETER).extrude(CUFF_HEIGHT)
    mug = mug.union(cuff_outer.cut(cuff_inner))

    # Three diagonal front fins make a deliberate wraparound-sportswear style
    # visual grip. Their rear faces overlap the cuff for a robust union.
    fin_x_positions = [FIN_X_SPACING * (index - (FIN_COUNT - 1) / 2.0) for index in range(FIN_COUNT)]
    for x in fin_x_positions:
        fin = box_at(FIN_WIDTH, FIN_DEPTH, FIN_HEIGHT, x, -CUFF_OUTER_DIAMETER / 2.0 + FIN_DEPTH / 2.0, FIN_CENTER_Z)
        mug = mug.union(fin.rotate((x, -CUFF_OUTER_DIAMETER / 2.0 + FIN_DEPTH / 2.0, FIN_CENTER_Z), (x, -CUFF_OUTER_DIAMETER / 2.0 + FIN_DEPTH / 2.0 + 1.0, FIN_CENTER_Z), FIN_ANGLE))

    # The handle is a rounded rectangular ring, deliberately angular rather
    # than a conventional circular ear. It overlaps the cup at its left side.
    handle_outer = box_at(
        HANDLE_OUTER_WIDTH,
        HANDLE_OUTER_DEPTH,
        HANDLE_OUTER_HEIGHT,
        HANDLE_CENTER_X,
        0,
        HANDLE_CENTER_Z,
    ).edges("|Y").fillet(HANDLE_CORNER_RADIUS)
    handle_opening = box_at(
        HANDLE_INNER_WIDTH,
        HANDLE_OUTER_DEPTH + 2.0,
        HANDLE_INNER_HEIGHT,
        HANDLE_CENTER_X,
        0,
        HANDLE_CENTER_Z,
    )
    return mug.union(handle_outer.cut(handle_opening))
