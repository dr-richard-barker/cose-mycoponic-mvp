#!/usr/bin/env python3
"""
CoSE Mycoponic Chamber — MVP Build & Verification Script
Generates print-ready STLs, editable STEP files, and runs watertightness
and assembly interference checks via trimesh.
"""

import os
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
    ("mvp_top_lid_syringe_tower", parts.mvp_top_lid_syringe_tower),
    ("mvp_top_lid_syringe_cage", parts.mvp_top_lid_syringe_cage),
    ("mvp_syringe_tower_addon", parts.mvp_syringe_tower_addon),
    ("mvp_syringe_tower_addon_half", parts.mvp_syringe_tower_addon_half),
    ("mvp_syringe_cage_addon", parts.mvp_syringe_cage_addon),
    ("mvp_syringe_cage_addon_25ml", parts.mvp_syringe_cage_addon_25ml),
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
]


def main():
    os.makedirs(OUT_STL_DIR, exist_ok=True)
    os.makedirs(OUT_STEP_DIR, exist_ok=True)

    solids = {}
    all_ok = True

    print("=== Building MVP Parts & Exporting STL / STEP ===")
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
        bodies = len(mesh.split(only_watertight=False))
        vol_cm3 = mesh.volume / 1000.0
        ok_mesh = watertight and (bodies == 1)
        status = "OK (watertight)" if ok_mesh else f"FAIL (wt={watertight}, bodies={bodies})"
        if not ok_mesh:
            all_ok = False
        print(f"  {name:24s} | {status:22s} | vol = {vol_cm3:7.2f} cm^3")

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
        ("mvp_top_lid_syringe_tower", "mvp_tube_ref"),
        ("mvp_top_lid_syringe_tower", "mvp_candle_ref"),
        ("mvp_top_lid_syringe_tower", "mvp_candle_collar"),
        ("mvp_top_lid_syringe_cage", "mvp_tube_ref"),
        ("mvp_candle_collar", "mvp_candle_ref"),
        ("mvp_bottom_base", "mvp_tube_ref"),
        ("mvp_bottom_base", "mvp_candle_ref"),
        ("mvp_bottom_base_collection", "mvp_tube_ref"),
        ("mvp_bottom_base_collection", "mvp_candle_ref"),
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

    print(f"\nTube ID/OD: {p.TUBE_ID} / {p.TUBE_OD} mm (L = {p.TUBE_LENGTH:.1f} mm)")
    print(f"Lid skirt ID: {p.LID_SKIRT_ID} mm | Base socket ID: {p.BASE_SOCKET_ID} mm")
    print(f"Candle tip Z: {p.Z_TUBE_TOP - p.CANDLE_BODY_LEN:.1f} mm | Funnel apex Z: {p.FUNNEL_APEX_Z:.1f} mm")

    if not all_ok:
        sys.exit(1)
    print("\nALL CHECKS PASSED.")


if __name__ == "__main__":
    main()
