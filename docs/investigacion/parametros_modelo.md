# Giant-humanoid ("mech") scaling model: sourced parameters

Compiled 2026-10-29. Verification tags:
- **[V]**: I read the number in the primary document text myself (PDF or page fetched and parsed).
- **[S]**: the number comes from a search-engine excerpt of the cited page. I did not open the page. Check it before relying on it.
- **[M]**: standard handbook value from memory. I could not open a source this session (blocked or paywalled). Treat it as a placeholder until checked.

---

## 1. Human gait biomechanics (normalized by body mass)

### 1a. Level walking: peak sagittal moments, powers, angles [V]
Source: Silder, Besier & Delp (2012), *Predicting the metabolic cost of incline walking from muscle activity and walking mechanics*, J Biomech, doi:10.1016/j.jbiomech.2012.03.032. Data are from 16 subjects on a treadmill at 1.29 ± 0.11 m/s. Values are from Table 3, mean (SD).
URL: https://nmbl.stanford.edu/publications/pdf/Silder2012.pdf

| Quantity | 0 % (level) | 5 % incline | 10 % incline |
|---|---|---|---|
| Hip extension moment (N·m/kg) | **0.93 (0.23)** | 1.22 (0.25) | 1.70 (0.32) |
| Hip flexion moment (N·m/kg) | 0.58 (0.18) | 0.49 | 0.34 |
| Knee extension moment (N·m/kg) | **0.94 (0.24)** | 0.67 | 0.36 |
| Knee flexion moment (N·m/kg) | 0.44 (0.19) | 0.68 | 1.03 |
| Ankle plantarflexion moment (N·m/kg) | **1.62 (0.17)** | 1.87 (0.14) | 2.16 (0.29) |
| Hip power generation, 1st peak (W/kg) | 1.20 (0.36) | 1.78 | 3.15 (0.91) |
| Hip power generation, 2nd peak (W/kg) | 0.94 (0.29) | 1.09 | 1.06 |
| Hip power absorption (W/kg) | 0.49 | 0.35 | 0.02 |
| **Ankle power generation, push-off (W/kg)** | **2.00 (0.51)** | 2.52 (0.49) | 3.35 (0.75) |
| Hip flexion / extension angle (deg) | 29 / 15 | 35 / 15 | 43 / 15 |
| Knee flexion, stance / swing (deg) | 21 / 69 | 25 / 67 | 34 / 68 |
| Ankle dorsiflexion / plantarflexion (deg) | 10 / 14 | 11 / 15 | 14 / 15 |

Implied walking range of motion: hip about 44°, knee about 69°, ankle about 24°.

Other walking values:
- **Ankle push-off (A2) peak power: 2.46 W/kg** (95 % CI 2.41–2.50), at its highest in the third decade of life, from a large lifespan study. Quote: "ankle push-off (A2) power peaked with a value of 2.46 (95%CI 2.41 to 2.50) W/kg in the 3rd decade of life". [S] https://cris.maastrichtuniversity.nl/en/publications/evolution-of-joint-power-across-the-lifespan-during-walking/
- Another review gives peak ankle push-off of ">2.5 W kg−1", citing Zelik & Kuo 2010. [S] https://pmc.ncbi.nlm.nih.gov/articles/PMC4664043
- **Peak plantarflexion moment: about 1.0–1.3 N·m/kg.** Young males 1.30 (0.11), young females 1.22 (0.19), elderly males 1.16 (0.22), elderly females 1.02 (0.16). [S] https://pmc.ncbi.nlm.nih.gov/articles/PMC4499994/table/tbl_002
- A meta-visualization estimates 1.0–1.5 N·m/kg plantarflexion at normal walking speed. [S] https://www.biorxiv.org/content/10.1101/2024.06.22.600197v1.full
- Winter's push-off values, as cited on the CGA FAQ: knee 0.16 N·m/kg extensor with 0.76 W/kg eccentric; hip 0.4 N·m/kg flexor with 0.67 W/kg concentric. The site's earlier, larger values were later found to be a synchronization error. [V] https://clinicalgaitanalysis.com/faq/moment.html

### 1b. Knee across tasks [V]
Source: *Knee Joint Biomechanics in Physiological Conditions and How Pathologies Can Affect It: A Systematic Review*, Applied Bionics & Biomechanics 2020, Article 7451683, doi:10.1155/2020/7451683. URL: https://pdfs.semanticscholar.org/78fb/0ba5b04dab71eaedf16e1a632cda96a665f6.pdf

| Task | Knee ROM (deg) | Peak knee extension moment (N·m/kg) | Knee power (W/kg) |
|---|---|---|---|
| Normal walking (11 studies) | "around 53 to 75 deg" | 1st peak 0.129–0.945. Total moment range 0.458–1.265 | generation 0.286–0.834; absorption up to −2.71 |
| Running (5–7 studies) | "around 60 to 115 deg" | **1.157–2.574**. "range of moment is about 1.434 to 3.904 Nm/kg for running" | generation 2.739–9.405; absorption −1.7 to **−12.6** |
| Stair ascent (7 studies) | 78–94 | 0.454–1.409 (moment range 1.010–1.815) | generation up to 2.887 |
| Stair descent | 76–90 | moment range 0.435–1.815 | absorption to about −5.5 |
| Sit-to-stand (9 studies) | about 82–96 | **0.619–2.187** (typical 0.619–1.578) | about 0.56–1.97 |

Other task data:
- Stair ascent, young vs old adults: knee extensor 1.19 ± 0.24 vs 0.89 ± 0.22 N·m/kg. Ankle plantarflexor 1.48 ± 0.27 vs 1.24 ± 0.21 N·m/kg. A healthy-control group gave 1.07 ± 0.20 N·m/kg. [S] https://pubmed.ncbi.nlm.nih.gov/17126461/ and https://lermagazine.com/article/stair-negotiation-alters-stability-in-older-adults
- Sit-to-stand: "The peak knee joint moment ranged from 0.51 to 1.97 N.m/kg". Hip plus knee moment must exceed 1.53 N·m/kg for a successful sit-to-stand. [S] https://link.springer.com/article/10.1186/1475-925X-6-26
- Running speed, 7.96 → 15.91 km/h: peak plantarflexion moment rises by 0.74 N·m/kg and peak knee extension moment by 0.52 N·m/kg (Petersen et al. 2014). [S] https://lermagazine.com/?p=22446
- Running absolute values: ankle plantarflexor about 2.5–3.5 N·m/kg and ankle power about 10–20 W/kg at 3–5 m/s (Novacheck 1998; Schache 2011). [M]

**Design takeaway for scaling.** For a bipedal walker, size the joints to about:
- Ankle: 1.6–2.2 N·m/kg
- Knee: 1.0–1.5 N·m/kg (stairs or sit-to-stand up to about 2)
- Hip: 1.0–1.7 N·m/kg
- Ankle power: about 2–3.5 W/kg

Running needs roughly 2–3 times these moments and 5–10 times the power.

---

## 2. Anthropometric segment parameters

### 2a. Dempster model adapted by Winter [V]
Source: Winter DA (2009), *Biomechanics and Motor Control of Human Movement*, 4th ed., Table 4.1, from the BMClab machine-readable copy.
URL: https://raw.githubusercontent.com/BMClab/BMC/master/data/BSP_DempsterWinter.txt (notebook: https://nbviewer.org/github/BMClab/bmc/blob/master/notebooks/BodySegmentParameters.ipynb)

Columns: Mass is the fraction of body mass M. "CM prox / CM dist" is the CoM position as a fraction of segment length from the proximal / distal end. Rg is the radius of gyration as a fraction of segment length, about the CoM, the proximal end and the distal end.

| Segment | Definition | Mass/M | CM prox | CM dist | Rg CM | Rg prox | Rg dist |
|---|---|---|---|---|---|---|---|
| Hand | WJC–KNU2 | 0.006 | 0.506 | 0.494 | 0.297 | 0.587 | 0.577 |
| Forearm | EJC–STYL | 0.016 | 0.430 | 0.570 | 0.303 | 0.526 | 0.647 |
| Upper arm | SJC–EJC | 0.028 | 0.436 | 0.564 | 0.322 | 0.542 | 0.645 |
| Forearm + hand | EJC–STYL | 0.022 | 0.682 | 0.318 | 0.468 | 0.827 | 0.565 |
| Total arm | SJC–STYL | 0.050 | 0.530 | 0.470 | 0.368 | 0.645 | 0.596 |
| Foot | LMAL–MT2 | 0.0145 | 0.50 | 0.50 | 0.475 | 0.690 | 0.690 |
| Leg (shank) | KJC–MMAL | 0.0465 | 0.433 | 0.567 | 0.302 | 0.528 | 0.643 |
| Thigh | GTR–KJC | 0.100 | 0.433 | 0.567 | 0.323 | 0.540 | 0.653 |
| Foot + leg | KJC–MMAL | 0.061 | 0.606 | 0.394 | 0.416 | 0.735 | 0.572 |
| Total leg | GTR–MMAL | 0.161 | 0.447 | 0.553 | 0.326 | 0.560 | 0.650 |
| Head + neck | C7T1–ear | 0.081 | 1.000 | 0 | 0.495 | 0.116 | — |
| Thorax | C7T1–T12L1 | 0.216 | 0.82 | 0.18 | — | — | — |
| Abdomen | T12L1–L4L5 | 0.139 | 0.44 | 0.56 | — | — | — |
| Pelvis | L4L5–GTR | 0.142 | 0.105 | 0.895 | — | — | — |
| Trunk | GTR–SJC | 0.497 | 0.50 | 0.50 | — | — | — |
| Trunk + head + neck | GTR–SJC | 0.578 | 0.66 | 0.34 | 0.503 | 0.830 | 0.607 |
| HAT (head, arms, trunk) | GTR–SJC | 0.678 | 0.626 | 0.374 | 0.496 | 0.798 | 0.621 |

Zatsiorsky / de Leva 1996 male and female tables are in the same repository: `data/BSPmale_ZdeLeva.txt` and `data/BSPfemale_ZdeLeva.txt`. In that model the thigh mass fraction is more than 40 % larger than Dempster's, and the trunk is about 15 % smaller ("Differences" section of the notebook). de Leva PDF: https://ebm.ufabc.edu.br/wp-content/uploads/2013/12/Leva-1996.pdf

### 2b. Segment lengths as fractions of stature H [M]
Source: Drillis & Contini (1966), reproduced as Winter Fig. 4.1. I could not open a copy this session. The landmark heights below are internally consistent: knee − ankle = shank, hip − knee = thigh, shoulder − elbow ≈ upper arm.

| Landmark height above floor | ×H | Segment length or width | ×H |
|---|---|---|---|
| Eye | 0.936 | Thigh (GTR–knee) | **0.245** |
| Chin | 0.870 | Shank (knee–ankle) | **0.246** |
| Shoulder | 0.818 | Foot length | **0.152** |
| Chest | 0.720 | Foot breadth | **0.055** |
| Elbow | 0.630 | Hip width | **0.191** |
| Hip (greater trochanter) | 0.530 | Shoulder width | 0.259 |
| Wrist | 0.485 | Upper arm | **0.186** |
| Knuckle | 0.377 | Forearm | **0.146** |
| Knee | 0.285 | Hand | 0.108 |
| Ankle | 0.039 | Trunk, hip to shoulder (0.818 − 0.530) | **≈0.288** |

The original citations are Drillis, Contini & Bluestein (1964), *Body segment parameters: a survey of measurement techniques*, Artificial Limbs 8:44–66 (http://www.oandplibrary.org/al/1964_01_044.asp), and Winter (2005/2009). A validation in children found errors of about 5–16 % (https://ojs.ub.uni-konstanz.de/cpa/article/view/292).

### 2c. Foot contact area [M, derived]
- Foot bounding box: 0.152H × 0.055H = 0.00836 H². At H = 1.75 m this is about 0.0256 m² per foot.
- Barefoot static plantar contact is typically about 0.010–0.015 m² (100–150 cm²) per foot, or about 0.02–0.03 m² for both feet. That is roughly 45–60 % of the bounding box.
- Mean standing plantar pressure is therefore about M·g / 0.025 m² ≈ 25–30 kPa for a 70 kg adult.
- I did not find a citable source this session (pedobarography literature, e.g. Novel emed). Use the bounding box × 0.5 as the modelling rule.

---

## 3. Hydraulic cylinders: mass per stroke work

### 3a. Industrial 700-bar (10,000 psi) cylinders, Enerpac [V]

| Model | Rated force | Stroke | Mass | Stroke work F×s | **kg/kJ** | Force/mass |
|---|---|---|---|---|---|---|
| RCR10012 (double-acting, hollow plunger) | 104 US ton (95 t) ≈ 925 kN | 300 mm (11.81 in) | 149 lb = **67.6 kg** | 277 kJ | **0.244** | 13.7 kN/kg |
| HCR10012 (double-acting, solid plunger) | 1002 kN (113 US ton) | 300 mm | **73 kg** (161 lb) | 301 kJ | **0.243** | 13.7 kN/kg |
| HCG50012 (single-acting, load return) | 575 US ton ≈ 5114 kN | 300 mm (11.81 in) | 1144 lb = **519 kg** | 1534 kJ | **0.338** | 9.9 kN/kg |

Sources and quotes:
- RCR10012: "Capacity (Imperial tons)104", "Capacity (Metric Tons)95", "Stroke (inch)11.81", "Maximum Operating Pressure (psi)10150", "Weight (lbs)149". Bore 5.12 in (130 mm) and plunger 3.94 in (100 mm) are given in the search excerpt. https://www.enerpac.com/en-us/high-tonnage-cylinders/high-tonnage-cylinder/RCR10012
- HCR10012: "Stroke (inch)11.81", "Collapsed Height A (in)18.86", "Weight (kg)73", "Maximum working pressure up to 10,000 psi (700 bar)". The 1002 kN figure is from the en-gb page title. https://www.enerpac.com/en-us/double-acting-cylinders/high-tonnage-cylinder/HCR10012
- HCG50012: weight 1144 lb, 11.81 in stroke, 23.39 in collapsed height [S]. The 5114 kN figure is the kN rating of the same frame (HCL50012). https://www.enerpac.com/en-US/product/hcg50012-575-ton-capacity-1181-in-stroke-single-acting-high-tonnage-hydraulic-cylinder/p/HCG50012
- Geometry reference only (no mass given): CLRG-1506 is 150 ton, bore 6.26 in, rod 4.49 in, stroke 5.91 in, 10,000 psi. https://www.sourceatlantic.ca/Product/CLRG1506

Note: these are short-stroke jacks, so end caps dominate the mass. A long-stroke cylinder approaches tube-wall mass ≈ ρ·(p·r/σ_allow)·2πr·s per unit work. Expect about 0.15–0.3 kg/kJ for steel at 700 bar, and worse at 210–350 bar.

### 3b. Robotic and aerospace lightweight cylinders
IIT/Moog Integrated Smart Actuators (servovalve, cylinder and sensors in one titanium AM body) [V]. Source: Table 2 of *Highly-Integrated Hydraulic Smart Actuators and Smart Manifolds for High-Bandwidth Force Control* (Front. Robot. AI 2018, doi:10.3389/frobt.2018.00051). https://pmc.ncbi.nlm.nih.gov/articles/PMC7919780/

| Actuator | Bore / rod | Stroke | Stall force | Dry mass | Pressure | Stroke work | **kg/kJ** | Force/mass |
|---|---|---|---|---|---|---|---|---|
| ISA v2 (HyQ hip and knee) | 16 / 12 mm | 80 mm | 4,000 N | 0.92 kg | 20.7 MPa | 320 J | **2.9** | 4.35 kN/kg |
| ISA v5 (HyQ-REAL knee) | 21.5 / 12 mm | 100 mm | 7,500 N | 1.60 kg | 20.7 MPa | 750 J | **2.1** | 4.7 kN/kg |
| Conventional HyQ unit (Hoerbiger LB6-1610-0080 cylinder + Moog E024 valve + manifold, load cell, encoders) | 16 mm bore | 80 mm | about 4 kN | 1.3 kg | 20.7 MPa | about 320 J | about 4.1 | about 3.1 kN/kg |

Quote: "The total estimated weight of the components of 1 actuator unit (excluding the electronics) is 1.3 kg". The ISA v2 "weighs only 0.92 kg".

- Small robot actuators come out about 10 times worse in kg/kJ than big industrial jacks. The reasons are the integrated valve and sensors, the low pressure (207 vs 700 bar) and the short stroke.
- Boston Dynamics Atlas (hydraulic): no public per-actuator force, stroke or mass data. Only system-level claims exist (about 3,000 psi, 3D-printed integrated actuators). Nothing citable was found.

---

## 4. Electro-hydrostatic actuator (EHA)

### Parker Compact EHA [V]
Source: German sales catalogue HY07-1310DE, "Technische Daten" and "Masse" tables. https://www.hefel-technik.com/wp-content/uploads/2024/04/Parker_Hydraulik-EHA-HY07-1310DE-Hefel_Technik.pdf (product page: https://ph.parker.com/pl/en/compact-electro-hydraulic-actuator)

Specifications:
- Bores 25.4 / 31.8 / 36.5 mm; rods 14.2 / 15.9 / 19.1 mm; standard strokes 102 / 152 / 203 mm.
- "Höchstkraft – Ausfahren 21,35 kN", "Höchstkraft – Einfahren 16,00 kN", "Max. Geschwindigkeit 84 mm/s". The product page gives pressure up to 207 bar (3,000 psi).
- Motors: 12 or 24 V DC, 245 W (A/C) or 560 W (B/D).
- **Mass:** base unit without motor is 2.1 / 2.8 / 3.5 kg for 102 / 152 / 203 mm stroke. Add 1.5 kg (motor A/C) or 2.0 kg (motor B/D).

Derived:

| Configuration | Total mass | Force/mass | Rated electrical W/kg | kg per kJ of stroke work |
|---|---|---|---|---|
| 102 mm + 560 W | 4.1 kg | 5.2 kN/kg | 137 W/kg | 1.9 |
| 203 mm + 560 W | 5.5 kg | 3.9 kN/kg | 102 W/kg | 1.27 |

Peak force and peak speed do not occur together. Peak mechanical output is bounded by the 560 W motor.

### Other EHA data points
- Hydra humanoid (University of Tokyo, Kaminaga/Nakamura): 24 double-rod cylinder EHAs, maximum cylinder thrust 1,500 N, rod-seal static friction 0.46 % of maximum force, force-control bandwidth about 53 Hz. No mass was published in the sources I found. [S] https://repository.dl.itc.u-tokyo.ac.jp/record/2001637/files/A35494_review.pdf
- A wheel-legged robot EHA: ">9400 N" force and ">2518 N/kg" force-to-weight. [S] https://doaj.org/article/ba7cf1d3282847b796f89a3dc920fdce
- Rule of thumb for EHAs: about 2.5–5 kN/kg and about 100–300 W/kg (motor-limited). Hydraulic cylinders alone reach about 10–14 kN/kg but need a separate power unit.

---

## 5. Prime movers and energy storage

### Diesel engines [V]
Cummins QSK60 mining engine (60 L V16). Source: Cummins mining bulletin, rev 6/10. https://www.dieselpartsdirect.com/documents/cummins-specs/cummins-qsk-60-mining-specs.pdf

| Rating | Power | Type |
|---|---|---|
| Two-stage QSK60 2850 | 2850 hp (2125 kW) @ 1900 rpm | intermittent |
| Two-stage QSK60 2700 | 2700 hp (2013 kW) | intermittent |
| Two-stage QSK60 2250 | 2250 hp (1678 kW) | continuous |
| Single-stage QSK60 2500 | 2500 hp (1864 kW) | intermittent |
| Single-stage QSK60 2000 | 2000 hp (1491 kW) | continuous |

- Dry weight "14,900 lb (6759 kg)" and "17,175 lb (7794 kg)". Wet weight 8570 / 9616 kg. The two columns are the two builds; the heavier one is presumably two-stage.
- **Power density:**
  - about 2125 / 7794 = **0.27 kW/kg** (dry, intermittent)
  - 1864 / 6759 = **0.28 kW/kg**
  - 0.22 kW/kg continuous
  - about 0.22 kW/kg wet

Caterpillar C18 industrial engine [V]. Source: Cat spec sheet. https://static.ferreyros.com.pe/fcsaprdferreyros01/2021/02/SS-8772183-18396700-082-C18-IND.pdf
- Ratings: "429-522 bkW (575-700 bhp) @ 1800-2100 rpm". Maximum torque 3655 N·m @ 1400 rpm.
- "Weight - Net Dry - Basic Operating Engine Without Optional Attachments 1673 kg".
- **Power density: 522 / 1673 = 0.31 kW/kg.**

Complete diesel-hydraulic power unit (engine, pumps, cooling, tank, oil): about **0.1–0.15 kW/kg** [M, estimate]. Halve the bare-engine figure.

### Battery packs, heavy duty (pack level)
- Proterra H2-23: 176 Wh/kg, 270 Wh/L. [S] https://chargedevs.com/newswire/proterra-launches-rugged-battery-pack-for-heavy-duty-ev-applications/
- Forsee Power ZEN-PLUS: 180 Wh/kg. [S] https://www.electrive.net/2022/03/08/forsee-power-praesentiert-neue-batterien-fuer-schwere-e-fahrzeuge/
- Ioncor Energy Pack (2026): "300 Wh/l and 170 Wh/kg". [S] https://electrive.com/2026/06/05/ioncor-energy-pack-compact-power-for-heavy-duty-electrification
- BYD construction-machinery packs: 120 Wh/kg standard, 160 Wh/kg fast-charge. [S] https://www.electrive.net/2024/11/27/byd-praesentiert-batterien-fuer-elektro-baumaschinen/
- Iveco S-eWay: about 173 Wh/kg derived (69.3 kWh, about 400 kg). [S] https://www.batterydesign.net/iveco-s-eway/
- **Power density** [M]: heavy-duty NMC/LFP packs run at 1–3C continuous, which is about 0.15–0.5 kW/kg. High-power packs reach 1–2 kW/kg at 5–10C. None was verified this session.

---

## 6. Structural materials

### 6a. Ti-6Al-4V fatigue

| Condition | Fatigue strength at 10⁷ cycles | R | Source |
|---|---|---|---|
| Wrought annealed (smooth) | **450–590 MPa** (route-sensitive) | −1 | [S] https://www.sdcverifier.com/wiki/fatigue-strength-and-limit/ |
| Wrought annealed rod, rotating bending | life >10⁷ at **±560 MPa** | −1 | [S] https://www.totalmateria.com/Article86.htm |
| Wrought lamellar (α-lath 10 → 1 µm) | endurance limit about 500 → 600 MPa | — | [V] cited in Hrabe/NIST, below |
| Hot-rolled Ti64, rotating bending | 347 ± 26 MPa | −1 | [S] https://www.sciencedirect.com/science/article/abs/pii/S0142112324002202 |
| LPBF as-built surface, rotating bending | **210 ± 10 MPa** | −1 | [S] same paper. Surface treatments raised it to 446 MPa |
| L-PBF summary (review) | as-produced about 200; machined 300–500; HIP + polished up to 700 MPa | mixed | [S] Metals 2026, 16, 204, https://doi.org/10.3390/met16020204 |
| LPBF + HIP + chemical etch | **≈450 MPa** run-out | 0.1 (max stress) | [V] https://pmc.ncbi.nlm.nih.gov/articles/PMC7345457/ ("fatigue limit of ~450 MPa at 10^7 cycles"; R = 0.1) |
| Optimized LPBF and wrought | 600 MPa | fully reversed | [S] https://advanced.onlinelibrary.wiley.com/doi/10.1002/adem.202500854 |
| EBM, as-built or stress-relieved (machined specimens) | **200–250 MPa** | 0.1 | [V] Hrabe, Gnäupel-Herold, Quinn (NIST), https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=919957 |
| EBM + HIP (machined) | **550–600 MPa** | 0.1 | [V] same: "significantly higher fatigue strength at 10^7 cycles of 550 MPa to 600 MPa was measured for the HIPed condition" |

- Tensile, from PMC7345457 Table 1 [V]:
  - LPBF as-fabricated vertical: YS 820, UTS 1007 MPa
  - LPBF HIP: YS 865, UTS 936 MPa
  - Wrought annealed: YS 790 ± 20, UTS 870 ± 10 MPa
  - ISO 5832-3 minimum: YS > 780, UTS > 860 MPa
- AMS 4928 bar yield: 862–910 MPa. [S] https://gsalloy.com/?p=1266
- Density about 4.43 g/cm³ and E about 110–114 GPa. [M]

**Lattices.** Yavari et al. 2013, *Fatigue behavior of porous biomaterials manufactured using selective laser melting*, Mater Sci Eng C 33:4849, doi:10.1016/j.msec.2013.08.006. Ti6Al4V ELI at 68–84 % porosity: "the normalized endurance limit of all tested porous structures (<0.2) is lower than that of corresponding solid material" (about 0.4). Normalization is to the lattice's own yield or plateau stress, at about 10⁶ cycles. [V, abstract] https://repub.eur.nl/pub/41664

Ahmadi et al. 2018 (Acta Biomater, doi:10.1016/j.actbio.2017.11.014) found that material type matters more than topology for the normalized S-N curve. https://digitalcommons.memphis.edu/facpubs/14735

**Design recommendation** (my interpretation of these sources):

| Material | σ_fat(10⁷) / σ_y |
|---|---|
| As-built lattice | about 0.12–0.2 |
| HIP + surface-finished lattice | about 0.25–0.3 |
| Machined HIP solid | about 0.6–0.65 |

### 6b. Al 7075-T6 [V except fatigue]
Source: Gabrian datasheet (Aluminum Association typical values). https://www.gabrian.com/wp-content/uploads/2018/09/7075-Aluminum-Alloy-Properties.pdf
- Density 2.81 g/cc; UTS 572 MPa; yield 503 MPa; E 71.7 GPa.
- Wikipedia gives 7075-T6 minimum yield as 430–480 MPa. https://en.wikipedia.org/wiki/7075_aluminium_alloy
- **Fatigue strength 159 MPa at 5×10⁸ cycles**, completely reversed, R.R. Moore rotating beam (MatWeb/ASM). [S] https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA7075T6

### 6c. High-strength steels
- **AISI 4340, quenched and tempered:**
  - Yield about 1150 MPa; fatigue strength about 540–740 MPa; E about 190–205 GPa; density 7.85 g/cm³. [S] https://www.makeitfrom.com/material-properties/Quenched-and-Tempered-4340-Ni-Cr-Mo-Steel
  - Hardened and double-tempered at 475°F: UTS 260 ksi (1793 MPa), yield 217 ksi (1496 MPa), elongation 10 %. [V] https://aircraftmaterials.com/data/alstst/E4340.html
  - voestalpine minimum proof strength: 665–1125 MPa depending on section. [S] https://www.voestalpine.com/highperformancemetals/australia/app/uploads/sites/265/2024/08/Datasheet-4340-2026-v1.pdf
- **S690QL (EN 10025-6)** [M]:
  - ReH ≥ 690 MPa (t ≤ 50 mm); Rm 770–940 MPa; E 210 GPa; density 7850 kg/m³.
  - Welded-joint fatigue under EN 1993-1-9 does not depend on yield strength. Detail categories are Δσ_C = 36–160 MPa at 2×10⁶ cycles; the constant-amplitude fatigue limit is 0.737·Δσ_C.
  - So welded high-strength steel gains nothing in fatigue over S355.

### 6d. Quasi-isotropic CFRP [M, not verified; NCAMP site blocked]
- IM7/8552 QI [0/45/90/−45]ns:
  - Unnotched compressive strength about 600–700 MPa; compressive modulus about 55–60 GPa; density about 1.57 g/cm³.
  - UD 0° compressive strength 1570 MPa (Lee & Soutis); calculated 0° ply failure stress in the multidirectional laminate about 1710 MPa. [S] https://eprints.whiterose.ac.uk/2661
  - Authoritative QI UNC1 allowables are in NCAMP NCP-RP-2009-028 §5.2.1. https://wichita.edu/industry_and_defense/NIAR/Documents/NCP-RP-2009-028-Rev-B-HEXCEL-8552-IM7-Uni-SAR-4-16-2019.pdf
- T300/T700-class QI: E about 45–50 GPa; σ_c about 450–600 MPa.
- Open-hole or impact-damaged design allowables are about 250–350 MPa (about 0.4–0.5 × unnotched).

---

## 7. Thin-walled cylinder local buckling, NASA SP-8007 [V]
Source: NASA SP-8007, *Buckling of Thin-Walled Circular Cylinders* (1965, revised Aug 1968). https://ntrs.nasa.gov/api/citations/19690013955/downloads/19690013955.pdf. The 2020 update NASA/SP-8007-2020/REV 2 is at https://ntrs.nasa.gov/citations/20205011530

**Axial compression, isotropic unstiffened (eqs. 4–6):**
- Eq. 4: σ_cr = γ · E / √(3(1−ν²)) · t/r ≈ **0.605 γ E t/r** for ν = 0.3. The monograph writes it as "0.6 γ E t/r".
- Eq. 5: **γ = 1 − 0.901 (1 − e^(−φ))**
- Eq. 6: **φ = (1/16) √(r/t)**, valid for r/t < 1500.
- The monograph calls this "a good lower bound for most test data". Use with caution for L/r > 5, where it has not been verified.
- Computed γ: r/t = 50 → 0.68; 100 → 0.58; 200 → 0.47; 500 → 0.32; 1000 → 0.22.

**Other cases:**
- Bending: same form, γ = 1 − 0.731 (1 − e^(−φ)). [M] I did not re-read this equation in the scan.
- Orthotropic or layered cylinders (eq. 45): same γ form, with t replaced by the geometric-mean radius of gyration √(⁴√(Dx·Dy/(Ex·Ey)))·√12. [V, form only]
- Stiffened cylinders with closely spaced, moderately large stiffeners: "multiplied by a factor of 0.75".
- Lateral or external pressure: γ = 0.75 (eq. 20); long cylinders that buckle into an oval shape: γ = 0.90 (eq. 21).
- Torsion: theoretical critical torque × 0.67 for moderately long cylinders.
- Internal pressure (eq. 34): P = 2πE t²(0.6γ + Δγ) + pπr², with Δγ from Fig. 6.
- Modern work (e.g. NASA SBKF) shows SP-8007 is conservative. Typical modern knockdown factors are about 0.65–0.8 for well-made, analysed shells. NASA tech brief: https://ntrs.nasa.gov/api/citations/20240000391/downloads/TB%2016%2001%20Buckling%20Knockdown%20Factors.pdf

---

## Quick reference for the scaling model

| Parameter | Value | Tag |
|---|---|---|
| Ankle moment, walking | 1.3–1.6 N·m/kg (2.2 on 10 % incline) | V |
| Knee moment, walking | about 0.9 N·m/kg | V |
| Knee moment, stairs / sit-to-stand | 1.0–2.2 N·m/kg | V |
| Hip moment, walking | about 0.9 N·m/kg (1.7 on incline) | V |
| Knee extension moment, running | 1.2–2.6 N·m/kg | V |
| Ankle push-off power | 2.0–2.5 W/kg (3.4 on incline) | V/S |
| Leg mass (thigh + shank + foot) | 0.161 M per leg | V |
| Thigh length | 0.245 H | M |
| Shank length | 0.246 H | M |
| Foot length × breadth | 0.152 H × 0.055 H | M |
| Industrial 700-bar cylinder | 0.24–0.34 kg per kJ of stroke work; 10–14 kN/kg | V |
| Robot servo-cylinder at 207 bar | 2–3 kg/kJ; about 4.5 kN/kg | V |
| Parker Compact EHA | about 1.3–1.9 kg/kJ; 4–5 kN/kg; 100–140 W/kg | V |
| Large diesel engine, dry | 0.27–0.31 kW/kg | V |
| Diesel-hydraulic power unit | about 0.1–0.15 kW/kg | M |
| Heavy-duty battery pack | 120–180 Wh/kg | S |
| Ti64 at 10⁷ cycles | wrought about 500–600; AM as-built about 200–250; AM HIP + machined about 450–600 MPa | V/S |
| Ti64 lattice σ_fat / σ_y | <0.2 (solid about 0.4) | V |
| 7075-T6 | ρ 2.81; σ_y 503; E 71.7 GPa; σ_fat 159 MPa at 5e8 | V/S |
| Cylinder buckling | σ_cr = 0.605 γ E t/r, γ = 1 − 0.901(1 − e^(−√(r/t)/16)) | V |
