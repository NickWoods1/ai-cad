"""Named dimensions for the soft geometric Art Deco coffee mug, in millimetres."""

# Primary body and drinking cavity.
BODY_HEIGHT = 95.0
BASE_THICKNESS = 5.0
NOMINAL_WALL_THICKNESS = 3.2
CAVITY_TOP_EXTENSION = 1.0

# Each section is (height Z, half-width, superellipse exponent). An exponent of
# 2 is circular; larger values create the soft-square plan that carries the
# geometric Deco character without applied faceting.
OUTER_SECTIONS = (
    (0.0, 40.5, 2.55),
    (5.0, 41.5, 2.60),
    (15.0, 40.0, 2.55),
    (55.0, 40.0, 2.45),
    (85.0, 43.5, 2.40),
    (95.0, 42.8, 2.50),
)
PROFILE_SAMPLE_COUNT = 64

# The handle is a filleted ribbon whose outer and inner boundaries are periodic
# splines in the X/Z plane. Wide roots overlap the body so the loop grows out of
# the cup rather than meeting it as a rectangular block.
HANDLE_DEPTH = 15.0
HANDLE_EDGE_FILLET = 2.4
HANDLE_OUTER_XZ = (
    (33.0, 83.0),
    (51.0, 84.0),
    (68.0, 76.0),
    (76.0, 61.0),
    (75.0, 43.0),
    (66.0, 26.0),
    (50.0, 16.0),
    (33.0, 19.0),
)
HANDLE_INNER_XZ = (
    (48.0, 72.0),
    (59.0, 72.0),
    (67.0, 64.0),
    (70.0, 52.0),
    (68.0, 39.0),
    (60.0, 28.0),
    (49.0, 25.0),
    (46.0, 36.0),
    (46.0, 62.0),
)

EXPECTED_SOLID_COUNT = 1
EXPECTED_OVERALL_WIDTH = 120.4122
EXPECTED_OVERALL_DEPTH = 87.5175
EXPECTED_OVERALL_HEIGHT = BODY_HEIGHT
EXPECTED_MATERIAL_VOLUME = 128238.126
DIMENSION_TOLERANCE = 0.02
VOLUME_TOLERANCE = 1.0
