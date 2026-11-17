# CoSE Mycoponic Chamber (MVP) — Complete Bill of Materials

## 1. Recommended 3D-Printed Parts (PETG, Support-Free)

| # | Part File | Volume | Est. Mass (PETG) | Print Orientation & Notes |
|---|---|---|---|---|
| 1 | `mvp_top_lid.stl` | 48.4 cm³ | ~61 g | Upside-down; 90.5 mm skirt, Ø58.5 mm collar pocket, 3 ports + 3 indents |
| 2 | `mvp_candle_collar.stl` | 10.0 cm³ | ~13 g | Flat; bolts to ceramic candle stem in the open |
| 3 | `mvp_syringe_cage_snap_falcon.stl` | 42.1 cm³ | ~53 g | Upside-down; 1-piece 50 mL net + 3-pin snap base + integrated 2-port Falcon cap |
| 4 | `mvp_bottom_base_collection.stl` | 212.8 cm³ | ~270 g | Upright (5 walls, 100% infill); 38.5° funnel, 20 mm drain, 3 bays, 10 mL clips |
| 5 | `mvp_fit_test_coupon.stl` | 21.2 cm³ | ~27 g | Flat (~15 min test print for tube, candle, Luer, air tube & M3 tolerances) |

*(Optional alternative variants in `out/stl/`: `mvp_top_lid_falcon.stl`, `mvp_syringe_cage_snap.stl`, `mvp_syringe_cage_snap_25ml.stl`, `mvp_syringe_tower_addon.stl`, `mvp_syringe_tower_addon_half.stl`, `mvp_top_lid_syringe_tower.stl`, `mvp_top_lid_syringe_cage.stl`, `mvp_cage_retainer_ring.stl`, `mvp_bottom_base.stl`, `mvp_port_barb_insert.stl`.)*

---

## 2. Chamber, Filtration & Syringes

| # | Component | Specification | Qty | Est. Cost |
|---|---|---|---|---|
| 7 | **Clear Chamber Tube** | Uxcell Rigid Acrylic/PC Pipe, **85 mm ID × 90 mm OD × 100 mm (4")** | 1 | ~$10 |
| 8 | **Ceramic Filter Candle** | AquaEasy **4-inch Ceramic Water Filter Candle** (~50 mm OD, 1/4" BSP stem + washer + wing nut) | 1 | ~$8 |
| 9 | **Syringe Filter** | **0.22 µm PTFE/PVDF Syringe Filter** (25/33 mm, Male Luer Slip) → 0° lid port | 1 | ~$2 |
| 10 | **Nutrient Feed Syringe** | **50 mL Medical Syringe** (Luer tip) → top 3-strut cage | 1 | ~$1 |
| 11 | **Collection Syringe** | **10 mL Medical Syringe** (~16 mm OD barrel) → 75° base C-clips | 1 | ~$0.50 |
| 12 | **Humidifier Bubbler Tube** | **50 mL Conical Centrifuge (Falcon) Tube** (~29.6 mm OD) → 300° loop | 1 | ~$0.50 |

---

## 3. Fluidics & Pneumatics

| # | Component | Specification | Qty | Est. Cost |
|---|---|---|---|---|
| 13 | **Inline Drain Valve** | **1/4" (6 mm) Inline Mini Ball Valve** or **Luer Stopcock** | 1 | ~$3 |
| 14 | **Drain Tubing** | **1/4" ID (6 mm ID)** silicone tubing (~0.3 m, 0° drain barb → valve → 10 mL syringe) | 1 | ~$1 |
| 15 | **Air Pump & Humidifier Tubing** | **6 mm OD / 4 mm ID** silicone/PU air tubing (~1.0 m, pump → Falcon cap → 240° lid port) | 1 | ~$2 |

---

## 4. Electronics, Sensor & Power

| # | Component | Specification | Qty | Est. Cost |
|---|---|---|---|---|
| 16 | **Microcontroller** | **ESP32 DevKit** (mounted in 180° base bay; runs `esp32_humid_controller.ino`) | 1 | ~$6 |
| 17 | **Temp/Humidity Sensor** | **SHT30 / SHT31 Waterproof I²C Probe** (hung through 120° Ø10 mm port) | 1 | ~$7 |
| 18 | **Pump Driver** | **5V Relay Module** or **Logic-Level MOSFET (IRLZ44N + 1N4007 flyback diode)** (285° bay) | 1 | ~$2 |
| 19 | **Mini Air Pump** | **5V DC Diaphragm Air Pump** (6 mm outlet barb) | 1 | ~$6 |
| 20 | **Power Supply** | **5V 2A USB-C / DC Power Supply** | 1 | ~$6 |
| 21 | **Hardware & Wiring** | **M3 × 8 mm screws** (8×), **Jumper wires**, **Silicone sealant / PTFE tape** | 1 set | ~$2 |

**Estimated Total Prototype Cost:** **~$57** (excluding PETG filament, ~430 g / ~$9).
