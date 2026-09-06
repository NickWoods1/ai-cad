"""Named dimensions for the aero-tech coffee mug, in millimetres."""

# Cup envelope and drinking cavity.  The dimensions produce about 425 ml of
# nominal internal volume before allowing for the curved rim and practical fill
# height; do not treat that as a calibrated capacity.
BODY_HEIGHT = 95.0
BASE_OUTER_RADIUS = 39.0
TOP_OUTER_RADIUS = 44.0
WALL_THICKNESS = 3.2
BASE_THICKNESS = 5.0

# Faceted lower armour cuff: a geometric style feature, fused into the cup.
CUFF_SIDES = 8
CUFF_OUTER_DIAMETER = 94.0
CUFF_INNER_DIAMETER = 76.0
CUFF_HEIGHT = 26.0

# Raised front grip fins on the cuff.
FIN_COUNT = 3
FIN_WIDTH = 5.0
# Deliberately deep enough to overlap the angled faces of the octagonal cuff.
FIN_DEPTH = 7.0
FIN_HEIGHT = 20.0
FIN_CENTER_Z = 14.0
FIN_X_SPACING = 18.0
FIN_ANGLE = -25.0

# Angular wraparound handle, fused into the cup at the right side.
HANDLE_OUTER_WIDTH = 34.0
HANDLE_OUTER_DEPTH = 16.0
HANDLE_OUTER_HEIGHT = 60.0
HANDLE_INNER_WIDTH = 20.0
HANDLE_INNER_HEIGHT = 38.0
HANDLE_CORNER_RADIUS = 5.0
HANDLE_FUSION_OVERLAP = 0.8
HANDLE_CENTER_X = TOP_OUTER_RADIUS + HANDLE_OUTER_WIDTH / 2.0 - HANDLE_FUSION_OVERLAP
HANDLE_CENTER_Z = BODY_HEIGHT / 2.0

EXPECTED_SOLID_COUNT = 1
EXPECTED_OVERALL_WIDTH = CUFF_OUTER_DIAMETER / 2.0 + HANDLE_CENTER_X + HANDLE_OUTER_WIDTH / 2.0
EXPECTED_OVERALL_DEPTH = CUFF_OUTER_DIAMETER
EXPECTED_OVERALL_HEIGHT = BODY_HEIGHT
DIMENSION_TOLERANCE = 0.01
