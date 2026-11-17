#!/usr/bin/env python3
"""
Generates a self-contained interactive 3D Orthographic Assembly Viewer
(mvp_assembly_viewer.html) with all MVP STL meshes embedded as base64.
"""

import base64
import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STL_DIR = os.path.join(CURRENT_DIR, "out", "stl")
OUT_HTML = os.path.join(CURRENT_DIR, "mvp_assembly_viewer.html")

PARTS_META = [
    ("mvp_bottom_base", "Bottom Base (Standard Arched Bays)", "#3b82f6", 1.0, 0.0),
    ("mvp_bottom_base_collection", "Bottom Base (10 mL Syringe Holder)", "#60a5fa", 1.0, 0.0),
    ("mvp_tube_ref", "Clear Acrylic Tube (85x90x100 mm)", "#67e8f9", 0.28, 1.0),
    ("mvp_top_lid", "Top Lid (Standard Slide-On)", "#10b981", 1.0, 2.0),
    ("mvp_top_lid_falcon", "Top Lid (50 mL Falcon Loop)", "#14b8a6", 1.0, 2.0),
    ("mvp_falcon_cap_2port", "Falcon 2-Port Humidifier Cap", "#f59e0b", 1.0, 2.8),
    ("mvp_top_lid_syringe_tower", "Top Lid (50 mL Syringe Tower)", "#10b981", 1.0, 2.0),
    ("mvp_top_lid_syringe_cage", "Top Lid (Compact Center Cage)", "#059669", 1.0, 2.0),
    ("mvp_syringe_tower_addon_half", "Half-Height Syringe Adapter (82.5 mm)", "#34d399", 1.0, 2.0),
    ("mvp_candle_collar", "Candle Drop-In Collar", "#f59e0b", 1.0, 3.0),
    ("mvp_syringe_cage_addon", "Glue-On 50 mL Syringe Cage", "#fbbf24", 1.0, 3.5),
    ("mvp_syringe_cage_addon_25ml", "Glue-On 25 mL Syringe Cage", "#f59e0b", 1.0, 3.5),
    ("mvp_cage_retainer_ring", "Snap-In Cage Retainer Ring", "#ec4899", 1.0, 4.2),
    ("mvp_syringe_cage_snap", "Snap-On 50 mL Net (1-Piece)", "#f97316", 1.0, 3.5),
    ("mvp_syringe_cage_snap_25ml", "Snap-On 25 mL Net (1-Piece)", "#ea580c", 1.0, 3.5),
    ("mvp_syringe_cage_snap_falcon", "Snap-On 50 mL Net + Falcon Holder", "#fb923c", 1.0, 3.5),
    ("mvp_syringe_cage_snap_falcon_funnel", "Double-Funnel Net + Falcon Cap", "#f43f5e", 1.0, 3.5),
    ("mvp_candle_ref", "4-in Ceramic Filter Candle", "#e2e8f0", 1.0, 3.0),
    ("mvp_syringe_50ml_ref", "50 mL Nutrient Feed Syringe", "#bae6fd", 0.42, 4.0),
    ("mvp_syringe_10ml_ref", "10 mL Collection Syringe", "#bae6fd", 0.42, 0.0),
    ("mvp_falcon_50ml_ref", "50 mL Falcon Humidifier Tube", "#7dd3fc", 0.40, 2.2),
    ("mvp_electronics_ref", "ESP32, Relay, Air Pump & 5V PSU", "#a855f7", 1.0, 0.0),
    ("mvp_sensor_probe_ref", "SHT30 Temp/RH Probe & Cable", "#eab308", 1.0, 1.5),
    ("mvp_cables_ref", "Power & Pump Control Cables", "#ef4444", 1.0, 0.0),
    ("mvp_plumbing_ref", "Air Tubes, Drain Tube & Valve", "#06b6d4", 0.78, 0.0),
]


def main():
    embedded = {}
    for name, label, color, opacity, explode_tier in PARTS_META:
        path = os.path.join(STL_DIR, f"{name}.stl")
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        embedded[name] = {
            "label": label,
            "color": color,
            "opacity": opacity,
            "explodeTier": explode_tier,
            "b64": b64,
        }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>CoSE Mycoponic MVP — Interactive Orthographic Assembly</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    display: flex;
    height: 100vh;
    overflow: hidden;
  }}
  #sidebar {{
    width: 310px;
    background: #1e293b;
    border-right: 1px solid #334155;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow-y: auto;
  }}
  h1 {{ font-size: 16px; font-weight: 700; color: #f8fafc; }}
  .sub {{ font-size: 12px; color: #94a3b8; margin-top: 2px; }}
  .group {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .group-title {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94a3b8;
  }}
  .btn-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }}
  button {{
    background: #334155;
    color: #f1f5f9;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 7px 10px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
  }}
  button:hover {{ background: #475569; }}
  button.active {{
    background: #2563eb;
    border-color: #3b82f6;
    color: #ffffff;
  }}
  label.row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    gap: 8px;
    cursor: pointer;
  }}
  input[type="range"] {{ width: 100%; accent-color: #3b82f6; }}
  .swatch {{
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 2px;
    margin-right: 6px;
  }}
  .specs {{
    font-size: 11px;
    line-height: 1.55;
    color: #cbd5e1;
  }}
  #viewport {{
    flex: 1;
    position: relative;
  }}
  #hud {{
    position: absolute;
    bottom: 14px;
    left: 14px;
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 11px;
    color: #94a3b8;
    pointer-events: none;
  }}
</style>
</head>
<body>
  <aside id="sidebar">
    <div>
      <h1>CoSE Mycoponic MVP</h1>
      <div class="sub">Interactive Orthographic CAD Assembly</div>
    </div>

    <div class="group">
      <div class="group-title">Orthographic Views</div>
      <div class="btn-grid">
        <button id="view-iso" class="active">Isometric</button>
        <button id="view-front">Front (XZ)</button>
        <button id="view-side">Side (YZ)</button>
        <button id="view-top">Top (XY)</button>
      </div>
    </div>

    <div class="group">
      <div class="group-title">Configuration Presets</div>
      <div class="btn-grid">
        <button id="preset-fullsys" class="active">Full System (+ Electronics)</button>
        <button id="preset-funnel">Double-Funnel Net</button>
        <button id="preset-snap50">Snap-On 50 mL Net</button>
        <button id="preset-tower">Full Tower</button>
      </div>
    </div>

    <div class="group">
      <div class="group-title">Exploded View: <span id="exp-val">0</span> mm</div>
      <input id="explode" type="range" min="0" max="80" value="0" step="1" />
      <label class="row">
        <span>X-Ray Housing (See Funnel &amp; Bays)</span>
        <input id="xray" type="checkbox" />
      </label>
      <button id="toggle-sys" class="active">Hide Electronics &amp; Plumbing</button>
    </div>

    <div class="group">
      <div class="group-title">Parts</div>
      <div id="part-toggles" style="display:flex;flex-direction:column;gap:6px;"></div>
    </div>

    <div class="group specs">
      <div class="group-title">Key Dimensions</div>
      <div>• Tube: 85 mm ID × 90 mm OD × 100 mm</div>
      <div>• Candle: Ø50 × 101.6 mm (top-drop collar)</div>
      <div>• Base: 38.5° funnel, 20 mm side drain</div>
      <div>• Bays: 3× 60° bays + 4× M3 holes each</div>
      <div>• Tower: 3× Ø14 mm pillars, +165 mm (6.5")</div>
    </div>
  </aside>

  <main id="viewport">
    <div id="hud">Left-drag: Orbit • Right-drag: Pan • Scroll: Zoom • True Orthographic Projection</div>
  </main>

  <script type="importmap">
  {{
    "imports": {{
      "three": "https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/"
    }}
  }}
  </script>
  <script type="module">
    import * as THREE from "three";
    import {{ OrbitControls }} from "three/addons/controls/OrbitControls.js";
    import {{ STLLoader }} from "three/addons/loaders/STLLoader.js";

    const PARTS = {json.dumps(embedded)};
    const container = document.getElementById("viewport");
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a);

    // Orthographic camera (Z-up CAD convention mapped via camera.up)
    const frustum = 360;
    const aspect = container.clientWidth / container.clientHeight;
    const camera = new THREE.OrthographicCamera(
      (-frustum * aspect) / 2,
      (frustum * aspect) / 2,
      frustum / 2,
      -frustum / 2,
      -2000,
      2000
    );
    camera.up.set(0, 0, 1);

    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.target.set(0, 0, 125);

    // Studio lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.65));
    const dir1 = new THREE.DirectionalLight(0xffffff, 1.1);
    dir1.position.set(220, -180, 350);
    scene.add(dir1);
    const dir2 = new THREE.DirectionalLight(0x93c5fd, 0.55);
    dir2.position.set(-220, 200, 100);
    scene.add(dir2);

    // Build plate grid on XY plane (Z = 0)
    const grid = new THREE.GridHelper(260, 26, 0x334155, 0x1e293b);
    grid.rotation.x = Math.PI / 2;
    scene.add(grid);

    const loader = new STLLoader();
    const meshes = {{}};
    let useTower = true;

    function b64ToBuffer(b64) {{
      const bin = atob(b64);
      const bytes = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      return bytes.buffer;
    }}

    const togglesDiv = document.getElementById("part-toggles");
    for (const [name, info] of Object.entries(PARTS)) {{
      const geom = loader.parse(b64ToBuffer(info.b64));
      geom.computeVertexNormals();
      const mat = new THREE.MeshStandardMaterial({{
        color: info.color,
        roughness: 0.42,
        metalness: 0.08,
        transparent: info.opacity < 1.0,
        opacity: info.opacity,
        depthWrite: info.opacity >= 1.0,
      }});
      const mesh = new THREE.Mesh(geom, mat);
      mesh.userData = {{ explodeTier: info.explodeTier, baseOpacity: info.opacity }};
      scene.add(mesh);
      meshes[name] = mesh;

      const hiddenByDefault = [
        "mvp_top_lid_falcon",
        "mvp_falcon_cap_2port",
        "mvp_top_lid_syringe_tower",
        "mvp_syringe_tower_addon_half",
        "mvp_bottom_base",
        "mvp_top_lid_syringe_cage",
        "mvp_syringe_cage_addon",
        "mvp_syringe_cage_addon_25ml",
        "mvp_cage_retainer_ring",
        "mvp_syringe_cage_snap",
        "mvp_syringe_cage_snap_25ml",
        "mvp_syringe_cage_snap_falcon_funnel",
      ];
      if (hiddenByDefault.includes(name)) mesh.visible = false;

      const lbl = document.createElement("label");
      lbl.className = "row";
      const left = document.createElement("span");
      left.innerHTML = `<span class="swatch" style="background:${{info.color}}"></span>${{info.label}}`;
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = !hiddenByDefault.includes(name);
      cb.dataset.part = name;
      cb.addEventListener("change", () => {{ mesh.visible = cb.checked; }});
      lbl.appendChild(left);
      lbl.appendChild(cb);
      togglesDiv.appendChild(lbl);
    }}

    function setView(mode) {{
      document.querySelectorAll("[id^='view-']").forEach(b => b.classList.remove("active"));
      document.getElementById(`view-${{mode}}`).classList.add("active");
      const target = controls.target.clone();
      if (mode === "iso") camera.position.set(target.x + 280, target.y - 280, target.z + 220);
      if (mode === "front") camera.position.set(target.x, target.y - 400, target.z);
      if (mode === "side") camera.position.set(target.x + 400, target.y, target.z);
      if (mode === "top") camera.position.set(target.x, target.y - 0.01, target.z + 400);
      camera.lookAt(target);
      controls.update();
    }}
    setView("iso");

    document.getElementById("view-iso").onclick = () => setView("iso");
    document.getElementById("view-front").onclick = () => setView("front");
    document.getElementById("view-side").onclick = () => setView("side");
    document.getElementById("view-top").onclick = () => setView("top");

    function applyPreset(id, activeParts) {{
      document.querySelectorAll("[id^='preset-']").forEach(b => b.classList.remove("active"));
      document.getElementById(id).classList.add("active");
      const all = Object.keys(meshes);
      for (const name of all) {{
        const on = activeParts.includes(name);
        meshes[name].visible = on;
        document.querySelector(`input[data-part="${{name}}"]`).checked = on;
      }}
    }}
    const sysLayerNames = ["mvp_electronics_ref", "mvp_sensor_probe_ref", "mvp_cables_ref", "mvp_plumbing_ref"];
    let sysVisible = true;
    const toggleSysBtn = document.getElementById("toggle-sys");
    function syncSysBtn() {{
      toggleSysBtn.classList.toggle("active", sysVisible);
      toggleSysBtn.textContent = sysVisible ? "Hide Electronics & Plumbing" : "Show Electronics & Plumbing";
    }}
    toggleSysBtn.onclick = () => {{
      sysVisible = !sysVisible;
      for (const name of sysLayerNames) {{
        meshes[name].visible = sysVisible;
        document.querySelector(`input[data-part="${{name}}"]`).checked = sysVisible;
      }}
      syncSysBtn();
    }};

    const common = ["mvp_bottom_base_collection", "mvp_tube_ref", "mvp_candle_ref", "mvp_candle_collar", "mvp_syringe_50ml_ref", "mvp_syringe_10ml_ref"];
    const sysParts = ["mvp_top_lid", "mvp_syringe_cage_snap_falcon", "mvp_falcon_50ml_ref", ...sysLayerNames];
    document.getElementById("preset-fullsys").onclick = () => {{ sysVisible = true; syncSysBtn(); applyPreset("preset-fullsys", [...common, ...sysParts]); }};
    document.getElementById("preset-funnel").onclick = () => {{ sysVisible = true; syncSysBtn(); applyPreset("preset-funnel", [...common, "mvp_top_lid", "mvp_syringe_cage_snap_falcon_funnel", "mvp_falcon_50ml_ref", ...sysLayerNames]); }};
    document.getElementById("preset-snap50").onclick = () => {{ sysVisible = false; syncSysBtn(); applyPreset("preset-snap50", [...common, "mvp_top_lid", "mvp_syringe_cage_snap"]); }};
    document.getElementById("preset-tower").onclick = () => {{ sysVisible = false; syncSysBtn(); applyPreset("preset-tower", [...common, "mvp_top_lid_syringe_tower"]); }};

    const explodeSlider = document.getElementById("explode");
    const expVal = document.getElementById("exp-val");
    explodeSlider.oninput = () => {{
      const d = Number(explodeSlider.value);
      expVal.textContent = d;
      for (const mesh of Object.values(meshes)) {{
        mesh.position.z = mesh.userData.explodeTier * d;
      }}
    }};

    document.getElementById("xray").onchange = (e) => {{
      const x = e.target.checked;
      for (const name of ["mvp_bottom_base", "mvp_top_lid", "mvp_top_lid_syringe_tower"]) {{
        const m = meshes[name];
        m.material.transparent = x;
        m.material.opacity = x ? 0.35 : 1.0;
        m.material.depthWrite = !x;
        m.material.needsUpdate = true;
      }}
    }};

    window.addEventListener("resize", () => {{
      const a = container.clientWidth / container.clientHeight;
      camera.left = (-frustum * a) / 2;
      camera.right = (frustum * a) / 2;
      camera.top = frustum / 2;
      camera.bottom = -frustum / 2;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    }});

    (function animate() {{
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }})();
  </script>
</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    docs_dir = os.path.join(CURRENT_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    docs_viewer = os.path.join(docs_dir, "viewer.html")
    with open(docs_viewer, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {OUT_HTML} ({os.path.getsize(OUT_HTML) / 1024:.1f} KB)")
    print(f"Generated {docs_viewer} ({os.path.getsize(docs_viewer) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
