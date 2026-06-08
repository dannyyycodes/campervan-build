# 03 — Electrical (12V LiFePO4 + solar + DC-DC)

Designed for the worst case: **UK winter, working every day, parked 2–3 days between drives.** Solar = summer bonus; **the alternator DC-DC is the winter workhorse.**

## Daily energy budget
| Load | Power | h/day | Wh typical | Wh heavy-winter |
|---|---|---|---|---|
| Starlink Mini | 22W | 10–12 | 220 | 264 |
| Laptop | 65W | 8 | 520 | 600 |
| 12V fridge (duty-cycled) | ~17W avg | 24 | 400 | 480 |
| Diesel heater (run) | 12W avg | 8–15 | 96 | 180 |
| Roof fan | 8W avg | 6 | 48 | 30 |
| LED lights | 20W | 4 | 80 | 100 |
| Phone/devices | 15W | 3 | 45 | 60 |
| Kettle (inverter, 2–3 brews) | — | — | 330 | 440 |
| Misc/standby | 8W | 24 | 190 | 190 |
| **TOTAL** | | | **~2.0 kWh** | **~2.5 kWh** |

Design around **2.5 kWh/day**. Kettle-on-inverter (~400Wh/day) is the biggest discretionary load — **boil on gas** and it leaves the electrical budget.

## Battery — **560Ah / 7.2kWh** (2× heated 12V 280Ah LiFePO4, parallel)
2.5kWh × 2 days ÷ 80% usable ≈ 6.25kWh nominal → round to ~7kWh. Gives 2 hard winter days (with electric kettle), ~3 days on gas.
- **Must have low-temp charge cutoff / self-heating BMS** — never charge LiFePO4 below 0°C (the UK-winter killer).
- Recommended: **2× Fogstar Drift 280Ah heated** (~£1,240). Parallel pair survives one dropping out.

## Solar — fit the max (~580–600W), but it's a summer gift
Honest UK numbers (flat roof, S England): **Dec ~40Wh/day per 100W**, **Jul ~320Wh/day per 100W** (7–8× swing). 580W → **~200Wh/day winter vs ~1.7kWh/day summer.** Covers most of a summer day; **<10% of a winter day.**
- 3× ~190–200W rigid on the roof rack. Wire **2S series strings** (starts harvesting earlier on dim mornings).
- **Victron SmartSolar MPPT 100/50** (~£190).

## DC-DC alternator charger — the winter lifeline
**1× Victron Orion-Tr Smart 12/12-30A Isolated** (~£250). 1h driving ≈ 360Wh; 2–3h/day ≈ 720–1,080Wh (30–45% of a winter day). Ducato alternator (150–180A) feeds one 30A fine. Isolated = cleaner for the EMF/earth scheme. Trigger off **ignition D+** (engine-only charging).

## Inverter — **Victron Phoenix 12/2000 VE.Direct pure sine** (~£540)
Pure sine (laptop PSU, EMF-clean). 2000W covers a 1500W kettle peak. **ECO mode idles <1W** — leave it armed. (Gas-only boiling → a 12/1200 ~£350 suffices.)

## Kettle decision (sign-off)
**Boil on gas primarily** (0Wh, fastest, ~£30/bottle lasts months) + **keep a 1500W electric kettle on the inverter** for no-gas convenience. That one choice swings ~400Wh/day (~15% of winter budget).

## EMF architecture (your spec → practice)
- **Bedside master kill-switch** on the main positive (Victron/Blue Sea 300–600A) — kills all house DC at night, zeroing fields near the bed.
- **Single-point chassis earth:** every negative → one negative busbar → **one** 70mm² bond to **one** paint-stripped chassis point. No daisy-chained negatives (ground loops).
- **Twisted-pair DC** runs (cancels magnetic field) — especially bedside + Starlink.
- Starlink Mini → **wired Ethernet** to laptop; short/heavy DC run or 12→30V step-up (avoids boot-sag restart loop).

## Fusing & cable (defence in depth)
- **MRBF 250A on each battery +post** (fuse at source).
- Inverter branch: **ANL/MEGA 250A**. MPPT 60A, Orion 50A MEGA in a **Victron Lynx Distributor**.
- 12V loads: **Blue Sea blade fuse block**, each branch on its own fuse. **Fuse protects the cable, not the device.**
- Cable (size on current AND round-trip length): battery↔bus **70mm²**, inverter **50–70mm²**, Orion/MPPT **10–16mm²**, branches 2.5–4mm², chassis bond **70mm²**.

## Shopping list (Victron-centric, ~mid-2026 UK)
Batteries 2×Fogstar 280Ah heated **£1,240** · SmartShunt 500A £110 · Orion-Tr 30A iso £250 · MPPT 100/50 £190 · 3× solar ~£360 · Phoenix 12/2000 £540 · Lynx Distributor £260 · fuses £80 · bedside isolator £60 · neg busbar £40 · blade block £35 · cable/lugs £150 · branch wiring £120 · Starlink step-up £40 → **core ≈ £3,475** (+£300–600 mounts/EHU/Cerbo).
**Suggested add:** Victron IP22 EHU shore charger (~£120) for winter static stretches when alternator+solar can't keep up.

## In the model
Battery/inverter/MPPT bay in the rear garage under the bed (`Elec_Bay`). Solar on the roof rack.

## Sources
FarOutRide (sizing/calculator), Will Prowse/DIY Solar, EXPLORIST.life, Victron docs, Roam Wired UK PSH, Quirky Campers.
