"""CadQuery model for a soft geometric American Art Deco coffee mug."""

from __future__ import annotations

import math

import cadquery as cq

from parameters import (
    BASE_THICKNESS,
    BODY_HEIGHT,
    CAVITY_TOP_EXTENSION,
    HANDLE_DEPTH,
    HANDLE_EDGE_FILLET,
    HANDLE_INNER_XZ,
    HANDLE_OUTER_XZ,
    NOMINAL_WALL_THICKNESS,
    OUTER_SECTIONS,
    PROFILE_SAMPLE_COUNT,
)


def closed_periodic_spline(points: list[cq.Vector]) -> cq.Wire:
    """Create a smooth closed wire through the supplied control samples."""
    edge = cq.Edge.makeSpline(points, periodic=True)
    return cq.Wire.assembleEdges([edge])


def soft_square_wire(z: float, half_width: float, exponent: float) -> cq.Wire:
    """Create a symmetric superellipse section in the XY plane."""
    points = []
    power = 2.0 / exponent
    for index in range(PROFILE_SAMPLE_COUNT):
        angle = 2.0 * math.pi * index / PROFILE_SAMPLE_COUNT
        cosine = math.cos(angle)
        sine = math.sin(angle)
        x = half_width * math.copysign(abs(cosine) ** power, cosine)
        y = half_width * math.copysign(abs(sine) ** power, sine)
        points.append(cq.Vector(x, y, z))
    return closed_periodic_spline(points)


def interpolate_section(z: float) -> tuple[float, float]:
    """Interpolate half-width and exponent for a section at height z."""
    for lower, upper in zip(OUTER_SECTIONS, OUTER_SECTIONS[1:], strict=True):
        if lower[0] <= z <= upper[0]:
            fraction = (z - lower[0]) / (upper[0] - lower[0])
            half_width = lower[1] + fraction * (upper[1] - lower[1])
            exponent = lower[2] + fraction * (upper[2] - lower[2])
            return half_width, exponent
    raise ValueError(f"Section height {z} lies outside the body")


def build_cup_body() -> cq.Solid:
    """Loft the integrated pedestal, body, shoulder, and lip, then hollow it."""
    outer_wires = [soft_square_wire(*section) for section in OUTER_SECTIONS]
    outer = cq.Solid.makeLoft(outer_wires)

    cavity_sections = []
    base_half_width, base_exponent = interpolate_section(BASE_THICKNESS)
    cavity_sections.append((BASE_THICKNESS, base_half_width - NOMINAL_WALL_THICKNESS, base_exponent))
    cavity_sections.extend(
        (z, half_width - NOMINAL_WALL_THICKNESS, exponent)
        for z, half_width, exponent in OUTER_SECTIONS
        if BASE_THICKNESS < z < BODY_HEIGHT
    )
    top_half_width, top_exponent = interpolate_section(BODY_HEIGHT)
    cavity_sections.append(
        (
            BODY_HEIGHT + CAVITY_TOP_EXTENSION,
            top_half_width - NOMINAL_WALL_THICKNESS,
            top_exponent,
        )
    )
    cavity = cq.Solid.makeLoft([soft_square_wire(*section) for section in cavity_sections])
    return outer.cut(cavity)


def xz_spline_wire(points: tuple[tuple[float, float], ...], y: float) -> cq.Wire:
    """Create a periodic handle boundary in a plane normal to Y."""
    return closed_periodic_spline([cq.Vector(x, y, z) for x, z in points])


def build_handle() -> cq.Solid:
    """Build the rounded, tapered-looking ribbon around a teardrop opening."""
    front_y = -HANDLE_DEPTH / 2.0
    outer = xz_spline_wire(HANDLE_OUTER_XZ, front_y)
    inner = xz_spline_wire(HANDLE_INNER_XZ, front_y)
    ribbon = cq.Solid.extrudeLinear(outer, [inner], cq.Vector(0.0, HANDLE_DEPTH, 0.0))
    perimeter_edges = [edge for edge in ribbon.Edges() if edge.geomType() == "BSPLINE"]
    return ribbon.fillet(HANDLE_EDGE_FILLET, perimeter_edges)


def build_model() -> cq.Workplane:
    """Return the printable one-piece mug, centred in X/Y with its base at Z=0."""
    mug = build_cup_body().fuse(build_handle()).clean()
    return cq.Workplane("XY").newObject([mug])
