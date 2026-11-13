# CoSE Mycoponic Chamber — Minimal Viable Prototype (MVP)

A cheap, pragmatic, 3D-printable single-chamber prototype built around off-the-shelf components:
- **Uxcell Clear Acrylic/Polycarbonate Tube** (`85 mm ID × 90 mm OD`)
- **AquaEasy 4-inch Ceramic Water Filter Candle** (`~50 mm OD × 100 mm`, top-hung)
- **Standard 0.22 µm Syringe Filter** (Luer-slip gas exchange)
- **External Humid Air Pump** (`6 mm OD / 4 mm ID` tubing port) + **Temp/RH Sensor** (`8 mm` pass-through)
- **Side-Exit Drain Barb** (`1/4"` tubing to small inline valve)

## 3D Printing Guide (Support-Free)

| File | Orientation | Material | Walls / Infill | Supports |
|---|---|---|---|---|
| `out/stl/mvp_fit_test_coupon.stl` | **Flat** (~15 min print first!) | PETG | 3 walls, 20% infill | **None** |
| `out/stl/mvp_top_lid.stl` | **Upside-down** (flat top on bed) | PETG | 4 walls, 25% gyroid | **None** |
| `out/stl/mvp_syringe_tower_addon.stl` | **Upside-down** (top ring on bed; plugs into `mvp_top_lid`) | PETG | 4 walls, 25% gyroid | **None** |
| `out/stl/mvp_top_lid_syringe_tower.stl` | **Upright** (optional 1-piece version) | PETG | 4 walls, 25% gyroid | Touching buildplate (under roof) |
| `out/stl/mvp_candle_collar.stl` | **Flat** | PETG | 4 walls, 100% infill | **None** |
| `out/stl/mvp_bottom_base.stl` | **Upright** (wide foot on bed) | PETG | **5 walls, 100% infill** (watertight) | **None** |
| `out/stl/mvp_port_barb_insert.stl` | **Upright** (optional) | PETG | 3 walls, 100% infill | **None** |

## Assembly
1. **Top-Loading Ceramic Candle:** Pass the ceramic candle's threaded stem through `mvp_candle_collar` (`Ø13.2 mm` hole) with its silicone sealing washer and hand-tighten the wing nut. Drop the candle + collar straight down into the stepped `Ø58.5 mm` pocket on top of `mvp_top_lid`—the `Ø58.0 mm` collar seats on the shoulder so the candle cannot fall through. Feed nutrient/water into the hollow stem from the top.
2. **Lid Ports:**
   - Press a **0.22 µm syringe filter** (Male Luer Slip tip) into the `0°` tapered Luer socket.
   - Push **6 mm OD air pump tubing** into the `120°` air inlet bore (or press in `mvp_port_barb_insert` for soft 4 mm ID tubing).
   - Drop your **temp/humidity sensor** through the `240°` `8 mm` bore and seal around the cable with putty or a split grommet.
3. **Tube + Base:** Push the `90 mm OD` clear tube into the `mvp_bottom_base` socket. Attach a short piece of `1/4" ID` silicone tubing + mini ball valve to the side drain barb.
4. **Close:** Slide `mvp_top_lid` onto the top of the clear tube.

## Regenerating CAD
```bash
CMBS-MVP-Prototype/.venv/bin/python CMBS-MVP-Prototype/build_mvp.py
```
