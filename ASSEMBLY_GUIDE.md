# CoSE Mycoponic Chamber (MVP) — Complete Print, Assembly & Software Guide

This tutorial covers the complete build for the **Double-Funnel + Pegged Lid + Collection Base** configuration, using your ordered electronics and hardware.

> **Total Estimated Time**
> - **3D Printing (unattended):** ~14–16 hours (PETG)
> - **Hands-On Mechanical & Fluidic Assembly:** ~35 minutes
> - **Electronics Soldering & Mounting:** ~45 minutes (+30 min tack-free / 24 hr full cure for conformal coating)
> - **Software Setup & ESP32 Flashing:** ~20–30 minutes

---

## 0. Complete Parts & Tools Checklist (~10 min)

### A. 3D-Printed Parts (PETG, Support-Free)
| File | Role | Vol | Print Orientation |
| :--- | :--- | :---: | :--- |
| `mvp_bottom_base_collection.stl` | Bottom Base (`10 mL` Syringe Holder + `285°` Pump Clips + `8.5°` Drain) | 215.7 cm³ | Upright (`Z = 0` circular foot on bed) |
| `mvp_top_lid_pegs.stl` | Top Lid with `3×` Upward Alignment Pegs (`Ø13.8 mm`) | 52.1 cm³ | Flat (`Z_LID_TOP` up, skirt down — or flip 180° for zero internal bridging) |
| `mvp_syringe_cage_snap_falcon_funnel.stl` | Double-Funnel Net + `300°` Downward Falcon Cap | 42.0 cm³ | Upright (`Z = Z_LID_TOP` flat base & Falcon skirt rim on bed) |
| `mvp_candle_collar.stl` | Candle Drop-In Collar (`Ø58 mm` flange) | 10.0 cm³ | Flat on bed |
| `mvp_fit_test_coupon.stl` *(optional)* | 15-min calibration check for tube, candle, Luer, air tube & M3 tap | 21.2 cm³ | Flat on bed |

### B. Chamber & Fluidics (Off-the-Shelf)
- Clear Acrylic/PC Tube (`85 mm ID × 90 mm OD × 100 mm` / 4")
- 4-inch Ceramic Filter Candle (`~50 mm OD`, `1/4"` BSP stem + rubber washer + wing nut)
- `0.22 µm` PTFE/PVDF Syringe Filter (Male Luer Slip)
- `50 mL` Nutrient Feed Syringe (Luer-Lock or Luer-Slip)
- `50 mL` Falcon Tube (standard conical centrifuge tube with `Ø30 mm` neck)
- `10 mL` Collection Syringe (`~16 mm` barrel OD)
- `1/4"` ID Silicone Drain Tubing (`~0.3 m`) + `1/4"` Inline Mini Ball Valve
- `6 mm` OD Flexible Air Tubing (`~1.0 m`)

### C. Ordered Electronics & Hardware
| Component | Purpose | Link |
| :--- | :--- | :--- |
| **ESP32-WROOM-32 DevKit (30-Pin)** | Microcontroller (I2C sensor read + GPIO 25 pump PWM/relay logic) | [Amazon B0718T232Z](https://www.amazon.com/dp/B0718T232Z) |
| **SHT30 Waterproof I2C Probe** | IP67 Temp/RH sensor (`3.3V`, address `0x44`, hung through `120°` lid port) | [Amazon B081JR1WQ7](https://www.amazon.com/dp/B081JR1WQ7) |
| **5V DC Diaphragm Mini Air Pump** | `Ø27×55 mm`, `4–6 mm` barbs (snaps into `285°` base clips) | [Amazon B074N2DCHW](https://www.amazon.com/dp/B074N2DCHW) |
| **IRLZ44N Logic-Level N-MOSFET** | TO-220 low-side switch driven by ESP32 `3.3V` GPIO 25 | [Amazon B08M441HDN](https://www.amazon.com/dp/B08M441HDN) |
| **1/4W Metal Film Resistors** | `220 Ω` (Gate current-limit) + `10 kΩ` (Gate pull-down to GND) | [Amazon B07QXP4KVZ](https://www.amazon.com/dp/B07QXP4KVZ) |
| **1N4007 Rectifier Diode (1A 1000V)** | Inductive flyback protection across pump terminals | [Amazon B07Q6J9TNW](https://www.amazon.com/dp/B07Q6J9TNW) |
| **5V 2A DC PSU + Screw Terminal** | `5.5×2.1 mm` barrel adapter powering both ESP32 (`VIN`) and pump | [Amazon B0BVHT4CB4](https://www.amazon.com/dp/B0BVHT4CB4) |
| **22 AWG Silicone Hook-Up Wire** | Flexible multi-color leads for power, I2C, and MOSFET driver | [Amazon B07G72D85H](https://www.amazon.com/dp/B07G72D85H) |
| **MG Chemicals 422B Conformal Coating** | Brush-on silicone moisture barrier for exposed electronics/solder | [Amazon B008O9YIV6](https://www.amazon.com/dp/B008O9YIV6) |
| **M3 Stainless 304 Screws/Nuts/Washers** | Mounting hardware for ESP32 (`180°` bay) & wire strain relief | [Amazon B0812TYT5L](https://www.amazon.com/dp/B0812TYT5L) |

### D. Tools Needed
- Soldering iron + lead-free/rosin-core solder + heat-shrink tubing (or electrical tape)
- Wire strippers / flush cutters + small Phillips/hex screwdriver
- Micro-USB data cable (must support **data**, not charge-only) + Windows/macOS/Linux computer
- Optional: PTFE plumber's tape (for ceramic candle `1/4"` BSP threads)

---

## Phase 1: 3D Printing & Prep (~14–16 hr print, ~20 min prep)

1. **Recommended Slicer Settings (PETG):**
   - **Material:** PETG (water-resistant, chemically inert, slight flex for snap-in C-clips)
   - **Nozzle / Layer Height:** `0.4 mm` nozzle, `0.20 mm` layer height
   - **Walls & Infill:** `4` perimeters (`1.6 mm` wall), `5` top/bottom layers, `25–35%` gyroid infill
   - **Supports:** **None required** (all parts use `<= 45°` chamfers/gussets). *Tip: you may enable a `5 mm` brim on `mvp_syringe_cage_snap_falcon_funnel.stl` if bed adhesion is light, and optionally print `mvp_top_lid_pegs.stl` upright with touching-buildplate support only if your printer struggles with the `Ø90.5 mm` ceiling bridge.*
2. **Optional Fit Check (~15 min):** Print `mvp_fit_test_coupon.stl` first to verify your printer's tolerances against the acrylic tube (`90.5 mm` socket), candle stem, Luer filter, `6 mm` air tube, and `M3` self-tapping holes.
3. **Post-Processing:**
   - Remove any brim or stringing from the `3×` `Ø14.2 mm` wing holes on `mvp_syringe_cage_snap_falcon_funnel.stl`, the `Ø13.8 mm` pegs on `mvp_top_lid_pegs.stl`, and the `Ø4.5 mm` sloped drain bore on `mvp_bottom_base_collection.stl`.
   - Test-thread the `50 mL` Falcon tube into the `300°` downward cap and the ceramic candle `1/4"` BSP stem into the bottom of the double-funnel boss.

---

## Phase 2: Mechanical & Chamber Assembly (~20 min)

1. **Mount the Ceramic Filter Candle:**
   - Slide the rubber washer onto the ceramic candle's `1/4"` BSP threaded stem.
   - Insert the stem up through `mvp_candle_collar.stl` (`Ø58 mm` flange) and secure with the candle's wing nut (hand-tight + 1/4 turn).
   - Wrap 2–3 turns of PTFE tape around the exposed top threads of the candle stem.
2. **Seat the Candle & Double-Funnel on the Top Lid:**
   - Drop the `mvp_candle_collar` + candle assembly into the central pocket on `mvp_top_lid_pegs.stl` so the collar rests flush and the threaded stem protrudes upward through the `Ø20 mm` center hole.
   - Align the `3×` `Ø14.2 mm` wing holes of `mvp_syringe_cage_snap_falcon_funnel.stl` over the `3×` upward pegs (`60° / 180° / 300°`) on `mvp_top_lid_pegs.stl`, and screw the internal `1/4"` BSP boss of the double-funnel down onto the candle stem until the wings sit flush on the lid top.
3. **Install Gas-Exchange Filter & Syringes (Top):**
   - Press the `0.22 µm` Male Luer-Slip syringe filter into the `0°` lid port.
   - Fill (or leave ready) the `50 mL` nutrient feed syringe, drop it into the 3-strut cage on top of the double-funnel, and seat its tip into the top Female Luer-Lock socket.
   - Screw a `50 mL` Falcon tube (filled ~1/3 with sterile DI water) upward into the `300°` downward-facing threaded cap.
4. **Assemble Chamber Tube & Base:**
   - Seat the `85×90×100 mm` clear acrylic tube firmly into the `Ø90.5 mm` socket of `mvp_bottom_base_collection.stl`.
   - Lower the `mvp_top_lid_pegs` + candle assembly onto the top rim of the acrylic tube (the candle hangs centered inside the tube without touching the walls or funnel).
   - Snap the `10 mL` collection syringe into the twin `75°` C-clips on the base.

---

## Phase 3: Plumbing & Fluidics (~10 min)

1. **Drain Line (`0°` Sloped Base Barb → `75°` Collection Syringe):**
   - Push one end of the `1/4"` ID silicone tubing all the way onto the `8.5°` downward-sloped drain barb (`16 mm` full push-on depth over both retention cones).
   - Cut to ~`12–15 cm`, insert the `1/4"` inline mini ball valve mid-line, and route the outlet to the `10 mL` collection syringe (or waste flask). Keep the valve **closed** during normal humidification/wicking and open it periodically to harvest leachate.
2. **Humidified Air Loop (`285°` Pump → `300°` Falcon Bubbler → `240°` Lid Port):**
   - Snap the `5V` mini air pump (`Ø27×55 mm`) into the `285°` C-clips on the base.
   - Connect a length of `6 mm` OD air tubing from the pump's **outlet** barb up to **Port A** of the `300°` Falcon cap, pushing an internal dip-tube section down through the port so it submerges below the water line in the `50 mL` Falcon tube.
   - Connect a second piece of `6 mm` OD air tubing from **Port B** of the `300°` Falcon cap (headspace above water) into the `240°` humid air inlet port on `mvp_top_lid_pegs.stl`.

---

## Phase 4: Electronics Wiring & Conformal Coating (~45 min + cure)

### A. Circuit Schematic (Low-Side IRLZ44N MOSFET Pump Driver + SHT30 I2C)

```text
  5V 2A PSU (+5V) ──┬──────────────────────────► ESP32 VIN (5V)
                    │
                    ├──► Pump (+) Red Wire
                    │         │
                    │    [1N4007 Diode]  (Cathode stripe toward +5V!)
                    │         │
                    └──► Pump (─) Black ──► IRLZ44N DRAIN (Pin 2 / Middle)
                                                 │
  ESP32 GPIO 25 ──[220 Ω]──┬──► IRLZ44N GATE (Pin 1 / Left)
                           │
                        [10 kΩ]
                           │
  5V 2A PSU (GND) ──┬──────┴──► IRLZ44N SOURCE (Pin 3 / Right)
                    │
                    └─────────► ESP32 GND

  SHT30 Probe (4 wires):
    VCC (Red)   ──► ESP32 3.3V
    GND (Black) ──► ESP32 GND
    SDA (Yellow/Blue) ──► ESP32 GPIO 21
    SCL (Green/White) ──► ESP32 GPIO 22
```

> [!CAUTION]
> **Check `1N4007` Diode Polarity:** The silver/grey band (**cathode**) on the `1N4007` diode MUST connect to **`+5V`** (Pump `+`), and the unbanded end (**anode**) connects to the **MOSFET Drain** (Pump `-`). Reversing it will short the `5V` supply when the pump turns on.
>
> **Check SHT30 Voltage:** Connect the SHT30 probe's `VCC` to **`3.3V`** on the ESP32, **not** `5V`, and verify your probe's wire color legend (typically Red=`VCC`, Black=`GND`, Yellow=`SDA`, Green=`SCL`, though check the seller's sticker/listing).

### B. Step-by-Step Wiring & Mounting
1. **Solder the MOSFET Driver Harness (using `22 AWG` silicone wire):**
   - Looking at the **IRLZ44N** with the printed face toward you and legs pointing down: **Pin 1 (Left) = Gate**, **Pin 2 (Middle) = Drain**, **Pin 3 (Right) = Source**.
   - Solder the `10 kΩ` pull-down resistor directly between **Gate (Pin 1)** and **Source (Pin 3)**.
   - Solder one side of the `220 Ω` resistor to **Gate (Pin 1)** and a `~10 cm` signal wire from the other side to **ESP32 GPIO 25**.
   - Solder the `1N4007` flyback diode across the pump wires (or between a `+5V` splice and **Drain Pin 2**), with the **stripe toward `+5V`**.
   - Connect **Pump `-`** to **Drain (Pin 2)**, **Pump `+`** to the `5.5×2.1 mm` screw terminal **`+`**, **Source (Pin 3)** to the screw terminal **`-` (GND)**, and run `+5V` / `GND` leads to **ESP32 `VIN`** and **`GND`**.
   - Insulate all exposed leads and resistors with heat-shrink tubing.
2. **Route the SHT30 Sensor Probe:**
   - Feed the SHT30 probe tip down through the `10 mm` sensor port (`120°`) in `mvp_top_lid_pegs.stl` so the sintered IP67 mesh hangs cleanly inside the chamber airspace (without touching the wet ceramic candle). Seal around the cable grommet if desired.
   - Connect the 4 probe wires to ESP32 **`3.3V`**, **`GND`**, **`GPIO 21` (SDA)**, and **`GPIO 22` (SCL)**.
3. **Apply Conformal Coating (MG Chemicals 422B):**
   - Brush a thin coat of **MG Chemicals 422B** over all exposed solder joints, resistor/diode leads, and the top/bottom of the ESP32 PCB **except** the Micro-USB port, `EN`/`BOOT` buttons, and pin headers you still need to plug into.
   - *Never* coat the sintered tip of the SHT30 probe!
   - Let dry **~30 minutes** until tack-free (full moisture-barrier cure takes **24 hours** at room temperature).
4. **Mount in Base Bays:**
   - Mount the ESP32-WROOM-32 DevKit in the `180°` arched bay of `mvp_bottom_base_collection.stl` using **`M3×8 mm`** stainless screws (self-tapping into the `Ø2.8 mm` floor holes) and washers/nuts as needed, and tuck the MOSFET harness neatly into the bay.

---

## Phase 5: Software Installation & Firmware Flashing (~20–30 min)

1. **Install Arduino IDE 2.x (~5 min):**
   - Download and install **Arduino IDE 2.x** from [arduino.cc/en/software](https://www.arduino.cc/en/software).
2. **Add ESP32 Board Support (~10 min):**
   - Open Arduino IDE → **Settings / Preferences** (`Ctrl+,` on Windows/Linux, `Cmd+,` on macOS).
   - In **Additional boards manager URLs**, paste:
     ```text
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Open **Tools → Board → Boards Manager**, search **`esp32`**, and install **`esp32 by Espressif Systems`** (latest 2.x or 3.x).
3. **Install the SHT30/SHT31 Library (~2 min):**
   - Open **Tools → Manage Libraries** (Library Manager), search **`Adafruit SHT31`**, and click **Install** (click **Install all** when prompted for `Adafruit BusIO`).
4. **USB-UART Driver Check (~3 min, if port does not appear):**
   - Plug the ESP32 into your computer with a **data-capable** Micro-USB cable.
   - If no COM / `/dev/cu.*` port appears under **Tools → Port**, install the **Silicon Labs CP210x** (or **CH340**) USB-to-UART VCP driver for your OS and replug the cable.
5. **Open & Flash the Firmware (~5 min):**
   - Open `CMBS-MVP-Prototype/firmware/esp32_humid_controller/esp32_humid_controller.ino` in Arduino IDE.
   - Select **Tools → Board → esp32 → DOIT ESP32 DEVKIT V1** (or `ESP32 Dev Module`).
   - Select your ESP32's port under **Tools → Port**.
   - Click **Upload (`→`)**. *(If the IDE hangs on `Connecting........`, hold the **`BOOT`** button on the ESP32 until `Writing at 0x...` begins, then release.)*
6. **Verify Live Telemetry:**
   - Open **Tools → Serial Monitor** and set the baud rate to **`115200`**.
   - You should see readings every 2 seconds:
     ```text
     T=22.40 C | RH=64.2% | Pump=ON
     ```
   - *(Optional)* Adjust `RH_TARGET_LOW` (`85.0f`), `RH_TARGET_HIGH` (`90.0f`), or `MAX_PUMP_ON_MS` (`120000`) at the top of the `.ino` file for your mushroom species.

---

## Phase 6: Leak Test & Commissioning (~15 min)

1. **Dry Electronics Check:** Unplug USB, plug the `5V 2A` PSU into the `5.5×2.1 mm` screw terminal adapter, and confirm the pump turns **ON** when ambient RH is below `85%` (or stops if you breathe gently near the SHT30 probe to push RH above `90%`).
2. **Wet Seal Check:** Fill the `50 mL` Falcon tube ~1/3 with water, screw it into the `300°` cap, and verify bubbles rise cleanly without air leaks around the cap or tubing.
3. **Nutrient Feed Check:** Close the `1/4"` drain ball valve, load sterile water/nutrient into the `50 mL` top syringe, and verify slow weeping through the ceramic candle into the chamber.

### Quick Troubleshooting
- **`ERROR: SHT31/SHT30 not found at 0x44`:** Swap `SDA` (`GPIO 21`) and `SCL` (`GPIO 22`), verify `3.3V` power on the probe, or check if your probe uses alternate I2C address `0x45` (`sht31.begin(0x45)`).
- **Pump hums or doesn't spin:** Confirm the `5V 2A` PSU is connected (USB alone may brown out under pump startup current) and check common `GND` between PSU `-`, MOSFET Source, and ESP32 `GND`.
- **Upload fails (`Failed to connect to ESP32`):** Use a known data Micro-USB cable and hold **`BOOT`** during `Connecting...`.
