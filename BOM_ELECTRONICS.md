# CoSE Mycoponic MVP — Electronics, Sensor & Pump BOM

## 1. Parts List (Sized for CAD Bays, `Ø27.4 mm` Pump Clips & `Ø10 mm` Lid Port)

| # | Component | Exact Spec / Form Factor | Fit / CAD Location | Qty | Est. Cost | Buy Link |
|---|---|---|---|---|---|---|
| 1 | **Microcontroller** | **ESP32-WROOM-32 DevKit** (`~28 × 52 mm`, 30/38-pin, USB-C/Micro-USB) | `180°` arched base bay (`M3` holes) | 1 | ~$6.00 | [Amazon](https://www.amazon.com/s?k=ESP32+DevKit+WROOM-32) |
| 2 | **Temp / Humidity Sensor** | **SHT30 / SHT31 Waterproof I²C Probe** (IP67 sintered mesh tip `Ø6 mm`, 1 m 4-wire cable, `3.3V`, addr `0x44`) | Drops through `120°` `Ø10.0 mm` lid port into headspace | 1 | ~$7.00 | [Amazon](https://www.amazon.com/s?k=SHT30+waterproof+I2C+temperature+humidity+sensor+probe) |
| 3 | **Mini Air Pump** | **5V DC Diaphragm Air Pump** (`Ø27 × 55 mm` motor/pump body, `4–6 mm` outlet barb, `~1.5–2.0 L/min`, `< 400 mA`) | Snaps into `285°` front **`Ø27.4 mm` C-clips** | 1 | ~$6.00 | [Amazon](https://www.amazon.com/s?k=5V+mini+diaphragm+air+pump+27mm) |
| 4 | **Pump Driver (Choose 1)** | **Option A:** 1-Ch `5V` Optocoupler Relay Module (`~20 × 30 mm`)<br>**Option B:** `IRLZ44N` Logic-Level N-MOSFET + `220 Ω` gate resistor + `10 kΩ` pull-down | `285°` arched base bay (`M3` holes) | 1 | ~$2.00 | [Amazon](https://www.amazon.com/s?k=5V+1+channel+optocoupler+relay+module) / [Grainger](https://www.grainger.com/search?searchQuery=IRLZ44N+MOSFET) |
| 5 | **Flyback Diode** | **`1N4007`** rectifier diode (across pump `+` / `−`, cathode to `+`) | Inline at pump leads (protects ESP32/driver) | 1 | ~$0.25 | [Amazon](https://www.amazon.com/s?k=1N4007+rectifier+diode) / [Grainger](https://www.grainger.com/search?searchQuery=1N4007+diode) |
| 6 | **I²C Pull-Up Resistors** | **`4.7 kΩ`** (1/4 W) resistors × 2 *(only if bare SHT30 probe lacks internal pull-ups)* | `SDA` & `SCL` to `3.3V` | 2 | ~$0.25 | [Amazon](https://www.amazon.com/s?k=4.7k+ohm+resistor+1%2F4W) / [Grainger](https://www.grainger.com/search?searchQuery=4.7k+ohm+resistor) |
| 7 | **Power Supply** | **`5V 2A` Regulated DC Power Supply** + `5.5×2.1 mm` barrel/USB-C pigtail | Benchtop beside `180°` bay | 1 | ~$6.00 | [Amazon](https://www.amazon.com/s?k=5V+2A+DC+power+supply+5.5x2.1mm) / [Grainger](https://www.grainger.com/search?searchQuery=5V+2A+power+supply) |
| 8 | **Wiring & Fasteners** | **Dupont jumper wires** (F-F / M-F, 10–20 cm), **`M3 × 8 mm` screws** (8×) + nylon standoffs, **split silicone grommet / putty** (`Ø10 mm` port seal) | Base bays & `120°` sensor port | 1 set | ~$3.00 | [Amazon](https://www.amazon.com/s?k=M3x8mm+screws+dupont+jumper+wires) / [Grainger](https://www.grainger.com/search?searchQuery=M3+x+8mm+machine+screw) |

**Estimated Electronics, Sensor & Pump Subtotal:** **~$30.50**

---

## 2. ESP32 Wiring Pinout (`firmware/esp32_humid_controller/esp32_humid_controller.ino`)

| ESP32 Pin | Connects To | Notes |
|---|---|---|
| `3.3V` | SHT30/31 `VCC` (Red) | **Do not** power SHT30 from `5V` if bare 3.3V sensor |
| `GND` | SHT30/31 `GND` (Black), Driver `GND`, PSU `GND` | Common ground across ESP32, sensor, and 5V PSU |
| `GPIO 21` | SHT30/31 `SDA` (Yellow/Green) | I²C Data (`0x44`), `4.7 kΩ` pull-up to `3.3V` if needed |
| `GPIO 22` | SHT30/31 `SCL` (White/Blue) | I²C Clock (`0x44`), `4.7 kΩ` pull-up to `3.3V` if needed |
| `GPIO 25` | Relay `IN` or MOSFET `Gate` (via `220 Ω`) | `HIGH` = Pump ON (`RH < 85%`), `LOW` = Pump OFF (`RH >= 90%`) |
| `VIN / 5V` | `5V PSU (+)` & Relay `COM` (or Pump `+`) | Powers ESP32 & air pump; put `1N4007` across pump leads |
