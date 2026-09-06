"""Named dimensions and image-derived profile data for the DoorDash logo."""

# Editable physical scale assumptions. The supplied reference contains no scale.
OVERALL_WIDTH = 120.0
EXTRUSION_DEPTH = 8.0

# The red-pixel silhouette in the supplied 470 x 299 reference occupies this
# image-space envelope. Keeping these values explicit preserves its proportions.
REFERENCE_X_MIN = 25.0
REFERENCE_X_MAX = 438.0
REFERENCE_Y_MIN = 29.0
REFERENCE_Y_MAX = 263.0
REFERENCE_PROFILE_WIDTH = REFERENCE_X_MAX - REFERENCE_X_MIN
REFERENCE_PROFILE_HEIGHT = REFERENCE_Y_MAX - REFERENCE_Y_MIN
PROFILE_SCALE = OVERALL_WIDTH / REFERENCE_PROFILE_WIDTH
EXPECTED_OVERALL_HEIGHT = REFERENCE_PROFILE_HEIGHT * PROFILE_SCALE

# Cubic Bezier path in reference-image pixel coordinates. Each segment is
# (control_1, control_2, end); the first point is the starting point.
PROFILE_START = (25.0, 39.0)
PROFILE_SEGMENTS = (
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
    ((26.0, 44.0), (25.0, 42.0), PROFILE_START),
)

EXPECTED_SOLID_COUNT = 1
DIMENSION_TOLERANCE = 0.01

