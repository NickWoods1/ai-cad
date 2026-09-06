"""CadQuery reconstruction of the photographed Shure MV6 and desktop stand."""

from __future__ import annotations

import math

import cadquery as cq

from parameters import *


def rounded_box(length: float, width: float, height: float, radius: float, center: tuple[float, float, float]) -> cq.Solid:
    """Make a rounded rectangular solid with all edges softened."""
    return (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges()
        .fillet(radius)
        .translate(center)
        .val()
    )


def rounded_prism_x(length: float, width: float, height: float, radius: float, center: tuple[float, float, float]) -> cq.Solid:
    """Extrude a rounded YZ section along X, leaving clean planar end faces."""
    x0 = center[0] - length / 2.0
    result = (
        cq.Workplane("XY")
        .box(length, width - 2.0 * radius, height)
        .translate(center)
        .val()
    )
    result = result.fuse(
        cq.Workplane("XY").box(length, width, height - 2.0 * radius).translate(center).val()
    )
    for y in (center[1] - width / 2.0 + radius, center[1] + width / 2.0 - radius):
        for z in (center[2] - height / 2.0 + radius, center[2] + height / 2.0 - radius):
            result = result.fuse(
                cq.Solid.makeCylinder(radius, length, cq.Vector(x0, y, z), cq.Vector(1.0, 0.0, 0.0))
            )
    return result.clean()


def rounded_plate_xy(length: float, width: float, height: float, radius: float, center: tuple[float, float, float]) -> cq.Solid:
    """Extrude a thin rounded XY outline without over-filletting its thickness."""
    z0 = center[2] - height / 2.0
    result = cq.Workplane("XY").box(length - 2.0 * radius, width, height).translate(center).val()
    result = result.fuse(cq.Workplane("XY").box(length, width - 2.0 * radius, height).translate(center).val())
    for x in (center[0] - length / 2.0 + radius, center[0] + length / 2.0 - radius):
        for y in (center[1] - width / 2.0 + radius, center[1] + width / 2.0 - radius):
            result = result.fuse(
                cq.Solid.makeCylinder(radius, height, cq.Vector(x, y, z0), cq.Vector(0.0, 0.0, 1.0))
            )
    return result.clean()


def superellipse_wire_x(x: float, half_y: float, half_z: float, exponent: float, samples: int = 96) -> cq.Wire:
    """Return a smooth closed superellipse in a plane normal to X."""
    points: list[cq.Vector] = []
    power = 2.0 / exponent
    for index in range(samples):
        angle = 2.0 * math.pi * index / samples
        cosine = math.cos(angle)
        sine = math.sin(angle)
        y = half_y * math.copysign(abs(cosine) ** power, cosine)
        z = MIC_AXIS_Z + half_z * math.copysign(abs(sine) ** power, sine)
        points.append(cq.Vector(x, y, z))
    # Dense, exact samples avoid the dimensional overshoot of an interpolating
    # periodic spline while remaining visually smooth after tessellation.
    return cq.Wire.makePolygon(points, close=True)


def lofted_superellipse(sections: tuple[tuple[float, float, float], ...], exponent: float) -> cq.Solid:
    """Loft a controlled family of rounded-square/circular transverse sections."""
    wires = [superellipse_wire_x(x, half_y, half_z, exponent) for x, half_y, half_z in sections]
    return cq.Solid.makeLoft(wires, ruled=True)


def build_base_and_post() -> cq.Solid:
    """Build the photographed low-profile weighted base and slim upright."""
    base = (
        cq.Workplane("XY")
        .circle(BASE_DIAMETER / 2.0)
        .extrude(BASE_HEIGHT)
        .edges()
        .fillet(BASE_EDGE_RADIUS)
        .translate((STAND_AXIS_X, 0.0, 0.0))
        .val()
    )
    post = cq.Solid.makeCylinder(
        POST_DIAMETER / 2.0,
        POST_TOP_Z - POST_BOTTOM_Z,
        cq.Vector(STAND_AXIS_X, 0.0, POST_BOTTOM_Z),
        cq.Vector(0.0, 0.0, 1.0),
    )
    post_collar = cq.Solid.makeCylinder(
        POST_COLLAR_DIAMETER / 2.0,
        POST_COLLAR_HEIGHT,
        cq.Vector(STAND_AXIS_X, 0.0, POST_COLLAR_BOTTOM_Z),
        cq.Vector(0.0, 0.0, 1.0),
    )
    return base.fuse(post).fuse(post_collar)


def build_mount() -> cq.Solid:
    """Build the fork, transverse pivot hardware, and the microphone saddle."""
    mount = rounded_box(
        FORK_ARM_LENGTH_X,
        FORK_OUTER_WIDTH_Y,
        FORK_TOP_Z - FORK_BOTTOM_Z,
        FORK_CORNER_RADIUS,
        (FORK_CENTER_X, 0.0, (FORK_BOTTOM_Z + FORK_TOP_Z) / 2.0),
    )
    slot = rounded_box(
        FORK_ARM_LENGTH_X + 2.0,
        FORK_OUTER_WIDTH_Y - 2.0 * FORK_ARM_THICKNESS,
        FORK_TOP_Z - FORK_BOTTOM_Z + 2.0,
        3.0,
        (FORK_CENTER_X, 0.0, (FORK_BOTTOM_Z + FORK_TOP_Z) / 2.0 + 5.0),
    )
    # Keep a lower bridge so the two arms remain joined to the post.
    slot = slot.intersect(
        cq.Workplane("XY")
        .box(FORK_ARM_LENGTH_X + 4.0, FORK_OUTER_WIDTH_Y, FORK_TOP_Z - FORK_BOTTOM_Z)
        .translate((FORK_CENTER_X, 0.0, (FORK_BOTTOM_Z + FORK_TOP_Z) / 2.0 + 8.0))
        .val()
    )
    mount = mount.cut(slot)
    axle = cq.Solid.makeCylinder(
        PIVOT_AXLE_RADIUS,
        FORK_OUTER_WIDTH_Y + 2.0 * PIVOT_HEAD_DEPTH,
        cq.Vector(PIVOT_X, -FORK_OUTER_WIDTH_Y / 2.0 - PIVOT_HEAD_DEPTH, PIVOT_Z),
        cq.Vector(0.0, 1.0, 0.0),
    )
    for y, direction in ((-FORK_OUTER_WIDTH_Y / 2.0 - PIVOT_HEAD_DEPTH, 1.0), (FORK_OUTER_WIDTH_Y / 2.0 + PIVOT_HEAD_DEPTH, -1.0)):
        axle = axle.fuse(
            cq.Solid.makeCylinder(
                PIVOT_HEAD_RADIUS,
                PIVOT_HEAD_DEPTH,
                cq.Vector(PIVOT_X, y, PIVOT_Z),
                cq.Vector(0.0, direction, 0.0),
            )
        )
    saddle_height = SADDLE_TOP_Z - SADDLE_BOTTOM_Z
    saddle = rounded_box(
        SADDLE_WIDTH_X,
        SADDLE_WIDTH_Y,
        saddle_height,
        3.5,
        (PIVOT_X, 0.0, SADDLE_BOTTOM_Z + saddle_height / 2.0),
    )
    return mount.fuse(axle).fuse(saddle)


def build_microphone_body() -> cq.Solid:
    """Build the metal shell, collar, windscreen, controls, vents, and rear face."""
    shell_center_x = SHELL_FRONT_X + SHELL_LENGTH / 2.0
    shell = lofted_superellipse(SHELL_SECTIONS, SHELL_SECTION_EXPONENT)

    # Side vents are shallow spherical dimples, as the photos show recesses rather than bores.
    for x in VENT_X_POSITIONS:
        for z_offset in VENT_Z_OFFSETS:
            for side in (-1.0, 1.0):
                cutter_center_y = side * (SHELL_WIDTH / 2.0 + VENT_RADIUS - VENT_CUT_DEPTH)
                shell = shell.cut(cq.Solid.makeSphere(VENT_RADIUS, cq.Vector(x, cutter_center_y, MIC_AXIS_Z + z_offset)))

    collar_center_x = WINDSCREEN_REAR_X + COLLAR_LENGTH / 2.0
    collar = rounded_prism_x(
        COLLAR_LENGTH,
        COLLAR_WIDTH,
        COLLAR_HEIGHT,
        COLLAR_CORNER_RADIUS,
        (collar_center_x, 0.0, MIC_AXIS_Z),
    )
    windscreen = lofted_superellipse(WINDSCREEN_SECTIONS, WINDSCREEN_SECTION_EXPONENT)

    top_z = MIC_AXIS_Z + SHELL_HEIGHT / 2.0 - 0.25
    seam = (
        cq.Workplane("XY")
        .box(TOP_SEAM_LENGTH, TOP_SEAM_WIDTH, TOP_SEAM_HEIGHT)
        .translate((TOP_SEAM_X_START + TOP_SEAM_LENGTH / 2.0, 0.0, top_z))
        .val()
    )
    button = rounded_plate_xy(
        MUTE_BUTTON_LENGTH,
        MUTE_BUTTON_WIDTH,
        MUTE_BUTTON_HEIGHT,
        MUTE_BUTTON_RADIUS,
        (MUTE_BUTTON_CENTER_X, 0.0, top_z + MUTE_BUTTON_HEIGHT / 2.0),
    )

    # Approximate the visible SHURE marks on both broad sides with shallow relief.
    marks: list[cq.Solid] = []
    for side in (-1.0, 1.0):
        start_y = side * (SHELL_WIDTH / 2.0 - WORDMARK_EMBED)
        relief = -side * (WORDMARK_EMBED + WORDMARK_RELIEF)
        mark = (
            cq.Workplane("XZ")
            .text(
                WORDMARK_TEXT,
                WORDMARK_SIZE,
                relief,
                font=WORDMARK_FONT,
                kind="bold",
                halign="center",
                valign="center",
            )
            .translate((WORDMARK_CENTER_X, start_y, WORDMARK_CENTER_Z))
            .val()
        )
        marks.append(mark)

    # Rear USB-C and headphone openings are shallow, printable recesses.
    usb = rounded_prism_x(
        REAR_FACE_INSET + 1.0,
        USB_PORT_WIDTH,
        USB_PORT_HEIGHT,
        1.2,
        (MIC_REAR_X - REAR_FACE_INSET / 2.0, USB_PORT_CENTER_Y, USB_PORT_CENTER_Z),
    )
    headphone = cq.Solid.makeCylinder(
        HEADPHONE_PORT_DIAMETER / 2.0,
        REAR_FACE_INSET + 1.0,
        cq.Vector(MIC_REAR_X + 0.3, HEADPHONE_PORT_CENTER_Y, HEADPHONE_PORT_CENTER_Z),
        cq.Vector(-1.0, 0.0, 0.0),
    )
    microphone = shell.fuse(collar).fuse(windscreen).fuse(seam).fuse(button)
    for mark in marks:
        microphone = microphone.fuse(mark)
    return microphone.cut(usb).cut(headphone)


def build_model() -> cq.Workplane:
    """Return one full-scale visual replica, centred on the base with Z=0."""
    model = build_base_and_post().fuse(build_mount()).fuse(build_microphone_body()).clean()
    return cq.Workplane("XY").newObject([model])
