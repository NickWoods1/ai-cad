"""CadQuery model of a stylised DoorDash insulated courier backpack miniature."""

from __future__ import annotations

import cadquery as cq

from parameters import *


def polygon_wire(points: list[cq.Vector]) -> cq.Wire:
    """Return a closed straight-edged wire through the supplied points."""
    return cq.Wire.makePolygon(points, close=True)


def rounded_rail(start: cq.Vector, end: cq.Vector, radius: float) -> cq.Solid:
    """Create a softly terminated raised piping cord between two points."""
    direction = end - start
    rail = cq.Solid.makeCylinder(radius, direction.Length, start, direction.normalized())
    return rail.fuse(cq.Solid.makeSphere(radius, start)).fuse(cq.Solid.makeSphere(radius, end))


def swept_tube(points: list[cq.Vector], radius: float) -> cq.Solid:
    """Sweep a circular toy-like strap or handle along a smooth open path."""
    path = cq.Edge.makeSpline(points)
    tangent = (points[1] - points[0]).normalized()
    profile = cq.Wire.makeCircle(radius, points[0], tangent)
    return cq.Solid.sweep(profile, [], path, makeSolid=True, isFrenet=True)


def swept_bezier_tube(points: list[cq.Vector], radius: float) -> cq.Solid:
    """Sweep a tube along one controlled cubic curve without spline ripples."""
    path = cq.Edge.makeBezier(points)
    tangent = (points[1] - points[0]).normalized()
    profile = cq.Wire.makeCircle(radius, points[0], tangent)
    return cq.Solid.sweep(profile, [], path, makeSolid=True, isFrenet=True)


def logo_point_front(
    point: tuple[float, float], width: float, center_x: float, center_z: float, y: float
) -> cq.Vector:
    """Map a reference-logo pixel to the front XZ plane."""
    scale = width / (LOGO_REFERENCE_X_MAX - LOGO_REFERENCE_X_MIN)
    centre_px = (LOGO_REFERENCE_X_MIN + LOGO_REFERENCE_X_MAX) / 2.0
    centre_py = (LOGO_REFERENCE_Y_MIN + LOGO_REFERENCE_Y_MAX) / 2.0
    return cq.Vector(center_x + (point[0] - centre_px) * scale, y, center_z + (centre_py - point[1]) * scale)


def logo_point_side(
    point: tuple[float, float], width: float, center_y: float, center_z: float, x: float
) -> cq.Vector:
    """Map a reference-logo pixel to the right-side YZ plane."""
    scale = width / (LOGO_REFERENCE_X_MAX - LOGO_REFERENCE_X_MIN)
    centre_px = (LOGO_REFERENCE_X_MIN + LOGO_REFERENCE_X_MAX) / 2.0
    centre_py = (LOGO_REFERENCE_Y_MIN + LOGO_REFERENCE_Y_MAX) / 2.0
    return cq.Vector(x, center_y + (point[0] - centre_px) * scale, center_z + (centre_py - point[1]) * scale)


def make_logo_front() -> cq.Solid:
    """Create the small raised mark paired with the front wordmark."""
    current = logo_point_front(LOGO_PROFILE_START, FRONT_LOGO_WIDTH, FRONT_LOGO_CENTER_X, FRONT_LOGO_CENTER_Z, FRONT_LOGO_START_Y)
    edges = []
    for control_1, control_2, end in LOGO_PROFILE_SEGMENTS:
        points = [current]
        points.extend(
            logo_point_front(point, FRONT_LOGO_WIDTH, FRONT_LOGO_CENTER_X, FRONT_LOGO_CENTER_Z, FRONT_LOGO_START_Y)
            for point in (control_1, control_2, end)
        )
        edges.append(cq.Edge.makeBezier(points))
        current = points[-1]
    wire = cq.Wire.assembleEdges(edges)
    return cq.Solid.extrudeLinear(wire, [], cq.Vector(0.0, -FRONT_LOGO_THICKNESS, 0.0))


def make_logo_side() -> cq.Solid:
    """Create the larger raised mark on the right side panel."""
    current = logo_point_side(LOGO_PROFILE_START, SIDE_LOGO_WIDTH, SIDE_LOGO_CENTER_Y, SIDE_LOGO_CENTER_Z, SIDE_LOGO_START_X)
    edges = []
    for control_1, control_2, end in LOGO_PROFILE_SEGMENTS:
        points = [current]
        points.extend(
            logo_point_side(point, SIDE_LOGO_WIDTH, SIDE_LOGO_CENTER_Y, SIDE_LOGO_CENTER_Z, SIDE_LOGO_START_X)
            for point in (control_1, control_2, end)
        )
        edges.append(cq.Edge.makeBezier(points))
        current = points[-1]
    wire = cq.Wire.assembleEdges(edges)
    return cq.Solid.extrudeLinear(wire, [], cq.Vector(SIDE_LOGO_THICKNESS, 0.0, 0.0))


def build_body() -> cq.Solid:
    """Build the faceted insulated case, top flap, and broad front panel."""
    body = (
        cq.Workplane("XY")
        .box(BODY_WIDTH, BODY_DEPTH, BODY_HEIGHT)
        .translate((0.0, 0.0, BODY_HEIGHT / 2.0))
        .edges("<Z")
        .chamfer(BOTTOM_CHAMFER)
        .edges(">Z")
        .chamfer(TOP_CHAMFER)
        .edges("|Z")
        .fillet(BODY_VERTICAL_RADIUS)
        .val()
    )
    flap = (
        cq.Workplane("XY")
        .box(TOP_FLAP_WIDTH, TOP_FLAP_DEPTH, TOP_FLAP_HEIGHT)
        .translate((0.0, 0.0, TOP_FLAP_CENTER_Z))
        .edges("|Z")
        .fillet(TOP_FLAP_CORNER_RADIUS)
        .val()
    )
    panel_wire = polygon_wire(
        [
            cq.Vector(-FRONT_PANEL_BOTTOM_HALF_WIDTH, FRONT_PANEL_BACK_Y, FRONT_PANEL_BOTTOM_Z),
            cq.Vector(FRONT_PANEL_BOTTOM_HALF_WIDTH, FRONT_PANEL_BACK_Y, FRONT_PANEL_BOTTOM_Z),
            cq.Vector(FRONT_PANEL_TOP_HALF_WIDTH, FRONT_PANEL_BACK_Y, FRONT_PANEL_TOP_Z),
            cq.Vector(-FRONT_PANEL_TOP_HALF_WIDTH, FRONT_PANEL_BACK_Y, FRONT_PANEL_TOP_Z),
        ]
    )
    panel = cq.Solid.extrudeLinear(panel_wire, [], cq.Vector(0.0, -FRONT_PANEL_THICKNESS, 0.0))
    return body.fuse(flap).fuse(panel)


def add_panel_piping(bag: cq.Solid) -> cq.Solid:
    """Add the prominent piping geometry around the face and top flap."""
    front_points = [
        cq.Vector(-FRONT_PANEL_BOTTOM_HALF_WIDTH, FRONT_PIPING_Y, FRONT_PANEL_BOTTOM_Z),
        cq.Vector(FRONT_PANEL_BOTTOM_HALF_WIDTH, FRONT_PIPING_Y, FRONT_PANEL_BOTTOM_Z),
        cq.Vector(FRONT_PANEL_TOP_HALF_WIDTH, FRONT_PIPING_Y, FRONT_PANEL_TOP_Z),
        cq.Vector(-FRONT_PANEL_TOP_HALF_WIDTH, FRONT_PIPING_Y, FRONT_PANEL_TOP_Z),
    ]
    for start, end in zip(front_points, front_points[1:] + front_points[:1], strict=True):
        bag = bag.fuse(rounded_rail(start, end, PIPING_RADIUS))

    top_points = [
        cq.Vector(-TOP_PIPING_HALF_WIDTH, -TOP_PIPING_HALF_DEPTH, TOP_PIPING_Z),
        cq.Vector(TOP_PIPING_HALF_WIDTH, -TOP_PIPING_HALF_DEPTH, TOP_PIPING_Z),
        cq.Vector(TOP_PIPING_HALF_WIDTH, TOP_PIPING_HALF_DEPTH, TOP_PIPING_Z),
        cq.Vector(-TOP_PIPING_HALF_WIDTH, TOP_PIPING_HALF_DEPTH, TOP_PIPING_Z),
    ]
    for start, end in zip(top_points, top_points[1:] + top_points[:1], strict=True):
        bag = bag.fuse(rounded_rail(start, end, TOP_PIPING_RADIUS))

    side_points = [
        cq.Vector(SIDE_PIPING_X, SIDE_PANEL_FRONT_Y, SIDE_PANEL_BOTTOM_Z),
        cq.Vector(SIDE_PIPING_X, SIDE_PANEL_REAR_Y, SIDE_PANEL_BOTTOM_Z),
        cq.Vector(SIDE_PIPING_X, SIDE_PANEL_REAR_Y, SIDE_PANEL_TOP_Z),
        cq.Vector(SIDE_PIPING_X, SIDE_PANEL_FRONT_Y, SIDE_PANEL_TOP_Z),
    ]
    for start, end in zip(side_points, side_points[1:] + side_points[:1], strict=True):
        bag = bag.fuse(rounded_rail(start, end, SIDE_PIPING_RADIUS))
    return bag


def add_rider_side(bag: cq.Solid) -> cq.Solid:
    """Add a padded back, two simplified shoulder loops, and the carry handle."""
    pad = (
        cq.Workplane("XZ")
        .rect(BACK_PAD_WIDTH, BACK_PAD_HEIGHT)
        .extrude(-BACK_PAD_THICKNESS)
        .translate((0.0, BACK_PAD_CENTER_Y, BACK_PAD_CENTER_Z))
        .edges("|Y")
        .fillet(BACK_PAD_EDGE_RADIUS)
        .val()
    )
    bag = bag.fuse(pad)
    for x in (-STRAP_X_OFFSET, STRAP_X_OFFSET):
        bag = bag.fuse(swept_bezier_tube([cq.Vector(x, y, z) for y, z in STRAP_BEZIER_YZ], STRAP_RADIUS))
    return bag.fuse(swept_tube([cq.Vector(x, HANDLE_Y, z) for x, z in HANDLE_PATH_XZ], HANDLE_RADIUS))


def build_model() -> cq.Workplane:
    """Return one printable miniature, centred in X/Y with its base at Z=0."""
    bag = add_panel_piping(build_body())
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
        .translate((WORDMARK_CENTER_X, WORDMARK_START_Y, WORDMARK_CENTER_Z))
        .val()
    )
    bag = bag.fuse(wordmark).fuse(make_logo_front()).fuse(make_logo_side())
    return cq.Workplane("XY").newObject([add_rider_side(bag).clean()])
