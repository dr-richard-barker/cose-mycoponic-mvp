"""
CoSE Mycoponic Chamber — Minimal Viable Prototype (MVP) Master Parameters
Single source of truth for all dimensions, clearances, and port specs.
All dimensions in millimeters (mm) unless noted.
"""

import math

INCH = 25.4

# ==============================================================================
# 1. Off-the-Shelf Clear Tube (Uxcell Clear Rigid Acrylic / Polycarbonate Pipe)
# ==============================================================================
TUBE_ID = 85.0                     # 3.35 in nominal
TUBE_OD = 90.0                     # 3.54 in nominal
TUBE_WALL = (TUBE_OD - TUBE_ID) / 2.0  # 2.5 mm
TUBE_LENGTH = 100.0                # 100 mm (~4" Uxcell metric pipe)

# ==============================================================================
# 2. Off-the-Shelf 4-Inch Ceramic Water Filter Candle (AquaEasy / Standard)
# ==============================================================================
CANDLE_OD = 50.0                   # ~2.0 in nominal ceramic body diameter
CANDLE_BODY_LEN = 4.0 * INCH       # 101.6 mm porous body length
CANDLE_STEM_DIA = 12.5             # ~1/4" BSP / M12 threaded mount stem OD
CANDLE_STEM_BORE_CLEARANCE = 13.2  # Through-hole in drop-in collar for stem
CANDLE_WASHER_OD = 26.0            # Clearance diameter for sealing washer & wing nut

# Top-loading drop-in candle slot (candle + collar drop in from top of lid)
CANDLE_DROP_BORE_DIA = 51.5        # Through-bore in lid so 50 mm candle drops through
CANDLE_COLLAR_OD = 58.0            # Outer flange of printable retention collar
CANDLE_COLLAR_THICKNESS = 4.0      # Collar flange thickness (sits flush in lid pocket)
CANDLE_POCKET_DIA = 58.5           # Stepped counterbore in lid top (0.25 mm radial clearance)
CANDLE_POCKET_DEPTH = 4.0          # Depth of stepped shoulder so collar cannot fall through

# ==============================================================================
# 3. 3D Printing (FDM) Tolerances & Wall Thicknesses
# ==============================================================================
SLIDE_CLEARANCE_RADIAL = 0.25      # 0.50 mm diametral clearance for hand slide-fit
WALL_THICKNESS = 3.75              # Sturdy, watertight PETG skirt/socket wall
ROOF_THICKNESS = 7.5               # Lid roof thickness (houses Female Luer taper)
SKIRT_ENGAGEMENT = 12.0            # Overlap of lid skirt and base socket onto tube

# ==============================================================================
# 4. Z-Stack Datum (Z = 0.0 at bottom of 3D-printed base on build plate)
# ==============================================================================
BASE_FOOT_HEIGHT = 4.0             # Solid base rim/foot thickness
FUNNEL_APEX_Z = 17.75              # Lowest point of conical sump (~18 mm off table)
FUNNEL_SLOPE_DEG = 38.5            # Steep enough for clean drainage & support-free print
# Rise from drain bore radius (2.25 mm) to tube ID radius (42.5 mm):
# 40.25 mm * tan(38.5 deg) = 32.0 mm -> Z_TUBE_SEAT = 50.0 mm
Z_TUBE_SEAT = 50.0
Z_BASE_TOP = Z_TUBE_SEAT + SKIRT_ENGAGEMENT  # 62.0 mm

Z_TUBE_TOP = Z_TUBE_SEAT + TUBE_LENGTH       # 151.6 mm (for 4" tube)
Z_LID_TOP = Z_TUBE_TOP + ROOF_THICKNESS      # 159.1 mm
Z_LID_SKIRT_BOTTOM = Z_TUBE_TOP - SKIRT_ENGAGEMENT  # 139.6 mm

# ==============================================================================
# 5. Bottom Base & Side-Exit Drain Valve Port
# ==============================================================================
BASE_BODY_OD = TUBE_OD + 2.0 * SLIDE_CLEARANCE_RADIAL + 2.0 * WALL_THICKNESS  # 98.0 mm
BASE_FLANGE_OD = 114.0             # Wide foot flange for benchtop stability
BASE_SOCKET_ID = TUBE_OD + 2.0 * SLIDE_CLEARANCE_RADIAL  # 90.5 mm

DRAIN_BORE_DIA = 4.5               # Internal drain channel diameter
DRAIN_CENTER_Z = FUNNEL_APEX_Z + DRAIN_BORE_DIA / 2.0  # 10.25 mm
DRAIN_BARB_LEN = 16.0              # Protrusion from base body OD for 1/4" ID tubing
DRAIN_BARB_SHAFT_OD = 6.5          # Fits standard 1/4" (6.35 mm) ID silicone tubing
DRAIN_BARB_RIB_OD = 7.4            # Retention barb ridge OD

# Base Electronics / Sensor Bays (3x smooth arched cutouts hugging the funnel)
BAY_ARCH_ANGLES_DEG = (75.0, 180.0, 285.0)  # Leaves +/- 37 deg solid around 0 deg drain
BAY_ARCH_RADIUS = 30.0             # 60 mm wide x 30 mm tall smooth arch (Z = 4 to 34 mm)
BAY_PEDESTAL_R = 14.0              # Central pedestal radius (Z = 4.0 to 14.0 mm)
BAY_FLOOR_Z = BASE_FOOT_HEIGHT     # 4.0 mm flat floor shelf
BAY_PEDESTAL_TOP_Z = 14.0          # Start of ~43 deg conical flare hugging funnel
BAY_CEILING_TOP_Z = 47.0           # Meets body OD 3 mm below Z_TUBE_SEAT (50.0 mm)
ARDUINO_M3_HOLE_DIA = 2.8          # Self-tapping M3 mounting holes in bay floor
ARDUINO_HOLE_RADII = (28.0, 44.0)  # Radial positions of M3 hole pairs
ARDUINO_HOLE_Y_OFFSET = 12.7       # +/- 12.7 mm (25.4 mm / 1.0 in spacing)

# ==============================================================================
# 8. Collection Base Variant (10 mL Syringe Snap-In C-Clip Cradle)
# ==============================================================================
COLL_SYRINGE_BARREL_ID = 16.4      # Snap-fit for standard 10 mL syringe (~16.0 mm OD)
COLL_CLIP_WALL = 3.0               # C-clip wall thickness
COLL_CLIP_WIDTH = 10.0             # Width of each C-clip along syringe axis
COLL_CLIP_SPACING = 32.0           # Center-to-center spacing of the 2 clips
COLL_CRADLE_ANGLE_DEG = 75.0       # Centered along the 75 deg arched bay
COLL_CRADLE_R = 47.5               # 6.5 mm (~2/3 cm) inward, flush with 114 mm foot rim
COLL_CRADLE_Z = 14.0               # Syringe centerline height off table

# ==============================================================================
# 9. Compact Center Syringe-Cage Lid Variant (Holds 50 mL Syringe Shaft)
# ==============================================================================
CAGE_ID = 32.0                     # Holds 50 mL syringe barrel (~30 mm OD) centered
CAGE_WALL = 3.0                    # 38.0 mm OD cage wall
CAGE_HEIGHT = 45.0                 # ~45 mm tall compact central cage
CAGE_RING_HEIGHT = 5.0             # Bottom & top ring height
CAGE_NUM_RIBS = 4                  # 4 vertical pillars (90 deg apart) for wide finger access
CAGE_RIB_WIDTH = 6.5               # 6.5 mm wide pillars -> ~18 mm wide windows to tighten wing nut

# Glue-on syringe cage add-on (mates onto Ø58 mm mvp_candle_collar)
CAGE_ADDON_BASE_OD = CANDLE_COLLAR_OD  # 58.0 mm
CAGE_ADDON_BASE_ID = 28.0          # Clears Ø26 mm candle washer & wing nut
CAGE_25ML_ID = 23.5                # Fits standard 25 mL syringe barrel (~22 mm OD)

# ==============================================================================
# 6. Top Lid & Annular Ports (Placed at R = 33.5 mm, 120 deg apart)
# ==============================================================================
LID_OD = BASE_BODY_OD              # 98.0 mm
LID_SKIRT_ID = TUBE_OD + 2.0 * SLIDE_CLEARANCE_RADIAL    # 90.5 mm
PORT_RING_RADIUS = 35.5            # Clears Ø58.5 mm candle pocket & Ø85 mm tube bore

# Port 1 (0 deg): Gas Exchange (Standard Male Luer Slip Syringe Filter socket)
# ISO 80369-7 Luer 6% taper: ~4.30 mm at entry tapering down to ~3.85 mm over 7.5 mm
LUER_TOP_DIA = 4.35
LUER_BOT_DIA = 3.90
LUER_THRU_DIA = 3.0

# Port 2 (120 deg): Humid Air Inlet (Snug push-fit for 6 mm OD / 4 mm ID air tubing)
AIR_PORT_BORE_DIA = 6.0            # Direct push-fit for 6 mm OD tubing or printable barb

# Port 3 (240 deg): Temp/Humidity Sensor Pass-Through
SENSOR_PORT_BORE_DIA = 8.0         # Pass-through for wired SHT30/DHT22/probe cable

# ==============================================================================
# 7. Syringe Tower Lid Variant (Supports 50 mL Medical Syringe on Top)
# ==============================================================================
SYRINGE_TOWER_HEIGHT = 165.0       # 6.50 in (within 5.5 - 6.8 in spec)
SYRINGE_TOWER_HALF_HEIGHT = 82.5   # 3.25 in (half-height syringe adapter)
SYRINGE_PILLAR_DIA = 14.0          # 1.4 cm diameter strong frame pillars (3x at 60/180/300 deg)
SYRINGE_PILLAR_RING_R = 41.0       # Sits cleanly inside 49 mm lid rim & 33 mm ring ID (no tangent seam)
SYRINGE_TOP_RING_THICKNESS = 10.0  # Top cradle ring thickness
SYRINGE_TOP_RING_ID = 66.0         # Open upper ring ID (overlaps pillars cleanly)
SYRINGE_BARREL_CRADLE_ID = 32.0    # Fits standard 50 mL syringe barrel (~29.5-30.5 mm OD)
SYRINGE_BARREL_CRADLE_OD = 44.0    # Catches syringe finger flanges (~45-48 mm)
SYRINGE_SPOKE_WIDTH = 12.0         # Radial spokes connecting top ring to central cradle
