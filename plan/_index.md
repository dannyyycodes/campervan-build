# Build plan — system by system

The **build order is sacred** — each system precedes the next for a reason (you can't insulate after cladding, can't run cables after the walls are on). See [00-build-order](00-build-order.md).

| # | System | Doc | Status |
|---|--------|-----|--------|
| 00 | Build order & sequence | [00-build-order.md](00-build-order.md) | ✅ drafted |
| 01 | Insulation (sheep wool, breathable) | [01-insulation.md](01-insulation.md) | ✅ researched |
| 02 | Ventilation & condensation | [02-ventilation.md](02-ventilation.md) | ✅ researched |
| 03 | Electrical (12V LiFePO4 + solar + DC-DC) | [03-electrical.md](03-electrical.md) | ✅ researched |
| 04 | Water & plumbing (cans + sink) | [04-water-plumbing.md](04-water-plumbing.md) | ✅ researched |
| 05 | Gas (single hob + safety) | [05-gas.md](05-gas.md) | ✅ researched |
| 06 | Facilities & toilet (facility-hop) | [06-facilities-toilet.md](06-facilities-toilet.md) | ✅ researched |
| 07 | Weight & payload budget | [07-weight-payload.md](07-weight-payload.md) | ⏳ todo |
| 08 | Cut list (timber + ply) | [08-cut-list.md](08-cut-list.md) | ⏳ from model |
| 09 | Materials — non-toxic spec | [09-materials-nontoxic.md](09-materials-nontoxic.md) | ✅ drafted |

## ⚠️ Decisions awaiting sign-off (pulled from the research)
1. **DVLA "Motor Caravan" reclass — yes or no?** Portable single hob = minimal, no gas regime, but likely **fails** reclass. Fixed hob = passes, but triggers BS EN 1949 + Gas-Safe. Can't have both. ([05-gas](05-gas.md))
2. **Insulation fixings:** lock **jute net/string, not spray adhesive** (off-gas); and **wool + variable/breather membrane**, not bare wool. ([01-insulation](01-insulation.md))
3. **Fresh water can:** stainless (~£70–90) vs BPA-free HDPE (~£15). ([04-water-plumbing](04-water-plumbing.md))
4. **Kettle:** gas-primary + 1500W electric backup (recommended) — sets inverter/battery. ([03-electrical](03-electrical.md))
5. **Electrical budget:** ~£3,475 core (560Ah bank + Victron). Sign-off the spend tier.

Each doc = the design for one system: what, why, sizing/numbers, components + UK prices, schematic. The 3D model in [`/model`](../model) shows where each system physically lives.
