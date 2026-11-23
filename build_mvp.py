#!/usr/bin/env python3
"""
CoSE Mycoponic Chamber — MVP Build & Verification Script
Generates print-ready STLs, editable STEP files, and runs watertightness
and assembly interference checks via trimesh.
"""

import os
import shutil
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import trimesh
from build123d import Compound, Pos, export_step, export_stl
from OCP.BRepTools import BRepTools

import mvp_params as p
import mvp_parts as parts

OUT_STL_DIR = os.path.join(CURRENT_DIR, "out", "stl")
OUT_STEP_DIR = os.path.join(CURRENT_DIR, "out", "step")

PRINT_PARTS = [
    ("mvp_top_lid", parts.mvp_top_lid),
    ("mvp_top_lid_pegs", parts.mvp_top_lid_pegs),
    ("mvp_top_lid_falcon", parts.mvp_top_lid_falcon),
    ("mvp_falcon_cap_2port", parts.mvp_falcon_cap_2port),
    ("mvp_top_lid_syringe_tower", parts.mvp_top_lid_syringe_tower),
    ("mvp_top_lid_syringe_cage", parts.mvp_top_lid_syringe_cage),
    ("mvp_syringe_tower_addon", parts.mvp_syringe_tower_addon),
    ("mvp_syringe_tower_addon_half", parts.mvp_syringe_tower_addon_half),
    ("mvp_syringe_cage_addon", parts.mvp_syringe_cage_addon),
    ("mvp_syringe_cage_addon_25ml", parts.mvp_syringe_cage_addon_25ml),
    ("mvp_cage_retainer_ring", parts.mvp_cage_retainer_ring),
    ("mvp_syringe_cage_snap", parts.mvp_syringe_cage_snap),
    ("mvp_syringe_cage_snap_25ml", parts.mvp_syringe_cage_snap_25ml),
    ("mvp_syringe_cage_snap_falcon", parts.mvp_syringe_cage_snap_falcon),
    ("mvp_syringe_cage_snap_falcon_funnel", parts.mvp_syringe_cage_snap_falcon_funnel),
    ("mvp_luer_stopcock_body", parts.mvp_luer_stopcock_body),
    ("mvp_luer_stopcock_plug", parts.mvp_luer_stopcock_plug),
    ("mvp_snap_pin", parts.mvp_snap_pin),
    ("mvp_candle_collar", parts.mvp_candle_collar),
    ("mvp_bottom_base", parts.mvp_bottom_base),
    ("mvp_bottom_base_collection", parts.mvp_bottom_base_collection),
    ("mvp_port_barb_insert", parts.mvp_port_barb_insert),
    ("mvp_fit_test_coupon", parts.mvp_fit_test_coupon),
]

REF_PARTS = [
    ("mvp_tube_ref", parts.mvp_tube_ref),
    ("mvp_candle_ref", parts.mvp_candle_ref),
    ("mvp_syringe_50ml_ref", parts.mvp_syringe_50ml_ref),
    ("mvp_syringe_10ml_ref", parts.mvp_syringe_10ml_ref),
    ("mvp_falcon_50ml_ref", parts.mvp_falcon_50ml_ref),
    ("mvp_electronics_ref", parts.mvp_electronics_ref),
    ("mvp_sensor_probe_ref", parts.mvp_sensor_probe_ref),
    ("mvp_cables_ref", parts.mvp_cables_ref),
    ("mvp_plumbing_ref", parts.mvp_plumbing_ref),
]


def main():
    os.makedirs(OUT_STL_DIR, exist_ok=True)
    os.makedirs(OUT_STEP_DIR, exist_ok=True)

    solids = {}
    all_ok = True

    print("=== Building MVP Parts & Exporting STL / STEP ===")
    print_names = {n for n, _ in PRINT_PARTS}
    for name, builder in PRINT_PARTS + REF_PARTS:
        shape = builder()
        solids[name] = shape

        BRepTools.Clean_s(shape.wrapped)
        stl_path = os.path.join(OUT_STL_DIR, f"{name}.stl")
        step_path = os.path.join(OUT_STEP_DIR, f"{name}.step")

        export_stl(shape, stl_path, tolerance=0.05, angular_tolerance=0.2)
        export_step(shape, step_path)

        mesh = trimesh.load(stl_path, force="mesh")
        watertight = mesh.is_watertight
        bodies = len(shape.solids())
        vol_cm3 = mesh.volume / 1000.0
        ok_mesh = watertight and (bodies == 1 if name in print_names else bodies >= 1)
        status = "OK (watertight)" if ok_mesh else f"FAIL (wt={watertight}, bodies={bodies})"
        if not ok_mesh:
            all_ok = False
        print(f"  {name:24s} | {status:22s} | vol = {vol_cm3:7.2f} cm^3")

    # Sync pre-oriented Revopoint 3D scan asset (AstroMycology legacy Tube01_Raw_Mesh.ply)
    scan_src = os.path.join(CURRENT_DIR, "assets", "mvp_mycoponics_tube_scan_ref.stl")
    if os.path.exists(scan_src):
        scan_dst = os.path.join(OUT_STL_DIR, "mvp_mycoponics_tube_scan_ref.stl")
        shutil.copy2(scan_src, scan_dst)
        scan_mesh = trimesh.load(scan_dst, force="mesh")
        scan_r_max = float(((scan_mesh.vertices[:, 0] ** 2 + scan_mesh.vertices[:, 1] ** 2) ** 0.5).max())
        scan_z_min, scan_z_max = float(scan_mesh.bounds[0][2]), float(scan_mesh.bounds[1][2])
        scan_ok = scan_r_max < (p.TUBE_ID / 2.0) and scan_z_min > p.FUNNEL_APEX_Z and scan_z_max < p.Z_TUBE_TOP
        if not scan_ok:
            all_ok = False
        print(f"  {'mvp_mycoponics_tube_scan_ref':24s} | {'OK (3D scan ref)' if scan_ok else 'FAIL (bounds)':22s} | r_max={scan_r_max:.2f} mm, Z=[{scan_z_min:.1f}, {scan_z_max:.1f}]")

    # Export full reference assembly STEP
    asm = Compound(children=list(solids.values()))
    asm_step = os.path.join(OUT_STEP_DIR, "mvp_full_assembly.step")
    export_step(asm, asm_step)

    # Geometric interference checks on assembled solids
    print("\n=== Assembly Interference Checks ===")
    pairs = [
        ("mvp_top_lid", "mvp_tube_ref"),
        ("mvp_top_lid", "mvp_candle_ref"),
        ("mvp_top_lid", "mvp_candle_collar"),
        ("mvp_top_lid", "mvp_syringe_cage_addon"),
        ("mvp_candle_collar", "mvp_syringe_cage_addon"),
        ("mvp_top_lid", "mvp_syringe_cage_addon_25ml"),
        ("mvp_candle_collar", "mvp_syringe_cage_addon_25ml"),
        ("mvp_top_lid", "mvp_cage_retainer_ring"),
        ("mvp_syringe_cage_addon", "mvp_cage_retainer_ring"),
        ("mvp_syringe_cage_addon_25ml", "mvp_cage_retainer_ring"),
        ("mvp_top_lid", "mvp_syringe_cage_snap"),
        ("mvp_candle_collar", "mvp_syringe_cage_snap"),
        ("mvp_top_lid", "mvp_syringe_cage_snap_25ml"),
        ("mvp_candle_collar", "mvp_syringe_cage_snap_25ml"),
        ("mvp_top_lid", "mvp_syringe_cage_snap_falcon"),
        ("mvp_candle_collar", "mvp_syringe_cage_snap_falcon"),
        ("mvp_top_lid", "mvp_syringe_cage_snap_falcon_funnel"),
        ("mvp_top_lid_pegs", "mvp_tube_ref"),
        ("mvp_top_lid_pegs", "mvp_candle_ref"),
        ("mvp_top_lid_pegs", "mvp_candle_collar"),
        ("mvp_top_lid_pegs", "mvp_syringe_cage_snap_falcon_funnel"),
        ("mvp_luer_stopcock_body", "mvp_syringe_cage_snap_falcon_funnel"),
        ("mvp_luer_stopcock_body", "mvp_luer_stopcock_plug"),
        ("mvp_candle_collar", "mvp_syringe_cage_snap_falcon_funnel"),
        ("mvp_top_lid_syringe_tower", "mvp_tube_ref"),
        ("mvp_top_lid_syringe_tower", "mvp_candle_ref"),
        ("mvp_top_lid_syringe_tower", "mvp_candle_collar"),
        ("mvp_top_lid_syringe_cage", "mvp_tube_ref"),
        ("mvp_top_lid_falcon", "mvp_tube_ref"),
        ("mvp_top_lid_falcon", "mvp_falcon_50ml_ref"),
        ("mvp_falcon_cap_2port", "mvp_falcon_50ml_ref"),
        ("mvp_top_lid_falcon", "mvp_falcon_cap_2port"),
        ("mvp_candle_collar", "mvp_candle_ref"),
        ("mvp_bottom_base", "mvp_tube_ref"),
        ("mvp_bottom_base", "mvp_candle_ref"),
        ("mvp_bottom_base", "mvp_electronics_ref"),
        ("mvp_bottom_base_collection", "mvp_tube_ref"),
        ("mvp_bottom_base_collection", "mvp_candle_ref"),
        ("mvp_bottom_base_collection", "mvp_electronics_ref"),
        ("mvp_bottom_base_collection", "mvp_syringe_10ml_ref"),
        ("mvp_syringe_10ml_ref", "mvp_tube_ref"),
        ("mvp_syringe_10ml_ref", "mvp_top_lid_pegs"),
        ("mvp_tube_ref", "mvp_candle_ref"),
    ]
    for a, b in pairs:
        inter = solids[a] & solids[b]
        vol = inter.volume if inter else 0.0
        ok = vol < 1e-3
        if not ok:
            all_ok = False
        print(f"  {a:18s} <-> {b:16s} | overlap = {vol:8.4f} mm^3 | {'PASS' if ok else 'FAIL'}")

    # Check syringe cage lid with candle seated under Z_TUBE_TOP (stem-mounted)
    candle_under_lid = Pos(0, 0, -(p.ROOF_THICKNESS - p.CANDLE_POCKET_DEPTH)) * solids["mvp_candle_ref"]
    cage_inter = solids["mvp_top_lid_syringe_cage"] & candle_under_lid
    cage_vol = cage_inter.volume if cage_inter else 0.0
    if cage_vol >= 1e-3:
        all_ok = False
    print(f"  {'mvp_top_lid_syringe_cage':18s} <-> {'candle_under_lid':16s} | overlap = {cage_vol:8.4f} mm^3 | {'PASS' if cage_vol < 1e-3 else 'FAIL'}")

    # Check merged Snap-On Net + Falcon Cap with Falcon tube seated inside (10 mm lower than loop-mounted)
    falcon_in_merged = Pos(0, 0, -10.5) * solids["mvp_falcon_50ml_ref"]
    fm_inter = solids["mvp_syringe_cage_snap_falcon"] & falcon_in_merged
    fm_vol = fm_inter.volume if fm_inter else 0.0
    if fm_vol >= 1e-3:
        all_ok = False
    print(f"  {'mvp_syringe_cage_snap_falcon':18s} <-> {'falcon_in_merged':16s} | overlap = {fm_vol:8.4f} mm^3 | {'PASS' if fm_vol < 1e-3 else 'FAIL'}")

    print(f"\nTube ID/OD: {p.TUBE_ID} / {p.TUBE_OD} mm (L = {p.TUBE_LENGTH:.1f} mm)")
    print(f"Lid skirt ID: {p.LID_SKIRT_ID} mm | Base socket ID: {p.BASE_SOCKET_ID} mm")
    print(f"Candle tip Z: {p.Z_TUBE_TOP - p.CANDLE_BODY_LEN:.1f} mm | Funnel apex Z: {p.FUNNEL_APEX_Z:.1f} mm")

    if not all_ok:
        sys.exit(1)
    print("\nALL CHECKS PASSED.")


if __name__ == "__main__":
    main()
