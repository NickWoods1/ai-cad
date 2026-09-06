"""Named dimensions for the stylised DoorDash courier-bag miniature, in mm."""

# Main insulated case. The supplied photograph contains no absolute dimensions;
# this is an intentionally hand-sized display miniature.
BODY_WIDTH = 76.0
BODY_DEPTH = 50.0
BODY_HEIGHT = 78.0
BODY_VERTICAL_RADIUS = 4.0
BOTTOM_CHAMFER = 7.0
TOP_CHAMFER = 2.5

# Slightly oversized soft top flap.
TOP_FLAP_WIDTH = 78.0
TOP_FLAP_DEPTH = 52.0
TOP_FLAP_HEIGHT = 3.0
TOP_FLAP_CENTER_Z = 78.0
TOP_FLAP_CORNER_RADIUS = 3.0

# Broad rear-facing branded panel visible in the supplied riding photograph.
FRONT_PANEL_BOTTOM_Z = 22.0
FRONT_PANEL_TOP_Z = 74.0
FRONT_PANEL_BOTTOM_HALF_WIDTH = 35.0
FRONT_PANEL_TOP_HALF_WIDTH = 33.5
FRONT_PANEL_BACK_Y = -24.4
FRONT_PANEL_THICKNESS = 2.2

# Raised seam/piping cords. Their back halves intersect the panels and body.
PIPING_RADIUS = 1.2
FRONT_PIPING_Y = -26.25
TOP_PIPING_RADIUS = 0.9
TOP_PIPING_Z = 79.1
TOP_PIPING_HALF_WIDTH = 37.5
TOP_PIPING_HALF_DEPTH = 24.5
SIDE_PIPING_RADIUS = 1.0
SIDE_PIPING_X = 38.35
SIDE_PANEL_FRONT_Y = -21.5
SIDE_PANEL_REAR_Y = 20.0
SIDE_PANEL_BOTTOM_Z = 22.0
SIDE_PANEL_TOP_Z = 74.0

# Raised front wordmark and logo.
WORDMARK_TEXT = "DOORDASH"
WORDMARK_FONT = "DejaVu Sans"
WORDMARK_FONT_SIZE = 7.0
WORDMARK_THICKNESS = 2.5
WORDMARK_CENTER_X = 6.0
WORDMARK_CENTER_Z = 60.0
WORDMARK_START_Y = -25.8
FRONT_LOGO_WIDTH = 13.0
FRONT_LOGO_CENTER_X = -25.0
FRONT_LOGO_CENTER_Z = 60.0
FRONT_LOGO_START_Y = -25.8
FRONT_LOGO_THICKNESS = 2.5

# Large raised logo on the right side, as seen in the photograph.
SIDE_LOGO_WIDTH = 20.0
SIDE_LOGO_CENTER_Y = -4.0
SIDE_LOGO_CENTER_Z = 55.0
SIDE_LOGO_START_X = 37.6
SIDE_LOGO_THICKNESS = 1.8

# Rider-facing back pad and simplified toy-like tubular shoulder straps.
BACK_PAD_WIDTH = 54.0
BACK_PAD_HEIGHT = 50.0
BACK_PAD_THICKNESS = 1.8
BACK_PAD_CENTER_Z = 43.0
BACK_PAD_CENTER_Y = 25.4
BACK_PAD_EDGE_RADIUS = 2.5
STRAP_X_OFFSET = 20.0
STRAP_RADIUS = 2.2
STRAP_BEZIER_YZ = ((24.5, 68.0), (34.0, 58.0), (34.0, 24.0), (24.5, 13.0))

# Small top carry loop, inferred because the rider-facing top is obscured.
HANDLE_Y = 8.0
HANDLE_RADIUS = 1.6
HANDLE_PATH_XZ = (
    (-11.0, 78.0),
    (-10.0, 84.0),
    (0.0, 87.0),
    (10.0, 84.0),
    (11.0, 78.0),
)

# DoorDash mark reconstructed from the separate user-supplied logo reference.
LOGO_REFERENCE_X_MIN = 25.0
LOGO_REFERENCE_X_MAX = 438.0
LOGO_REFERENCE_Y_MIN = 29.0
LOGO_REFERENCE_Y_MAX = 263.0
LOGO_PROFILE_START = (25.0, 39.0)
LOGO_PROFILE_SEGMENTS = (
    ((25.0, 34.0), (28.0, 29.0), (35.0, 29.0)),
    ((135.0, 29.0), (236.0, 29.0), (337.0, 29.0)),
    ((395.0, 29.0), (438.0, 76.0), (438.0, 146.0)),
    ((438.0, 214.0), (393.0, 263.0), (331.0, 263.0)),
    ((304.0, 263.0), (279.0, 263.0), (253.0, 263.0)),
    ((246.0, 263.0), (241.0, 260.0), (236.0, 255.0)),
    ((216.0, 235.0), (194.0, 213.0), (172.0, 191.0)),
    ((165.0, 184.0), (170.0, 174.0), (179.0, 174.0)),
    ((226.0, 174.0), (274.0, 174.0), (322.0, 174.0)),
    ((338.0, 174.0), (349.0, 162.0), (349.0, 147.0)),
    ((349.0, 132.0), (338.0, 119.0), (322.0, 119.0)),
    ((251.0, 119.0), (180.0, 119.0), (109.0, 119.0)),
    ((102.0, 119.0), (98.0, 116.0), (93.0, 111.0)),
    ((73.0, 91.0), (51.0, 69.0), (29.0, 47.0)),
    ((26.0, 44.0), (25.0, 42.0), LOGO_PROFILE_START),
)

EXPECTED_SOLID_COUNT = 1
# Refined after measuring the intentional raised-detail envelope.
EXPECTED_OVERALL_WIDTH = 78.400000
EXPECTED_OVERALL_DEPTH = 62.121038
EXPECTED_OVERALL_HEIGHT = 88.480604
DIMENSION_TOLERANCE = 0.02
