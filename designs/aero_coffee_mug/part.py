"""CadQuery model for an American Art Deco coffee mug."""

from __future__ import annotations

import cadquery as cq

from parameters import (
    BASE_OUTER_RADIUS,
    BASE_THICKNESS,
    BODY_HEIGHT,
    CROWN_BOTTOM_Z,
    CROWN_HEIGHT,
    CROWN_INNER_RADIUS,
    CROWN_OUTER_DIAMETER,
    FLUTE_CENTER_RADIUS,
    FLUTE_CENTER_Z,
    FLUTE_COUNT,
    FLUTE_DEPTH,
    FLUTE_HEIGHT,
    FLUTE_WIDTH,
    HANDLE_CENTER_X,
    HANDLE_CENTER_Z,
    HANDLE_CORNER_RADIUS,
    HANDLE_INNER_HEIGHT,
    HANDLE_INNER_WIDTH,
    HANDLE_OUTER_DEPTH,
    HANDLE_OUTER_HEIGHT,
    HANDLE_OUTER_WIDTH,
    LOWER_TIER_HEIGHT,
    LOWER_TIER_OUTER_DIAMETER,
    MIDDLE_TIER_HEIGHT,
    MIDDLE_TIER_OUTER_DIAMETER,
    TIER_INNER_RADIUS,
    TIER_SIDES,
    TOP_OUTER_RADIUS,
    UPPER_TIER_HEIGHT,
    UPPER_TIER_OUTER_DIAMETER,
    WALL_THICKNESS,
)


def box_at(width: float, depth: float, height: float, center_x: float, center_y: float, center_z: float) -> cq.Workplane:
    """Create an axis-aligned box positioned by its centre."""
    return cq.Workplane("XY").box(width, depth, height).translate((center_x, center_y, center_z))


def octagonal_band(outer_diameter: float, inner_radius: float, height: float, bottom_z: float) -> cq.Workplane:
    """Create a hollow octagonal band at the requested height."""
    outer = cq.Workplane("XY").polygon(TIER_SIDES, outer_diameter).extrude(height).translate((0, 0, bottom_z))
    inner = cq.Workplane("XY").circle(inner_radius).extrude(height).translate((0, 0, bottom_z))
    return outer.cut(inner)


def build_model() -> cq.Workplane:
    """Return a hollow, single-solid Art Deco mug centred in X/Y with base at Z=0."""
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

    # Stepped lower plinth: an Art Deco architectural silhouette which leaves
    # the drinking cavity unobstructed.
    lower_bottom = 0.0
    middle_bottom = lower_bottom + LOWER_TIER_HEIGHT
    upper_bottom = middle_bottom + MIDDLE_TIER_HEIGHT
    mug = mug.union(octagonal_band(LOWER_TIER_OUTER_DIAMETER, TIER_INNER_RADIUS, LOWER_TIER_HEIGHT, lower_bottom))
    mug = mug.union(octagonal_band(MIDDLE_TIER_OUTER_DIAMETER, TIER_INNER_RADIUS, MIDDLE_TIER_HEIGHT, middle_bottom))
    mug = mug.union(octagonal_band(UPPER_TIER_OUTER_DIAMETER, TIER_INNER_RADIUS, UPPER_TIER_HEIGHT, upper_bottom))
    mug = mug.union(octagonal_band(CROWN_OUTER_DIAMETER, CROWN_INNER_RADIUS, CROWN_HEIGHT, CROWN_BOTTOM_Z))

    # Slender raised flutes provide the vertical, sunburst-like rhythm of an
    # American Art Deco facade. Each overlaps the cup's curved wall.
    for index in range(FLUTE_COUNT):
        angle = index * 360.0 / FLUTE_COUNT
        flute = box_at(FLUTE_WIDTH, FLUTE_DEPTH, FLUTE_HEIGHT, 0, -FLUTE_CENTER_RADIUS, FLUTE_CENTER_Z)
        mug = mug.union(flute.rotate((0, 0, 0), (0, 0, 1), angle))

    # A rectangular ring with modest corner rounding continues the stepped,
    # architectural theme while preserving a generous finger opening.
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
