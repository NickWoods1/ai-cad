"""Extruded DoorDash logo silhouette reconstructed from the supplied image."""

from __future__ import annotations

import cadquery as cq

from parameters import (
    EXTRUSION_DEPTH,
    OVERALL_WIDTH,
    PROFILE_SCALE,
    PROFILE_SEGMENTS,
    PROFILE_START,
    REFERENCE_X_MAX,
    REFERENCE_X_MIN,
    REFERENCE_Y_MAX,
    REFERENCE_Y_MIN,
)


def _profile_point(point: tuple[float, float]) -> tuple[float, float]:
    """Convert reference pixels to centred millimetres with image Y inverted."""
    centre_x = (REFERENCE_X_MIN + REFERENCE_X_MAX) / 2.0
    centre_y = (REFERENCE_Y_MIN + REFERENCE_Y_MAX) / 2.0
    return ((point[0] - centre_x) * PROFILE_SCALE, (centre_y - point[1]) * PROFILE_SCALE)


def build_model() -> cq.Workplane:
    """Return one uniformly extruded logo solid, centred in X/Y on Z=0."""
    path = cq.Workplane("XY").moveTo(*_profile_point(PROFILE_START))
    for control_1, control_2, end in PROFILE_SEGMENTS:
        path = path.bezier(
            [_profile_point(control_1), _profile_point(control_2), _profile_point(end)],
            includeCurrent=True,
        )

    logo = path.close().extrude(EXTRUSION_DEPTH)

    # Guard the concept-level scale here as well as in the build validator.
    if abs(logo.val().BoundingBox().xlen - OVERALL_WIDTH) > 0.01:
        raise ValueError("Logo profile does not preserve the requested overall width")
    return logo

