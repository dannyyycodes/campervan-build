# Campervan Build — Citroën Relay / Fiat Ducato L3 H3

Full-time, off-grid, non-toxic camper conversion. A to-scale 3D model **plus** a system-by-system build plan, all versioned in git.

**🔗 Live 3D viewer + plan:** https://dannyyycodes.github.io/campervan-build/

## The van
Citroën Relay = Fiat Ducato = Peugeot Boxer (same SeVeL van) — **L3 (LWB) H3 (high roof)**, 3500kg, FWD, 2.3 MultiJet diesel, manual.
- Interior load bay: **3705 × 1870 × 2172 mm** (1422 between wheel arches)
- External: **5998 × 2050 × 2764 mm**, wheelbase 4035, wheels Ø744

## Brief (locked)
- **Non-toxic + breathable:** sheep wool, formaldehyde-free birch ply, zero-VOC, **no spray foam, no Dynamat**.
- **EMF-conscious:** master kill-switch by bed, Ethernet over Wi-Fi, single-point chassis earth, twisted-pair DC.
- **Off-grid full-time**, works on a laptop over **Starlink Mini**.
- Transverse bed (6ft fits) on a garage; swivel cab seats + fold-down desk; minimal water (food-grade cans + sink), small gas hob; **no fixed toilet** (facility-hop + emergency backup); diesel heater; roof fan; drive-away awning; Surron e-bike on a tow-ball rack.

## Repo layout
- [`/model`](model) — Blender `.blend`, exported `.glb`, and the Python build scripts (re-run to regenerate the model).
- [`/plan`](plan) — system-by-system design docs. **Start:** [`plan/_index.md`](plan/_index.md).
- [`/docs`](docs) — the GitHub Pages 3D viewer (`index.html` + the `.glb`s it loads).

## How to iterate (the loop)
1. Edit a build script in `/model` (e.g. `build_van_master.py`).
2. Re-run headless: `blender --background --python model/<script>.py`.
3. Commit. The git history **is** your design iteration log — roll back anytime.

Open the master model: `model/ducato_L3H3_master.blend` in Blender 4.5.

> A real licensed Fiat Ducato reference model is used **locally** for planning (open3dmodel, personal-use licence) — it is intentionally **not** committed/published here. The viewer ships a from-scratch, licence-clean van instead.
