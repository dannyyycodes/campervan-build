# 01 — Insulation (sheep wool, breathable)

**Spec (locked):** sheep wool, breathable / vapour-open build, **no spray foam, no Dynamat**, mould-resistant via breathability + roof fan + no carpet.

## ⚠️ Two deviations to lock before building (sign-off)
1. **Don't hold the wool with spray adhesive** — it off-gasses (breaks the zero-VOC brief). Use **jute netting / mould-resistant string criss-cross**, or friction-pack into rib bays held by the cladding.
2. **"Breathable" ≠ nothing.** The correct non-toxic move is wool **+ a variable / breather membrane on the warm (interior) side** (Thermofloc / Intello-type) — slows bulk vapour but still dries. NOT a sealed poly vapour barrier (traps moisture → rust/mould), NOT bare wool with no membrane.

## Why wool fits this build
Hygroscopic — absorbs ~35–40% of its weight in moisture, stays dry to touch, buffers humidity, and warms slightly as it absorbs → raises local dew point → *reduces* condensation. Builders opening wool walls years later find them dry. Trade-off: lower R-value than foam, so go thicker (the H3 roof gives the headroom).

## Spec by surface
| Surface | Wool | ~R | Notes |
|---|---|---|---|
| **Ceiling** | **75–100mm** | R-10–14 | Most heat lost up; prioritise. Battens built out, string/jute retained. |
| **Walls** | **50mm** packed in rib bays | R-7 | Ducato rib depth ~45–50mm — fill, don't compress. Thin layer over ribs if depth allows. |
| **Floor** | **25mm rigid breathable board** between battens (NOT loose wool — compresses underfoot) | — | See floor stack below. |
| **Doors / arches** | wool loosely in voids, jute net | — | Keep wool off the hot brake/exhaust side of the arch. |
| **Behind furniture** | full wool, jute net | — | Never leave bare metal behind cabinets (hidden condensation). |

Wool R ≈ **3.6–3.8 per 25mm**. Thicker = warmer.

## Floor build-up (breathable, load-bearing)
25mm battens (**bonded** with Sikaflex, not screwed through the pan) → 25mm rigid board between battens → **12mm birch ply** subfloor → cork/vinyl finish. ≈ **~50mm** build-up.

**Headroom lost total: ~110–150mm** (budget **130mm**: ~50mm floor + ~75–100mm ceiling). Still comfortable standing in H3.

## Anti-corrosion FIRST (can never redo after cladding)
- Existing rust: wire-back → **Bilt Hamber Hydrate-80** converter → protect. Cure + ventilate (off-gasses while wet, inert cured).
- Cavities / ribs / box sections: **Bilt Hamber Dynax-S50** cavity wax (60cm injection lance, self-healing) — inject **every rib** before insulating.
- Underbody: **Bilt Hamber Dynax-UB**.

## In the model
Wall/ceiling/floor layer cross-section: `model/build_section.py` → `van_section.glb`.

## Sources
The Van Conversion, AsoboLife, FarOutRide, gnomadhome, Celtic Sustainables (UK wool), Havelock, Bilt Hamber. (Full URLs in commit history / research notes.)
