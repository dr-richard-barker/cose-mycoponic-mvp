"""
CoSE Mycoponic Chamber — Minimal Viable Prototype (MVP) CAD Parts
Parametric build123d solid builders for:
  - mvp_top_lid: Slide-on lid with candle mount, syringe filter Luer socket,
    humid air inlet port, and temp/humidity sensor pass-through.
  - mvp_bottom_base: Stability foot, 90 mm OD tube socket, 38.5 deg conical
    nutrient funnel, and side-exit 1/4" drain barb for an inline valve.
  - mvp_port_barb_insert: Optional printable 6 mm -> 4 mm hose barb plug
    that presses into the air inlet port if using flexible 4 mm ID tubing.
  - mvp_tube_ref & mvp_candle_ref: Reference solids for assembly verification.
"""

import math

from build123d import (
    Align,
    Box,
    Circle,
    Cone,
    Cylinder,
    Helix,
    Locations,
    Plane,
    Polygon,
    Pos,
    Rot,
    Spline,
    chamfer,
    extrude,
    sweep,
)

import mvp_params as p


def _tube(r_in: float, r_out: float, height: float, z0: float):
    """Hollow vertical cylinder from z0 to z0 + height."""
    outer = Pos(0, 0, z0) * Cylinder(r_out, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    if r_in <= 0.0:
        return outer
    inner = Pos(0, 0, z0) * Cylinder(r_in, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return outer - inner


def _frustum(r_bot: float, r_top: float, height: float, z0: float):
    """Vertical cone frustum from z0 to z0 + height."""
    return Pos(0, 0, z0) * Cone(r_bot, r_top, height, align=(Align.CENTER, Align.CENTER, Align.MIN))


def mvp_top_lid():
    """Slide-on 3D-printed top lid (print upside-down, Z_LID_TOP on build plate).

    Features:
      - 90.5 mm ID x 12 mm deep slide-on skirt with 1.2 mm entry chamfer
      - Central 13.2 mm bore for 4-inch ceramic candle threaded stem + washer
      - 0 deg: Female Luer Slip tapered socket for standard syringe filter
      - 120 deg: 6.0 mm bore for humid air pump tubing / barb insert
      - 240 deg: 8.0 mm bore for hanging temp/humidity sensor cable
    """
    r_outer = p.LID_OD / 2.0
    r_skirt_in = p.LID_SKIRT_ID / 2.0

    # Roof disc + outer slide-on skirt
    roof = Pos(0, 0, p.Z_TUBE_TOP) * Cylinder(
        r_outer, p.ROOF_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    skirt = _tube(r_skirt_in, r_outer, p.SKIRT_ENGAGEMENT, p.Z_LID_SKIRT_BOTTOM)
    lid = roof + skirt

    # Lead-in chamfer at bottom inner lip of skirt for easy slide-on
    chamfer_cone = _frustum(r_skirt_in + 1.2, r_skirt_in, 1.5, p.Z_LID_SKIRT_BOTTOM)
    lid = lid - chamfer_cone

    # Central top-loading drop-in candle slot:
    # 51.5 mm through-bore lets the 50 mm candle drop in from the top;
    # 58.5 mm x 4.0 mm stepped pocket catches mvp_candle_collar so it cannot fall.
    candle_drop_bore = Pos(0, 0, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.CANDLE_DROP_BORE_DIA / 2.0,
        p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    candle_pocket = Pos(0, 0, p.Z_LID_TOP - p.CANDLE_POCKET_DEPTH) * Cylinder(
        p.CANDLE_POCKET_DIA / 2.0,
        p.CANDLE_POCKET_DEPTH + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    lid = lid - candle_drop_bore - candle_pocket

    # Port 1 (0 deg): Female Luer Slip tapered socket (wider at Z_LID_TOP)
    px1, py1 = p.PORT_RING_RADIUS, 0.0
    luer_socket = Pos(px1, py1, p.Z_TUBE_TOP) * Cone(
        p.LUER_BOT_DIA / 2.0,
        p.LUER_TOP_DIA / 2.0,
        p.ROOF_THICKNESS + 0.5,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    luer_thru = Pos(px1, py1, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.LUER_THRU_DIA / 2.0,
        p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    lid = lid - luer_socket - luer_thru

    # Port 2 (240 deg): Humid air inlet bore (6.0 mm snug push-fit, opposite 75 deg syringe)
    px2 = p.PORT_RING_RADIUS * math.cos(math.radians(240.0))
    py2 = p.PORT_RING_RADIUS * math.sin(math.radians(240.0))
    air_bore = Pos(px2, py2, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.AIR_PORT_BORE_DIA / 2.0,
        p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    lid = lid - air_bore

    # Port 3 (120 deg): Temp/Humidity sensor pass-through bore (10.0 mm, near 180 deg ESP32 bay)
    px3 = p.PORT_RING_RADIUS * math.cos(math.radians(120.0))
    py3 = p.PORT_RING_RADIUS * math.sin(math.radians(120.0))
    sensor_bore = Pos(px3, py3, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.SENSOR_PORT_BORE_DIA / 2.0,
        p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    lid = lid - sensor_bore

    # 3x blind sockets (Ø14.5 mm x 4.5 mm deep) at 60/180/300 deg for optional
    # support-free plug-in mvp_syringe_tower_addon
    for deg in (60.0, 180.0, 300.0):
        sx = p.SYRINGE_PILLAR_RING_R * math.cos(math.radians(deg))
        sy = p.SYRINGE_PILLAR_RING_R * math.sin(math.radians(deg))
        sock = Pos(sx, sy, p.Z_LID_TOP - 4.5) * Cylinder(
            (p.SYRINGE_PILLAR_DIA + 0.5) / 2.0,
            5.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        lid = lid - sock

    return lid


def mvp_top_lid_pegs():
    """Standard slide-on top lid with 3x upward alignment pegs (Ø13.8 mm x 11.4 mm
    above Z_LID_TOP) at 60/180/300 deg that mate into the Ø14.2 mm wing holes of
    mvp_syringe_cage_snap_falcon_funnel.
    """
    lid = mvp_top_lid()
    peg_r = (p.SYRINGE_PILLAR_DIA - 0.2) / 2.0  # 6.9 mm (Ø13.8 mm)
    peg_z0 = p.Z_LID_TOP - 5.0  # anchor 0.5 mm into the 4.5 mm socket floor
    peg_h = 5.0 + (3.8 * 3.0)  # protrudes 11.4 mm (3x) above Z_LID_TOP through 4.0 mm wing
    for deg in (60.0, 180.0, 300.0):
        sx = p.SYRINGE_PILLAR_RING_R * math.cos(math.radians(deg))
        sy = p.SYRINGE_PILLAR_RING_R * math.sin(math.radians(deg))
        peg_cyl = Pos(sx, sy, peg_z0) * Cylinder(
            peg_r,
            peg_h - 1.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        peg_tip = Pos(sx, sy, peg_z0 + peg_h - 1.0) * Cone(
            peg_r,
            peg_r - 1.0,
            1.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        lid = lid + peg_cyl + peg_tip
    return lid


def mvp_top_lid_syringe_tower():
    """Extended lid variant with a 165 mm (6.5 in) 3-pillar frame on top.

    Built on top of mvp_top_lid, adding three 15 mm (1.5 cm) diameter pillars
    at 60/180/300 deg (clear of all three lid ports) supporting a top ring and
    central Ø32 mm syringe cradle to hold a 50 mL medical syringe upright over
    the ceramic candle.
    """
    lid = mvp_top_lid()
    z_base = p.Z_LID_TOP
    z_ring_bot = z_base + p.SYRINGE_TOWER_HEIGHT - p.SYRINGE_TOP_RING_THICKNESS

    # Three 14 mm (1.4 cm) vertical frame pillars (anchored below the 4.5 mm sockets into lid roof)
    for deg in (60.0, 180.0, 300.0):
        px = p.SYRINGE_PILLAR_RING_R * math.cos(math.radians(deg))
        py = p.SYRINGE_PILLAR_RING_R * math.sin(math.radians(deg))
        pillar = Pos(px, py, z_base - 5.5) * Cylinder(
            p.SYRINGE_PILLAR_DIA / 2.0,
            p.SYRINGE_TOWER_HEIGHT - p.SYRINGE_TOP_RING_THICKNESS + 6.5,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        lid = lid + pillar

    # Top outer ring connecting the 3 pillars (open center, Ø66 mm clear ID)
    top_ring = _tube(
        p.SYRINGE_TOP_RING_ID / 2.0,
        p.LID_OD / 2.0,
        p.SYRINGE_TOP_RING_THICKNESS,
        z_ring_bot,
    )

    return lid + top_ring


def mvp_top_lid_syringe_cage():
    """Compact lid variant with a central 6-rib cylindrical cage (Ø32 mm ID,
    Ø38 mm OD, 45 mm tall) to hold a 50 mL syringe shaft upright in the middle.

    Uses a central Ø13.2 mm candle stem bore in the lid roof (matching the
    compact cage footprint) plus the same 90.5 mm slide-on skirt and 3 ports.
    """
    r_outer = p.LID_OD / 2.0
    r_skirt_in = p.LID_SKIRT_ID / 2.0

    roof = Pos(0, 0, p.Z_TUBE_TOP) * Cylinder(
        r_outer, p.ROOF_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    skirt = _tube(r_skirt_in, r_outer, p.SKIRT_ENGAGEMENT, p.Z_LID_SKIRT_BOTTOM)
    chamfer_cone = _frustum(r_skirt_in + 1.2, r_skirt_in, 1.5, p.Z_LID_SKIRT_BOTTOM)
    lid = roof + skirt - chamfer_cone

    # Central Ø13.2 mm candle stem bore
    stem_bore = Pos(0, 0, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.CANDLE_STEM_BORE_CLEARANCE / 2.0,
        p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    # 3 outer ports (0 deg Luer, 120 deg air, 240 deg sensor)
    px1, py1 = p.PORT_RING_RADIUS, 0.0
    luer_socket = Pos(px1, py1, p.Z_TUBE_TOP) * Cone(
        p.LUER_BOT_DIA / 2.0, p.LUER_TOP_DIA / 2.0, p.ROOF_THICKNESS + 0.5,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    luer_thru = Pos(px1, py1, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.LUER_THRU_DIA / 2.0, p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    px2 = p.PORT_RING_RADIUS * math.cos(math.radians(240.0))
    py2 = p.PORT_RING_RADIUS * math.sin(math.radians(240.0))
    air_bore = Pos(px2, py2, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.AIR_PORT_BORE_DIA / 2.0, p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    px3 = p.PORT_RING_RADIUS * math.cos(math.radians(120.0))
    py3 = p.PORT_RING_RADIUS * math.sin(math.radians(120.0))
    sensor_bore = Pos(px3, py3, p.Z_TUBE_TOP - 1.0) * Cylinder(
        p.SENSOR_PORT_BORE_DIA / 2.0, p.ROOF_THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    lid = lid - stem_bore - luer_socket - luer_thru - air_bore - sensor_bore

    # Central 4-pillar cylindrical cage (Ø32 mm ID, Ø38 mm OD, 45 mm tall)
    # Wide 90-deg windows give easy finger access to tighten the ceramic candle wing nut
    r_in = p.CAGE_ID / 2.0
    r_out = r_in + p.CAGE_WALL
    r_mid = (r_in + r_out) / 2.0
    z0 = p.Z_LID_TOP - 0.5
    bot_ring = _tube(r_in, r_out, p.CAGE_RING_HEIGHT + 0.5, z0)
    top_ring = _tube(r_in, r_out, p.CAGE_RING_HEIGHT, p.Z_LID_TOP + p.CAGE_HEIGHT - p.CAGE_RING_HEIGHT)
    rib_h = p.CAGE_HEIGHT - 2.0 * p.CAGE_RING_HEIGHT + 3.0
    z_rib = p.Z_LID_TOP + p.CAGE_RING_HEIGHT - 1.5

    cage = bot_ring + top_ring
    for i in range(p.CAGE_NUM_RIBS):
        ang = 45.0 + i * (360.0 / p.CAGE_NUM_RIBS)
        rib = Rot(0, 0, ang) * Pos(r_mid, 0, z_rib) * Box(
            p.CAGE_WALL, p.CAGE_RIB_WIDTH, rib_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        cage = cage + rib

    return lid + cage


def _bottom_base_core(m3_angles):
    """Shared builder for 3D-printed funneling sump base (print upright, Z = 0 on bed)."""
    r_body = p.BASE_BODY_OD / 2.0
    r_flange = p.BASE_FLANGE_OD / 2.0
    r_socket = p.BASE_SOCKET_ID / 2.0
    r_tube_in = p.TUBE_ID / 2.0
    r_drain = p.DRAIN_BORE_DIA / 2.0

    # Main cylindrical body + stability foot
    foot = Cylinder(r_flange, p.BASE_FOOT_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
    body = Cylinder(r_body, p.Z_BASE_TOP, align=(Align.CENTER, Align.CENTER, Align.MIN))
    base = foot + body

    # Cut tube socket (from Z_TUBE_SEAT to Z_BASE_TOP)
    socket_cut = Pos(0, 0, p.Z_TUBE_SEAT) * Cylinder(
        r_socket, p.SKIRT_ENGAGEMENT + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Lead-in chamfer at top mouth of base socket
    socket_chamfer = _frustum(r_socket, r_socket + 1.2, 1.5, p.Z_BASE_TOP - 1.5)
    base = base - socket_cut - socket_chamfer

    # Cut conical nutrient funnel (from FUNNEL_APEX_Z to Z_TUBE_SEAT)
    funnel_cut = _frustum(r_drain, r_tube_in, p.Z_TUBE_SEAT - p.FUNNEL_APEX_Z, p.FUNNEL_APEX_Z)
    # Small cylindrical sump well at apex to meet horizontal drain cleanly
    sump_well = Pos(0, 0, p.FUNNEL_APEX_Z - 0.5) * Cylinder(
        r_drain, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    base = base - funnel_cut - sump_well

    # Add downward-sloped (8.5 deg) side-exit 1/4" hose barb along +X
    x_start = r_body - 4.0
    shaft_len = p.DRAIN_BARB_LEN + 4.0
    drain_xform = Pos(0, 0, p.DRAIN_CENTER_Z) * Rot(0, p.DRAIN_SLOPE_DEG, 0)
    barb_shaft = (
        Pos(x_start, 0, 0)
        * Rot(0, 90, 0)
        * Cylinder(p.DRAIN_BARB_SHAFT_OD / 2.0, shaft_len, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    # Two retention barb cones along the shaft
    barb_tip = (
        Pos(r_body + p.DRAIN_BARB_LEN - 5.0, 0, 0)
        * Rot(0, 90, 0)
        * Cone(
            p.DRAIN_BARB_RIB_OD / 2.0,
            p.DRAIN_BARB_SHAFT_OD / 2.0 - 0.4,
            5.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
    )
    barb_mid = (
        Pos(r_body + p.DRAIN_BARB_LEN - 11.0, 0, 0)
        * Rot(0, 90, 0)
        * Cone(
            p.DRAIN_BARB_RIB_OD / 2.0,
            p.DRAIN_BARB_SHAFT_OD / 2.0,
            4.5,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
    )

    base = base + (drain_xform * (barb_shaft + barb_tip + barb_mid))

    # Cut downward-sloped drain bore from X = 0 all the way out through the barb
    drain_bore = drain_xform * (
        Pos(-1.0, 0, 0)
        * Rot(0, 90, 0)
        * Cylinder(r_drain, r_body + p.DRAIN_BARB_LEN + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    base = base - drain_bore

    # Carve 3 smooth arched electronics/humidifier bays down to Z = 4.0 mm
    # clipped by the conical funnel safety envelope (>= 6 mm perpendicular wall)
    pedestal_h = p.BAY_PEDESTAL_TOP_Z - p.BAY_FLOOR_Z
    cone_h = p.BAY_CEILING_TOP_Z - p.BAY_PEDESTAL_TOP_Z

    lower_bay = _tube(p.BAY_PEDESTAL_R, r_flange + 2.0, pedestal_h, p.BAY_FLOOR_Z)
    upper_outer = Pos(0, 0, p.BAY_PEDESTAL_TOP_Z) * Cylinder(
        r_flange + 2.0, cone_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    upper_cone = _frustum(p.BAY_PEDESTAL_R, r_body, cone_h, p.BAY_PEDESTAL_TOP_Z)
    funnel_safety_cut = lower_bay + (upper_outer - upper_cone)

    for deg in p.BAY_ARCH_ANGLES_DEG:
        arch_cyl = (
            Rot(0, 0, deg)
            * Pos(0, 0, p.BAY_FLOOR_Z)
            * Rot(0, 90, 0)
            * Cylinder(
                p.BAY_ARCH_RADIUS,
                r_flange + 4.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        )
        base = base - (arch_cyl & funnel_safety_cut)

        # 4x M3 self-tapping mounting holes (16 x 25.4 mm pattern) on bay floor
        if deg in m3_angles:
            for r_hole in p.ARDUINO_HOLE_RADII:
                for dy in (-p.ARDUINO_HOLE_Y_OFFSET, p.ARDUINO_HOLE_Y_OFFSET):
                    hx = r_hole * math.cos(math.radians(deg)) - dy * math.sin(math.radians(deg))
                    hy = r_hole * math.sin(math.radians(deg)) + dy * math.cos(math.radians(deg))
                    m3_hole = Pos(hx, hy, -0.5) * Cylinder(
                        p.ARDUINO_M3_HOLE_DIA / 2.0,
                        p.BAY_FLOOR_Z + 1.0,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
                    base = base - m3_hole
            if deg == 180.0:
                for zy in (-15.0, 15.0):
                    tie_slot = (
                        Rot(0, 0, deg)
                        * Pos(36.0, zy, -0.5)
                        * Box(2.5, 4.5, p.BAY_FLOOR_Z + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
                    )
                    base = base - tie_slot

    return base


def _c_clip_cradle(
    angle_deg: float,
    radius_r: float,
    z_center: float,
    bore_id: float,
    spacing: float,
    wall: float = 3.0,
    width: float = 10.0,
    snap_tilt_deg: float = 45.0,
):
    """Build twin support-free snap-in C-clips with Z=0 pedestals."""
    r_in = bore_id / 2.0
    r_out = r_in + wall
    half_span = spacing / 2.0
    clips = None
    for dy in (-half_span, half_span):
        clip_outer = (
            Pos(radius_r, dy, z_center)
            * Rot(90, 0, 0)
            * Cylinder(r_out, width, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        )
        clip_ped = Pos(radius_r, dy, 0.0) * Box(
            r_out * 1.4, width, z_center, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        clip_bore = (
            Pos(radius_r, dy, z_center)
            * Rot(90, 0, 0)
            * Cylinder(r_in, width + 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        )
        snap_slot = (
            Pos(radius_r, dy, z_center)
            * Rot(0, snap_tilt_deg, 0)
            * Box(
                bore_id * 0.84,
                width + 2.0,
                r_out + 4.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        )
        one_clip = Rot(0, 0, angle_deg) * ((clip_outer + clip_ped) - clip_bore - snap_slot)
        clips = one_clip if clips is None else (clips + one_clip)
    return clips


def mvp_bottom_base():
    """Standard funneling sump base with M3 Arduino holes & front air-pump clips."""
    base = _bottom_base_core(p.BAY_ARCH_ANGLES_DEG)
    pump_clips = _c_clip_cradle(
        p.PUMP_CLIP_ANGLE_DEG,
        p.PUMP_CLIP_R,
        p.PUMP_CLIP_Z,
        p.PUMP_BARREL_ID,
        p.PUMP_CLIP_SPACING,
        snap_tilt_deg=0.0,
    )
    return base + pump_clips


def mvp_bottom_base_collection():
    """Base variant with integrated 10 mL collection syringe cradle (75 deg)
    and front Ø27.4 mm air-pump snap-in clips (285 deg).
    """
    base = _bottom_base_core((180.0, 285.0))
    syringe_clips = _c_clip_cradle(
        p.COLL_CRADLE_ANGLE_DEG,
        p.COLL_CRADLE_R,
        p.COLL_CRADLE_Z,
        p.COLL_SYRINGE_BARREL_ID,
        p.COLL_CLIP_SPACING,
        wall=p.COLL_CLIP_WALL,
        width=p.COLL_CLIP_WIDTH,
        snap_tilt_deg=45.0,
    )
    pump_clips = _c_clip_cradle(
        p.PUMP_CLIP_ANGLE_DEG,
        p.PUMP_CLIP_R,
        p.PUMP_CLIP_Z,
        p.PUMP_BARREL_ID,
        p.PUMP_CLIP_SPACING,
        snap_tilt_deg=0.0,
    )
    return base + syringe_clips + pump_clips


def mvp_port_barb_insert():
    """Optional printable push-in barb adapter for the 6.0 mm air inlet port.

    Print upright (flange down) with zero supports; press into the lid's 6.0 mm
    humid-air port if connecting soft 4 mm ID (3/16") silicone tubing.
    """
    # 6.0 mm plug shank (6 mm long) + 9 mm collar + 10 mm barbed tail for 4 mm ID tubing
    shank = Cylinder(2.95, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    collar = Pos(0, 0, 6.0) * Cylinder(4.5, 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    tail = Pos(0, 0, 8.0) * Cylinder(2.15, 10.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    rib = Pos(0, 0, 14.0) * Cone(2.6, 1.9, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    bore = Pos(0, 0, -0.5) * Cylinder(1.4, 19.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return (shank + collar + tail + rib) - bore


def mvp_candle_collar():
    """Printable top-loading retention collar for the 4-inch ceramic candle.

    Mounts onto the candle's 1/4" BSP / ~12.5 mm threaded stem (secured by its
    wing nut + washer), then drops straight into the stepped pocket of
    mvp_top_lid from the top so the candle cannot fall into the chamber.
    Print flat-side down with zero supports.
    """
    z_bot = p.Z_LID_TOP - p.CANDLE_POCKET_DEPTH
    flange = Pos(0, 0, z_bot) * Cylinder(
        p.CANDLE_COLLAR_OD / 2.0,
        p.CANDLE_COLLAR_THICKNESS,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    stem_hole = Pos(0, 0, z_bot - 0.5) * Cylinder(
        p.CANDLE_STEM_BORE_CLEARANCE / 2.0,
        p.CANDLE_COLLAR_THICKNESS + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return flange - stem_hole


def _syringe_tower_addon(height: float):
    """Shared builder for support-free plug-in syringe tower (print upside-down).

    Three Ø14.0 mm pillars plug into the Ø14.5 mm sockets on mvp_top_lid.
    """
    z_sock_bot = p.Z_LID_TOP - 4.2
    z_ring_bot = p.Z_LID_TOP + height - p.SYRINGE_TOP_RING_THICKNESS
    pillar_h = z_ring_bot - z_sock_bot + 1.0

    tower = None
    for deg in (60.0, 180.0, 300.0):
        px = p.SYRINGE_PILLAR_RING_R * math.cos(math.radians(deg))
        py = p.SYRINGE_PILLAR_RING_R * math.sin(math.radians(deg))
        pillar = Pos(px, py, z_sock_bot) * Cylinder(
            p.SYRINGE_PILLAR_DIA / 2.0,
            pillar_h,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        tower = pillar if tower is None else (tower + pillar)

    top_ring = _tube(
        p.SYRINGE_TOP_RING_ID / 2.0,
        p.LID_OD / 2.0,
        p.SYRINGE_TOP_RING_THICKNESS,
        z_ring_bot,
    )

    return tower + top_ring


def mvp_syringe_tower_addon():
    """Full-height (165.0 mm / 6.5 in) support-free plug-in syringe tower."""
    return _syringe_tower_addon(p.SYRINGE_TOWER_HEIGHT)


def mvp_syringe_tower_addon_half():
    """Half-height (82.5 mm / 3.25 in) support-free plug-in syringe tower."""
    return _syringe_tower_addon(p.SYRINGE_TOWER_HALF_HEIGHT)


def _syringe_cage_addon(cage_id: float, rib_angles=(45.0, 135.0, 225.0, 315.0), rib_width: float = p.CAGE_RIB_WIDTH):
    """Shared builder for 100% support-free glue-on central syringe cage.

    Sits flush on top of mvp_candle_collar (Z = Z_LID_TOP, Ø58 mm OD, Ø28 mm
    wing-nut clearance) with a 45-deg self-supporting flare into the vertical
    central cage. Print upside-down (top ring on bed) with zero supports.
    """
    r_in = cage_id / 2.0
    r_out = r_in + p.CAGE_WALL
    r_mid = (r_in + r_out) / 2.0
    r_base_out = p.CAGE_ADDON_BASE_OD / 2.0
    r_base_in = p.CAGE_ADDON_BASE_ID / 2.0

    z0 = p.Z_LID_TOP
    flare_h = max(4.0, r_base_out - r_out)  # 45-deg flare when printed upside-down
    base_plate_h = 3.0

    # Glue-on base ring + 45-deg transition collar
    base_ring = _tube(r_base_in, r_base_out, base_plate_h, z0)
    flare_outer = _frustum(r_base_out, r_out, flare_h, z0 + base_plate_h)
    flare_inner = _frustum(r_base_in, r_in, flare_h + 0.2, z0 + base_plate_h - 0.1)
    collar_base = base_ring + (flare_outer - flare_inner)

    z_cage_start = z0 + base_plate_h + flare_h
    z_top_ring = z_cage_start + p.CAGE_HEIGHT - p.CAGE_RING_HEIGHT
    top_ring = _tube(r_in, r_out, p.CAGE_RING_HEIGHT, z_top_ring)

    rib_h = (z_top_ring - z_cage_start) + 2.0
    cage = collar_base + top_ring
    for ang in rib_angles:
        rib = Rot(0, 0, ang) * Pos(r_mid, 0, z_cage_start - 1.0) * Box(
            p.CAGE_WALL, rib_width, rib_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        cage = cage + rib

    return cage


def mvp_syringe_cage_addon():
    """Glue-on 50 mL syringe cage (Ø32.0 mm ID) for mvp_candle_collar."""
    return _syringe_cage_addon(p.CAGE_ID)


def mvp_syringe_cage_addon_25ml():
    """Glue-on 25 mL syringe cage (Ø23.5 mm ID) for mvp_candle_collar."""
    return _syringe_cage_addon(p.CAGE_25ML_ID)


def mvp_cage_retainer_ring():
    """Support-free 3-arm retainer ring that slides down over the 45-deg slanted
    base of the syringe cage ('net') and plugs into the 3x Ø14.5 mm circular
    indents on mvp_top_lid. Print upside-down (flat top on build plate).
    """
    z_bot = p.Z_LID_TOP + 5.0
    z_top = p.Z_LID_TOP + 13.0
    h_ring = z_top - z_bot  # 8.0 mm
    r_out = 30.0            # 60.0 mm OD (clears all 3 outer ports at R = 35.5 mm)

    ring_outer = Pos(0, 0, z_bot) * Cylinder(
        r_out, h_ring, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    ring_inner = _frustum(27.5, 20.25, h_ring + 0.2, z_bot - 0.1)
    retainer = ring_outer - ring_inner

    # 3 radial arms at 60/180/300 deg with downward Ø14.0 mm plug-in pins
    z_pin_bot = p.Z_LID_TOP - 4.2
    pin_total_h = z_top - z_pin_bot
    arm_len = (p.LID_OD / 2.0) - (r_out - 2.0)
    r_arm_mid = (p.LID_OD / 2.0 + (r_out - 2.0)) / 2.0

    for deg in (60.0, 180.0, 300.0):
        arm = Rot(0, 0, deg) * Pos(r_arm_mid, 0, z_bot) * Box(
            arm_len, 16.0, h_ring, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        px = p.SYRINGE_PILLAR_RING_R * math.cos(math.radians(deg))
        py = p.SYRINGE_PILLAR_RING_R * math.sin(math.radians(deg))
        pin = Pos(px, py, z_pin_bot) * Cylinder(
            p.SYRINGE_PILLAR_DIA / 2.0,
            pin_total_h,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        retainer = retainer + arm + pin

    return retainer


def _syringe_cage_snap(cage_id: float):
    """Single-piece snap-on syringe cage ('net') with 3 vertical struts aligned
    at 60/180/300 deg to join seamlessly with the 45-deg triangular gussets and
    3-pin wings. Print upside-down (zero supports).
    """
    wing_angles = (60.0, 180.0, 300.0)
    cage = _syringe_cage_addon(cage_id, rib_angles=wing_angles, rib_width=6.0)
    r_out = (cage_id / 2.0) + p.CAGE_WALL
    r_gusset_in = max(r_out - 1.5, p.CAGE_ADDON_BASE_ID / 2.0)  # Joins strut wall without grazing inner bore
    r_base_out = p.CAGE_ADDON_BASE_OD / 2.0
    arm_len = (p.LID_OD / 2.0) - (r_base_out - 2.0)
    r_arm_mid = (p.LID_OD / 2.0 + (r_base_out - 2.0)) / 2.0
    z0 = p.Z_LID_TOP
    z_pin_bot = z0 - 4.2
    gusset_h = (p.LID_OD / 2.0) - r_gusset_in

    for deg in wing_angles:
        arm = Rot(0, 0, deg) * Pos(r_arm_mid, 0, z0) * Box(
            arm_len, 16.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        px = p.SYRINGE_PILLAR_RING_R * math.cos(math.radians(deg))
        py = p.SYRINGE_PILLAR_RING_R * math.sin(math.radians(deg))
        pin = Pos(px, py, z_pin_bot) * Cylinder(
            p.SYRINGE_PILLAR_DIA / 2.0,
            8.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        # 45-deg triangular gusset joining directly into the vertical cage strut & wing
        gusset_prof = Polygon((r_gusset_in, 0.0), (49.0, 0.0), (r_gusset_in, gusset_h), align=None)
        gusset_3d = Pos(0, 0, z0 + 3.0) * Rot(90, 0, 0) * extrude(gusset_prof, amount=3.0, both=True)
        gusset = Rot(0, 0, deg) * gusset_3d
        cage = cage + arm + pin + gusset

    return cage


def mvp_syringe_cage_snap():
    """Single-piece snap-on 50 mL syringe cage (Ø32.0 mm ID)."""
    return _syringe_cage_snap(p.CAGE_ID)


def mvp_syringe_cage_snap_25ml():
    """Single-piece snap-on 25 mL syringe cage (Ø23.5 mm ID)."""
    return _syringe_cage_snap(p.CAGE_25ML_ID)


def mvp_syringe_cage_snap_falcon():
    """Single-piece Snap-On 50 mL Net with an integrated 2-port 50 mL Falcon
    tube cap/holder on the 300 deg wing (opposite the 75 deg 10 mL syringe).

    The 300 deg wing extends straight out at Z = Z_LID_TOP..+4.0 as the cap
    roof with two Ø6.0 mm tubing bores, while the Ø31.4 mm press-fit skirt and
    Ø26.0 mm inner sealing plug hang below so the Falcon tube pushes up into it.
    """
    cage = mvp_syringe_cage_snap()
    z0 = p.Z_LID_TOP
    fx = p.FALCON_LOOP_R * math.cos(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    fy = p.FALCON_LOOP_R * math.sin(math.radians(p.FALCON_LOOP_ANGLE_DEG))

    # Flat bridge from 300 deg wing (R = 47) to Falcon cap center (R = 68) at Z = z0..z0+4
    bridge_len = p.FALCON_LOOP_R - 46.0
    bridge_mid = (p.FALCON_LOOP_R + 46.0) / 2.0
    bridge = Rot(0, 0, p.FALCON_LOOP_ANGLE_DEG) * Pos(bridge_mid, 0, z0) * Box(
        bridge_len, 20.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # 45-deg support-free gusset from cage/wing to cap edge (R = 49.8)
    gusset_prof = Polygon((34.0, 0.0), (52.0, 0.0), (34.0, 18.0), align=None)
    gusset = (
        Rot(0, 0, p.FALCON_LOOP_ANGLE_DEG)
        * Pos(0, 0, z0 + 4.0)
        * Rot(90, 0, 0)
        * extrude(gusset_prof, amount=3.0, both=True)
    )

    # Integrated 2-port Falcon cap (roof at z0..z0+4, skirt & plug hanging down)
    cap_roof = Pos(fx, fy, z0) * Cylinder(
        p.FALCON_CAP_OD / 2.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    cap_skirt = Pos(fx, fy, 0.0) * _falcon_threaded_skirt(z0 - 10.0, 10.0)
    cap_plug = Pos(fx, fy, 0.0) * _tube(
        11.0, p.FALCON_CAP_PLUG_OD / 2.0, 7.0, z0 - 7.0
    )
    merged = cage + bridge + gusset + cap_roof + cap_skirt + cap_plug

    # Two Ø6.0 mm tubing bores spaced 13.0 mm apart through the cap roof
    for dx in (-p.FALCON_CAP_PORT_SPACING / 2.0, p.FALCON_CAP_PORT_SPACING / 2.0):
        hole = Pos(fx + dx, fy, z0 - 1.0) * Cylinder(
            p.AIR_PORT_BORE_DIA / 2.0, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        merged = merged - hole

    return merged


def mvp_syringe_cage_snap_falcon_funnel():
    """Simplified, larger-volume (~11.5 mL) Double-Funnel Net + 300 deg
    threaded Falcon cap.

    The double-funnel belly (Ø39.5 mm OD / Ø33.5 mm ID) serves directly as the
    base of the 3-strut syringe cage—eliminating radial webs and the separate
    collar flare while nearly tripling internal buffer volume.
    """
    z0 = p.Z_LID_TOP
    r_in = p.CAGE_ID / 2.0            # 16.75 mm (Ø33.5 mm)
    r_out = r_in + p.CAGE_WALL        # 19.75 mm (Ø39.5 mm)
    r_mid = (r_in + r_out) / 2.0
    r_base_out = p.CAGE_ADDON_BASE_OD / 2.0
    wing_angles = (60.0, 180.0, 300.0)

    # 1. Snap-in base ring (Ø20 mm ID to Ø58 mm OD, z0..z0+3) + 3 curved Ø21 mm wing lobes + wrap-around gussets
    base = _tube(10.0, r_base_out, 3.0, z0)
    r_hole = (p.SYRINGE_PILLAR_DIA + 0.2) / 2.0  # 7.1 mm (Ø14.2 mm)
    r_boss = 10.5  # Ø21.0 mm curved outer boss (3.4 mm wall around hole)
    r_wing_in = r_base_out - 2.0
    for deg in wing_angles:
        arm_rect = Pos(0, 0, z0) * extrude(
            Polygon(
                (r_wing_in, -r_boss),
                (p.SYRINGE_PILLAR_RING_R, -r_boss),
                (p.SYRINGE_PILLAR_RING_R, r_boss),
                (r_wing_in, r_boss),
                align=None,
            ),
            amount=4.0,
        )
        arm_boss = Pos(p.SYRINGE_PILLAR_RING_R, 0, z0) * Cylinder(
            r_boss, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        arm = arm_rect + arm_boss

        # Wishbone gusset: flows around both edges of the Ø21 mm circle without overhanging the hole
        stem = extrude(
            Polygon((17.5, -3.0), (33.5, -3.0), (33.5, 3.0), (17.5, 3.0), align=None),
            amount=32.0,
        )
        rib_pos = extrude(
            Polygon((27.5, 2.8), (42.5, r_boss - 0.8), (42.5, r_hole - 0.3), (30.5, 0.5), align=None),
            amount=32.0,
        )
        rib_neg = extrude(
            Polygon((27.5, -2.8), (42.5, -(r_boss - 0.8)), (42.5, -(r_hole - 0.3)), (30.5, -0.5), align=None),
            amount=32.0,
        )
        collar_ring = Pos(p.SYRINGE_PILLAR_RING_R, 0, 0.0) * _tube(r_hole - 0.2, r_boss - 0.1, 32.0, 0.0)
        wedge = Rot(90, 0, 0) * extrude(
            Polygon((17.5, 0.0), (47.5, 0.0), (17.5, 30.0), align=None),
            amount=15.0,
            both=True,
        )
        gusset_3d = Pos(0, 0, z0 + 3.2) * ((stem + rib_pos + rib_neg + collar_ring) & wedge)
        base = base + (Rot(0, 0, deg) * (arm + gusset_3d))

    # 2. Integrated 300 deg threaded 50 mL Falcon cap (skirt bottom flush at z0, roof at z0+10..+14)
    fx = p.FALCON_LOOP_R * math.cos(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    fy = p.FALCON_LOOP_R * math.sin(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    r_bridge_in = 46.0
    r_bridge_out = p.FALCON_LOOP_R - (p.FALCON_CAP_OD / 2.0) + 2.0  # 51.0 mm (embeds 2 mm into skirt wall)
    bridge_len = r_bridge_out - r_bridge_in
    bridge_mid = (r_bridge_out + r_bridge_in) / 2.0
    bridge = Rot(0, 0, p.FALCON_LOOP_ANGLE_DEG) * Pos(bridge_mid, 0, z0) * Box(
        bridge_len, 20.0, 14.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    cap_roof = Pos(fx, fy, z0 + 10.0) * Cylinder(
        p.FALCON_CAP_OD / 2.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    cap_skirt = Pos(fx, fy, 0.0) * _falcon_threaded_skirt(z0, 10.0)
    cap_plug = Pos(fx, fy, 0.0) * _tube(11.0, p.FALCON_CAP_PLUG_OD / 2.0, 7.0, z0 + 3.0)
    base = base + bridge + cap_roof + cap_skirt + cap_plug
    for deg in wing_angles:
        px = p.SYRINGE_PILLAR_RING_R * math.cos(math.radians(deg))
        py = p.SYRINGE_PILLAR_RING_R * math.sin(math.radians(deg))
        pin_hole = Pos(px, py, z0) * Cylinder(
            r_hole, 40.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        base = base - pin_hole
    for dx in (-p.FALCON_CAP_PORT_SPACING / 2.0, p.FALCON_CAP_PORT_SPACING / 2.0):
        hole = Pos(fx + dx, fy, z0 + 9.0) * Cylinder(
            p.AIR_PORT_BORE_DIA / 2.0, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        base = base - hole

    # 3. Unified Double-Funnel Chamber (1/4" BSP -> Ø39.5/33.5 mm belly -> Luer-Lock)
    bot_boss = _internal_thread(
        p.BSP14_ROOT_ID / 2.0, 10.0, z0, 9.0, p.BSP14_PITCH, p.BSP14_DEPTH, tooth_half_base=0.55
    )
    bot_cone_out = _frustum(10.0, r_out, 9.75, z0 + 8.5)
    bot_cone_in = _frustum(p.BSP14_ROOT_ID / 2.0, r_in, 9.95, z0 + 8.4)
    belly = _tube(r_in, r_out, 6.0, z0 + 18.25)
    top_cone_out = _frustum(r_out, 3.35, 16.4, z0 + 24.25)
    top_cone_in = _frustum(r_in, 1.5, 16.6, z0 + 24.15)
    luer_boss = Pos(0, 0, z0 + 34.5) * Cylinder(3.35, 7.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    luer_ears = Pos(0, 0, z0 + 40.8) * Box(7.8, 2.6, 1.2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    luer_taper = Pos(0, 0, z0 + 34.5) * Cone(3.90 / 2.0, 4.30 / 2.0, 7.7, align=(Align.CENTER, Align.CENTER, Align.MIN))

    chamber = (
        bot_boss
        + (bot_cone_out - bot_cone_in)
        + belly
        + (top_cone_out - top_cone_in)
        + luer_boss
        + luer_ears
    ) - luer_taper

    # 4. 3-strut syringe cage rising directly off the Ø39.5 mm funnel belly (2x height = 110 mm)
    # with slim (~4 mm) curved arch ribs meeting at 0/120/240 deg under the top ring
    z_cage_start = z0 + 24.25
    cage_h = p.CAGE_HEIGHT * 2.0
    z_top_ring = z_cage_start + cage_h - p.CAGE_RING_HEIGHT

    a = 16.2
    k = 0.262
    r_arc = (1.0 + k) * a
    arch_h = math.sqrt(r_arc**2 - (k * a) ** 2)  # 20.0 mm tall wide lancet arch
    z_skirt = z_top_ring - arch_h

    ring_wall = _tube(r_in, r_out, p.CAGE_RING_HEIGHT + arch_h, z_skirt)
    rib_h = (z_top_ring - z_cage_start) + 2.5
    cage = ring_wall
    for ang in wing_angles:
        rib = Rot(0, 0, ang) * Pos(r_mid, 0, z_cage_start - 1.2) * Box(
            p.CAGE_WALL, 6.0, rib_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        cage = cage + rib

    # Cut 3 wide pointed lancet windows (0/120/240 deg)
    pts = [(-a, -0.5)]
    n_seg = 16
    for i in range(n_seg + 1):
        x = -a + a * (i / n_seg)
        z = math.sqrt(max(0.0, r_arc**2 - (k * a - x) ** 2))
        pts.append((x, z))
    for i in range(1, n_seg + 1):
        x = a * (i / n_seg)
        z = math.sqrt(max(0.0, r_arc**2 - (k * a + x) ** 2))
        pts.append((x, z))
    pts.append((a, -0.5))
    arch_prof = Polygon(*pts, align=None)
    arch_cut_0 = Pos(r_in - 1.0, 0, z_skirt) * Rot(90, 0, 90) * extrude(arch_prof, amount=p.CAGE_WALL + 4.0)
    for win_ang in (0.0, 120.0, 240.0):
        cage = cage - (Rot(0, 0, win_ang) * arch_cut_0)

    # Cut 3 wide pointed spandrel windows above the stands (60/180/300 deg)
    # removing excess corner plastic so only ~4 mm curved arch ribs remain
    spandrel_prof = Polygon(
        (0.0, 2.0),
        (-7.5, 8.5),
        (-10.0, 13.5),
        (-6.0, 17.0),
        (0.0, arch_h),
        (6.0, 17.0),
        (10.0, 13.5),
        (7.5, 8.5),
        align=None,
    )
    spandrel_cut_0 = Pos(r_in - 1.0, 0, z_skirt) * Rot(90, 0, 90) * extrude(spandrel_prof, amount=p.CAGE_WALL + 4.0)
    for ang in wing_angles:
        cage = cage - (Rot(0, 0, ang) * spandrel_cut_0)

    return base + chamber + cage


def mvp_snap_pin():
    """Printable Ø14.0 x 8.2 mm dowel pin (print 3x flat) that drops through
    the Ø14.2 mm wing holes of mvp_syringe_cage_snap_falcon_funnel into the
    three Ø14.5 mm circular indents on mvp_top_lid.
    """
    return Cylinder(
        p.SYRINGE_PILLAR_DIA / 2.0, 8.2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )


def mvp_luer_stopcock_body():
    """3-Way Luer Stopcock body that plugs into the top Female Luer-Lock of
    mvp_syringe_cage_snap_falcon_funnel, accepts the 50 mL syringe on top, and
    provides a 0 deg (+X) Female Luer gas-bleed port through the open cage window.
    """
    z_seat = p.Z_LID_TOP + 42.0
    z_valve = p.Z_LID_TOP + 52.0

    # Bottom 6% Male Luer nose (Ø4.28 -> Ø3.88 mm, 0.01 mm radial clearance in funnel socket)
    male_nose = Pos(0, 0, z_seat - 7.4) * Cone(
        3.88 / 2.0, 4.28 / 2.0, 7.4, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    shoulder = Pos(0, 0, z_seat) * Cylinder(
        6.0, 4.5, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    # Central horizontal valve barrel along Y (Y = -7.0..+7.0, Ø15.0 mm)
    barrel = (
        Pos(0, -7.0, z_valve)
        * Rot(-90, 0, 0)
        * Cylinder(7.5, 14.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )

    # Top Female Luer-Lock boss (Z = z_valve + 5.5 .. z_valve + 14.0)
    top_boss = Pos(0, 0, z_valve + 5.5) * Cylinder(
        3.35, 8.5, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    top_ears = Pos(0, 0, z_valve + 12.8) * Box(
        7.8, 2.6, 1.2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    # Side 0 deg (+X) Female Luer-Lock bleed port (X = 5.5..18.0 mm)
    side_boss = (
        Pos(5.5, 0, z_valve)
        * Rot(0, 90, 0)
        * Cylinder(3.35, 12.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    side_ears = Pos(17.4, 0, z_valve) * Box(
        1.2, 2.6, 7.8, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )

    body = male_nose + shoulder + barrel + top_boss + top_ears + side_boss + side_ears

    # Cut 1:12 tapered valve seat along Y (Ø10.5 mm at +Y=7 -> Ø9.5 mm at -Y=-7)
    seat_cut = (
        Pos(0, -7.2, z_valve)
        * Rot(-90, 0, 0)
        * Cone(4.74, 5.26, 14.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    # Top Female Luer taper + central Ø2.5 mm bore
    top_taper = Pos(0, 0, z_valve + 6.3) * Cone(
        3.90 / 2.0, 4.30 / 2.0, 7.9, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    top_bore = Pos(0, 0, z_valve) * Cylinder(
        1.25, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Bottom Ø2.0 mm through-bore
    bot_bore = Pos(0, 0, z_seat - 7.6) * Cylinder(
        1.0, 18.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Side Female Luer taper + Ø2.5 mm bleed bore
    side_taper = (
        Pos(10.3, 0, z_valve)
        * Rot(0, 90, 0)
        * Cone(3.90 / 2.0, 4.30 / 2.0, 7.9, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    side_bore = (
        Pos(0, 0, z_valve)
        * Rot(0, 90, 0)
        * Cylinder(1.25, 11.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )

    return body - seat_cut - top_taper - top_bore - bot_bore - side_taper - side_bore


def mvp_luer_stopcock_plug():
    """Rotatable T-bore tapered plug for mvp_luer_stopcock_body (0.15 mm radial
    print clearance). Handle pointing UP (+Z) connects Syringe <-> Funnel;
    rotating toward +X bleeds Syringe or Funnel to the 0 deg side port.
    """
    z_valve = p.Z_LID_TOP + 52.0

    # Tapered plug core (Ø9.16 mm at -Y=-7.2 -> Ø10.2 mm at +Y=7.0)
    plug = (
        Pos(0, -7.2, z_valve)
        * Rot(-90, 0, 0)
        * Cone(4.58, 5.10, 14.2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    # Retaining collar lip on -Y end + ergonomic T-handle on +Y end
    ret_lip = (
        Pos(0, -8.5, z_valve)
        * Rot(-90, 0, 0)
        * Cylinder(5.1, 1.45, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    stem = (
        Pos(0, 7.0, z_valve)
        * Rot(-90, 0, 0)
        * Cylinder(3.5, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    handle = Pos(0, 12.5, z_valve + 3.0) * Box(
        4.0, 3.0, 14.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    plug = plug + ret_lip + stem + handle

    # Cut internal Ø2.5 mm T-bore: vertical through-bore (+Z/-Z) + one side leg (-X)
    t_vert = Pos(0, 0, z_valve - 6.0) * Cylinder(
        1.25, 12.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    t_side = (
        Pos(-6.0, 0, z_valve)
        * Rot(0, 90, 0)
        * Cylinder(1.25, 6.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    return plug - t_vert - t_side


def mvp_top_lid_falcon():
    """Lid variant with a side-mounted Ø30.8 mm loop at 120 deg (next to the
    humid air inlet port) so a 50 mL Falcon tube humidifier slides in from above.
    Prints upside-down with zero supports.
    """
    lid = mvp_top_lid()
    r_in = p.FALCON_LOOP_ID / 2.0
    r_out = r_in + p.FALCON_LOOP_WALL
    z_bot = p.Z_LID_TOP - p.FALCON_LOOP_HEIGHT

    # Neck bridging lid rim (R = 47 mm) to loop outer wall (R = 52.6 mm)
    neck_start = (p.LID_OD / 2.0) - 2.0
    neck_end = p.FALCON_LOOP_R - r_in
    neck_len = neck_end - neck_start
    neck_mid = (neck_start + neck_end) / 2.0
    neck = Rot(0, 0, p.FALCON_LOOP_ANGLE_DEG) * Pos(neck_mid, 0, z_bot) * Box(
        neck_len, 16.0, p.FALCON_LOOP_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    fx = p.FALCON_LOOP_R * math.cos(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    fy = p.FALCON_LOOP_R * math.sin(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    loop_outer = Pos(fx, fy, z_bot) * Cylinder(
        r_out, p.FALCON_LOOP_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    loop_bore = Pos(fx, fy, z_bot - 0.5) * Cylinder(
        r_in, p.FALCON_LOOP_HEIGHT + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return (lid + neck + loop_outer) - loop_bore


def _internal_thread(
    r_root: float,
    r_out: float,
    z_bot: float,
    height: float,
    pitch: float,
    depth: float,
    tooth_half_base: float = 1.1,
):
    """Build a support-free internal 45-deg helical thread inside a cylindrical wall."""
    skirt = _tube(r_root, r_out, height, z_bot)
    margin = tooth_half_base + 0.2
    thread_h = max(pitch, height - 2.0 * margin)
    helix = Pos(0, 0, z_bot + margin) * Helix(
        pitch=pitch, height=thread_h, radius=r_root
    )
    tooth = Plane.XZ * Pos(0, z_bot + margin) * Polygon(
        (r_root + 0.3, -tooth_half_base),
        (r_root - depth, 0.0),
        (r_root + 0.3, tooth_half_base),
        align=None,
    )
    ridge = sweep(tooth, path=helix, is_frenet=True)
    return skirt + ridge


def _falcon_threaded_skirt(z_bot: float, height: float = 10.0):
    """Build a Ø38 mm Falcon cap skirt with internal 45-deg helical thread ridges."""
    return _internal_thread(
        p.FALCON_CAP_SKIRT_ID / 2.0,
        p.FALCON_CAP_OD / 2.0,
        z_bot,
        height,
        p.FALCON_THREAD_PITCH,
        p.FALCON_THREAD_DEPTH,
        tooth_half_base=1.1,
    )


def mvp_falcon_cap_2port():
    """2-port screw-on cap for a 50 mL Falcon tube humidifier.

    Features an outer Ø31.6 mm skirt with internal 3.2 mm-pitch thread ridges,
    a Ø26.0 mm inner sealing plug, and two Ø6.0 mm bores (13 mm apart).
    Print upside-down with zero supports.
    """
    fx = p.FALCON_LOOP_R * math.cos(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    fy = p.FALCON_LOOP_R * math.sin(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    z_skirt_bot = p.Z_LID_TOP + 0.5
    skirt_h = 10.0
    roof_h = 4.5
    z_roof_bot = z_skirt_bot + skirt_h

    skirt = _falcon_threaded_skirt(z_skirt_bot, skirt_h)
    roof = Pos(0, 0, z_roof_bot) * Cylinder(
        p.FALCON_CAP_OD / 2.0, roof_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Inner hollow plug (Ø26.0 mm OD / Ø22.0 mm ID)
    plug = _tube(11.0, p.FALCON_CAP_PLUG_OD / 2.0, 7.0, z_roof_bot - 7.0)
    cap = skirt + roof + plug

    # 2x Ø6.0 mm tubing bores spaced 13.0 mm apart
    for dx in (-p.FALCON_CAP_PORT_SPACING / 2.0, p.FALCON_CAP_PORT_SPACING / 2.0):
        hole = Pos(dx, 0, z_roof_bot - 1.0) * Cylinder(
            p.AIR_PORT_BORE_DIA / 2.0, roof_h + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        cap = cap - hole

    return Pos(fx, fy, 0.0) * cap


def mvp_falcon_50ml_ref():
    """Reference solid for a 50 mL conical Falcon tube hanging in the lid loop."""
    fx = p.FALCON_LOOP_R * math.cos(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    fy = p.FALCON_LOOP_R * math.sin(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    z_top = p.Z_LID_TOP + 10.0
    z_cyl_bot = z_top - 85.0
    z_tip = z_cyl_bot - 30.0

    cyl = _tube(13.4, 14.8, 85.0, z_cyl_bot)
    cone_out = _frustum(3.0, 14.8, 30.0, z_tip)
    cone_in = _frustum(1.6, 13.4, 28.0, z_tip + 2.0)
    return Pos(fx, fy, 0.0) * (cyl + (cone_out - cone_in))


def _pipe(pts, radius: float):
    """Sweep a circular cross-section along a smooth 3D spline."""
    path = Spline(*pts)
    section = Plane(origin=pts[0], z_dir=path.tangent_at(0.0)) * Circle(radius)
    return sweep(section, path)


def mvp_electronics_ref():
    """Reference solids for ESP32 (180 deg bay), Relay/MOSFET (285 deg bay),
    Mini Air Pump (clipped into front 285 deg C-clips), and 5V Power Supply.
    """
    esp32 = Pos(-39.0, 0.0, 5.0) * Box(24.0, 48.0, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    relay = Rot(0, 0, 285.0) * Pos(30.0, 0.0, 5.0) * Box(
        18.0, 28.0, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    pump = (
        Rot(0, 0, p.PUMP_CLIP_ANGLE_DEG)
        * Pos(p.PUMP_CLIP_R, 0.0, p.PUMP_CLIP_Z)
        * Rot(-90, 0, 0)
        * Cylinder(13.5, 55.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    )
    pump_nozzle = (
        Rot(0, 0, p.PUMP_CLIP_ANGLE_DEG)
        * Pos(p.PUMP_CLIP_R, 32.0, p.PUMP_CLIP_Z)
        * Rot(-90, 0, 0)
        * Cylinder(3.5, 10.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    )
    psu = Pos(-95.0, -45.0, 0.0) * Box(38.0, 55.0, 24.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return esp32 + relay + pump + pump_nozzle + psu


def mvp_sensor_probe_ref():
    """Reference solid for SHT30/31 temp/humidity probe hanging through the
    120 deg (Ø10 mm) lid port into headspace + cable to the 180 deg ESP32 bay.
    """
    px3 = p.PORT_RING_RADIUS * math.cos(math.radians(120.0))
    py3 = p.PORT_RING_RADIUS * math.sin(math.radians(120.0))
    probe = Pos(px3, py3, 110.0) * Cylinder(
        3.0, 22.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    cable = _pipe(
        [
            (px3, py3, 131.5),
            (px3, py3, 166.0),
            (-56.0, 34.0, 148.0),
            (-58.0, 14.0, 25.0),
            (-39.0, 10.0, 11.0),
        ],
        1.5,
    )
    return probe + cable


def mvp_cables_ref():
    """Reference solids for 5V power and pump-control wiring harnesses."""
    psu_to_esp = _pipe(
        [(-76.0, -45.0, 12.0), (-62.0, -25.0, 6.0), (-45.0, -12.0, 8.0)],
        1.6,
    )
    esp_to_relay = _pipe(
        [(-39.0, -20.0, 8.0), (-20.0, -35.0, 7.0), (8.0, -37.0, 10.0)],
        1.3,
    )
    relay_to_pump = _pipe(
        [(10.0, -32.0, 9.0), (14.0, -42.0, 10.0), (14.0, -52.0, 14.0)],
        1.4,
    )
    return psu_to_esp + esp_to_relay + relay_to_pump


def mvp_plumbing_ref():
    """Reference solids for bottom drain tube + inline valve (0 deg barb to
    75 deg 10 mL syringe) and air-pump -> Falcon -> 240 deg lid tubing.
    """
    # Bottom drain tube + inline mini ball valve
    syr_x = p.COLL_CRADLE_R * math.cos(math.radians(p.COLL_CRADLE_ANGLE_DEG)) - (
        -48.0 * math.sin(math.radians(p.COLL_CRADLE_ANGLE_DEG))
    )
    syr_y = p.COLL_CRADLE_R * math.sin(math.radians(p.COLL_CRADLE_ANGLE_DEG)) + (
        -48.0 * math.cos(math.radians(p.COLL_CRADLE_ANGLE_DEG))
    )
    drain_tube = _pipe(
        [(64.0, 0.0, 8.2), (76.0, 10.0, 9.5), (74.0, 26.0, 12.0), (syr_x, syr_y, p.COLL_CRADLE_Z)],
        3.2,
    )
    valve_body = Pos(75.0, 18.0, 10.8) * Rot(0, 90, 110) * Cylinder(
        6.0, 20.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    valve_handle = Pos(75.0, 18.0, 17.8) * Rot(0, 0, 20) * Box(
        18.0, 4.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )

    # Air pump -> Falcon cap Port A + internal dip tube (passes cleanly through hole)
    fx = p.FALCON_LOOP_R * math.cos(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    fy = p.FALCON_LOOP_R * math.sin(math.radians(p.FALCON_LOOP_ANGLE_DEG))
    z_cap_top = p.Z_LID_TOP + 4.0
    p_a_x = fx - (p.FALCON_CAP_PORT_SPACING / 2.0)
    p_b_x = fx + (p.FALCON_CAP_PORT_SPACING / 2.0)

    # Pump nozzle tip in world coords (285 deg frame, local (54.0, 37.0, 16.0))
    rad285 = math.radians(p.PUMP_CLIP_ANGLE_DEG)
    nx = p.PUMP_CLIP_R * math.cos(rad285) - 37.0 * math.sin(rad285)
    ny = p.PUMP_CLIP_R * math.sin(rad285) + 37.0 * math.cos(rad285)

    pump_to_falcon = _pipe(
        [
            (nx, ny, p.PUMP_CLIP_Z),
            (nx + 12.0, ny - 12.0, 70.0),
            (p_a_x, fy - 12.0, 185.0),
            (p_a_x, fy, z_cap_top + 4.0),
            (p_a_x, fy, z_cap_top),
            (p_a_x, fy, 70.0),
        ],
        2.6,
    )
    # Falcon cap Port B -> main lid 240 deg humid air inlet (exits cleanly through hole)
    px2 = p.PORT_RING_RADIUS * math.cos(math.radians(240.0))
    py2 = p.PORT_RING_RADIUS * math.sin(math.radians(240.0))
    falcon_to_lid = _pipe(
        [
            (p_b_x, fy, z_cap_top - 4.0),
            (p_b_x, fy, z_cap_top + 8.0),
            (p_b_x, fy, 188.0),
            (10.0, -48.0, 192.0),
            (px2, py2, p.Z_LID_TOP + 12.0),
            (px2, py2, p.Z_LID_TOP - 2.0),
        ],
        2.6,
    )
    return drain_tube + valve_body + valve_handle + pump_to_falcon + falcon_to_lid


def mvp_fit_test_coupon():
    """15-minute 8 mm tall calibration coupon testing all critical tolerances:
      - 90.5 mm ID outer ring (Uxcell tube OD slide-fit)
      - 51.5 mm ID inner ring (ceramic candle drop-through bore)
      - 13.2 mm stem bore, Luer syringe-filter taper, 6.0 mm air bore, 2.8 mm M3 tap
    """
    h = 8.0
    outer_ring = _tube(p.LID_SKIRT_ID / 2.0, p.LID_OD / 2.0, h, 0.0)
    inner_ring = _tube(p.CANDLE_DROP_BORE_DIA / 2.0, (p.CANDLE_DROP_BORE_DIA / 2.0) + 4.0, h, 0.0)
    # 3 wide radial spokes (18 mm wide) bridging outer & inner rings to house test bores
    r_mid = (p.CANDLE_DROP_BORE_DIA / 2.0 + p.LID_SKIRT_ID / 2.0) / 2.0
    spoke_len = (p.LID_SKIRT_ID / 2.0) - (p.CANDLE_DROP_BORE_DIA / 2.0) + 3.0
    coupon = outer_ring + inner_ring
    for deg in (0.0, 120.0, 240.0):
        spoke = Rot(0, 0, deg) * Pos(r_mid, 0, 0) * Box(
            spoke_len, 18.0, h, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        coupon = coupon + spoke

    # Test bore 1 (0 deg): Female Luer Slip socket
    luer_sock = Pos(p.PORT_RING_RADIUS, 0, 0) * Cone(
        p.LUER_BOT_DIA / 2.0, p.LUER_TOP_DIA / 2.0, h + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Test bore 2 (120 deg): 6.0 mm air tubing bore
    px2 = p.PORT_RING_RADIUS * math.cos(math.radians(120.0))
    py2 = p.PORT_RING_RADIUS * math.sin(math.radians(120.0))
    air_hole = Pos(px2, py2, -0.5) * Cylinder(
        p.AIR_PORT_BORE_DIA / 2.0, h + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Test bore 3 (240 deg): 2.8 mm M3 self-tapping hole
    px3 = p.PORT_RING_RADIUS * math.cos(math.radians(240.0))
    py3 = p.PORT_RING_RADIUS * math.sin(math.radians(240.0))
    m3_hole = Pos(px3, py3, -0.5) * Cylinder(
        p.ARDUINO_M3_HOLE_DIA / 2.0, h + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return coupon - luer_sock - air_hole - m3_hole


def mvp_tube_ref():
    """Reference solid for the Uxcell 85 mm ID x 90 mm OD clear tube."""
    return _tube(p.TUBE_ID / 2.0, p.TUBE_OD / 2.0, p.TUBE_LENGTH, p.Z_TUBE_SEAT)


def mvp_candle_ref():
    """Reference solid for the 4-inch ceramic water filter candle (top-loaded)."""
    z_candle_top = p.Z_LID_TOP - p.CANDLE_POCKET_DEPTH
    z_candle_bot = z_candle_top - p.CANDLE_BODY_LEN
    body = Pos(0, 0, z_candle_bot) * Cylinder(
        p.CANDLE_OD / 2.0, p.CANDLE_BODY_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    stem = Pos(0, 0, z_candle_top) * Cylinder(
        p.CANDLE_STEM_DIA / 2.0, 20.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return body + stem


def mvp_syringe_50ml_ref():
    """Reference solid for a 50 mL nutrient-feed medical syringe above the lid."""
    z_tip = p.Z_LID_TOP + 42.1
    tip = Pos(0, 0, z_tip) * Cylinder(2.1, 10.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    barrel = Pos(0, 0, z_tip + 10.0) * Cylinder(15.0, 125.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    flange = Pos(0, 0, z_tip + 135.0) * Cylinder(23.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    plunger = Pos(0, 0, z_tip + 137.5) * Cylinder(7.0, 35.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    thumb = Pos(0, 0, z_tip + 172.0) * Cylinder(14.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return tip + barrel + flange + plunger + thumb


def mvp_syringe_10ml_ref():
    """Reference solid for a 10 mL collection syringe snapped into the base C-clips."""
    # Built along +Y in local frame, tip at -Y (pointing toward 0 deg drain barb)
    tip = Pos(p.COLL_CRADLE_R, -48.0, p.COLL_CRADLE_Z) * Rot(-90, 0, 0) * Cylinder(
        2.1, 9.5, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    barrel = Pos(p.COLL_CRADLE_R, -39.0, p.COLL_CRADLE_Z) * Rot(-90, 0, 0) * Cylinder(
        8.0, 82.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    flange = Pos(p.COLL_CRADLE_R, 43.0, p.COLL_CRADLE_Z) * Rot(-90, 0, 0) * Cylinder(
        15.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    plunger = Pos(p.COLL_CRADLE_R, 45.0, p.COLL_CRADLE_Z) * Rot(-90, 0, 0) * Cylinder(
        4.0, 22.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    thumb = Pos(p.COLL_CRADLE_R, 66.5, p.COLL_CRADLE_Z) * Rot(-90, 0, 0) * Cylinder(
        9.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return Rot(0, 0, p.COLL_CRADLE_ANGLE_DEG) * (tip + barrel + flange + plunger + thumb)
