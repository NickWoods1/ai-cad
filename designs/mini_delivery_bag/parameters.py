"""Named dimensions for a miniature generic bicycle delivery backpack, in mm."""

# Exact design choices for this printable miniature.  They are deliberately
# larger than a toy charm so the raised and recessed details survive FDM.
BODY_WIDTH = 70.0
BODY_DEPTH = 39.5
BODY_HEIGHT = 80.0
VERTICAL_CORNER_RADIUS = 4.0
# Cosmetic add-ons overlap the body by this amount to make reliable boolean
# unions rather than merely face-to-face contact.
FUSION_OVERLAP = 0.4

# The front flap sits in front of the main body; together they make the
# requested 42 mm finished depth.
FRONT_FLAP_WIDTH = 62.0
FRONT_FLAP_THICKNESS = 2.5
FRONT_FLAP_HEIGHT = 54.0
FRONT_FLAP_CENTER_Z = 43.0

# Raised front branding is deliberate geometry, so it is visible on the STL
# and can be colour-swapped during printing.
WORDMARK_TEXT = "DOORDASH"
WORDMARK_FONT = "DejaVu Sans"
WORDMARK_FONT_SIZE = 7.5
WORDMARK_THICKNESS = 0.9
WORDMARK_CENTER_Z = 42.0
WORDMARK_FUSION_OVERLAP = FUSION_OVERLAP

# Rear straps are fused to the body so that the model remains one solid.
STRAP_WIDTH = 6.0
STRAP_THICKNESS = 1.5
STRAP_HEIGHT = 58.0
STRAP_CENTER_Z = 43.0
STRAP_X_OFFSET = 19.0
STRAP_CROSSBAR_HEIGHT = 4.0
STRAP_CROSSBAR_CENTER_Z = 42.0

# A raised top carry handle gives the miniature a recognisable silhouette.
HANDLE_WIDTH = 30.0
HANDLE_DEPTH = 10.0
HANDLE_HEIGHT = 8.0

EXPECTED_SOLID_COUNT = 1
# The wordmark extends 0.5 mm beyond the front flap. It is the foremost feature.
EXPECTED_OVERALL_DEPTH = BODY_DEPTH + FRONT_FLAP_THICKNESS + STRAP_THICKNESS - (2.0 * FUSION_OVERLAP) + (WORDMARK_THICKNESS - WORDMARK_FUSION_OVERLAP)
EXPECTED_OVERALL_HEIGHT = BODY_HEIGHT + HANDLE_HEIGHT - FUSION_OVERLAP
DIMENSION_TOLERANCE = 0.01
