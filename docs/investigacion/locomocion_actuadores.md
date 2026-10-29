# Fact-check: locomotion, actuators, scaling, real giant robots (sections 2 & 7)

Checked 2026-10-29. Verdicts: CONFIRMED / PARTIALLY / CONTRADICTED / UNVERIFIABLE.
Note: mdpi.com, cob.silverchair.com (JEB), and dspace.mit.edu blocked or rate-limited direct fetches (403/429). I did not work around the blocks. I used the Essex repository copy of the MDPI paper, plus Europe PMC, Crossref, OSTI and arXiv.

---

## 1. Ground reaction force (GRF) and the cited MDPI paper

### 1a. Human GRF magnitudes. Verdict: PARTIALLY (right for running, overstated for walking)
The doc says GRF reaches "2 to 3+ BW" during "trote activo simple o caminata" and single stance. Section 8 also says that in "caminata bípeda normal" GRF is "hasta 2 o 3 veces el peso".
- **Nilsson & Thorstensson 1989**, *Acta Physiol Scand* 136:217–227 (PMID 2782094). 12 men, walking 1.0–3.0 m/s, running 1.5–6.0 m/s. Quote: *"The peak amplitude of the vertical reaction force in walking and running increased with speed from approximately 1.0 to 1.5 b.w. and 2.0 to 2.9 b.w. respectively."* https://pubmed.ncbi.nlm.nih.gov/2782094/ (abstract read via Europe PMC REST)
- **Keller et al. 1996**, *Clin Biomech* 11(5):253–259 (DOI 10.1016/0268-0033(95)00068-2, PMID 11415629). Quote: *"F(z) increased linearly during walking and running from 1.2 BW to approximately 2.5 BW at 6.0 m s(-1)."* Also: *"Slow jogging was associated with a > 50% higher F(z) and G(z) in comparison to walking or fast running."* Elsewhere, Keller's jog at 3 m/s is tabulated at ≈2.10 BW.
- **Conclusion:** walking peaks are about 1.0–1.5 BW (≈1.2 BW typical). Running and jogging peaks are about 2.0–2.9 BW. "2–3× BW" holds for trotting/running only, not walking. In walking, single stance is where the vertical force sits near or below 1 BW, between the two ~1.1–1.3 BW peaks.
- **MuJoCo use:** for walking sims, expect vertical GRF of 1.0–1.5 × m·g. For running or jogging, expect 2.0–2.9 × m·g. Stance foot contacts need a bounded impact transient, so tune `solref`/`solimp`.

### 1b. What the cited MDPI paper actually says. Verdict: PARTIALLY (the paper asserts ~3× without a citation and does not measure GRF)
- Zhang, Yuan, Dong, Sadiq, Zhang, Li (2020). "Structural Design and Kinematics Simulation of Hydraulic Biped Robot", *Appl. Sci.* 10(18):6377, DOI 10.3390/app10186377. Full text from the Essex repository: https://repository.essex.ac.uk/38034/1/Biped%20Robot.pdf (MDPI page https://www.mdpi.com/2076-3417/10/18/6377 returned 403).
- The only GRF statement is in §2.4, p.6, with no supporting reference: *"The maximum ground impact force during human walking and running is about three times the weight of the human body, and there is sufficient safety margin. The loading force is 5 kN."*
- Context: this is a static FE check of joint parts. Material is 45# steel, E = 2.05×10¹¹ Pa, yield 530 MPa, mesh 4.7 mm. Max von Mises stress is ≈22.9 MPa (U-bracket), ≈23.4 MPa (joint axis) and ≈64.8 MPa (joint sleeve) under 5 kN. That is a safety factor of ≈8 against yield.
- Robot: NWPUBR-1, 12 DOF (3 hip, 1 knee, 2 ankle per leg), hydraulic cylinders with FF102 flow servo valves, 4 × 300 kg load cells per sole. The simulated model weighs **27.13 kg**, is **1.42 m** tall, and has its CoM at **0.76 m**. Step 0.5 m, stride width 0.25 m, swing height 0.05 m, friction μs = 1, μk = 0.8. The paper uses 3D-LIPM + ZMP in MATLAB. It contains no dynamics or GRF measurement, and the knee link lengths are 385 mm (thigh) and 72 mm.
- **Conclusion:** the doc's footnote 1 is a weak source for its claim. The paper only asserts "about 3× BW for walking and running", which is itself wrong for walking per 1a. Nor is the paper a "macro-análisis estadístico empírico", as the doc calls it.

---

## 2. Inertia and actuator torque scaling

### 2a. I ∝ L⁵ under geometric similarity. Verdict: CONFIRMED (as an isometric identity)
- I ∝ m·L² ∝ L³·L² = L⁵. **Oke, Carter, Gu, Man, Pride, Bergbreiter, Johnson, "Allometric Scaling Laws for Bipedal Robots", arXiv:2603.22560** (v1 March 2026, v5 Sept 2026): rotational arguments "predict joint torque demands on the order of τ∝mL²∝L⁵" (isometric). https://arxiv.org/abs/2603.22560

### 2b. The "required torque ∝ L⁵" framing. Verdict: PARTIALLY (true only at constant angular acceleration, which is not the natural scaling)
- The doc keeps α constant ("misma agilidad"). Under **dynamic similarity** (equal Froude number), time scales as √(L/g), so α ∝ 1/L and **τ ∝ I·α ∝ mL**, which is **L⁴** isometrically. The gravitational torque m·g·L is also ∝ L⁴.
- Oke et al. 2026: torque needed for walking "scales with mL". In their simulations (done in **Drake**, not MuJoCo), with m ∝ L³ they fit τ ∝ L^3.90 (Zippy) and L^4.07 (Mugatu). With m ∝ L² they get τ ∝ L^2.92 and L^3.49. Their survey of real robots finds **biped mass ∝ L^1.91 (n = 20, R² = 0.59)**, lower-body bipeds ∝ L^1.95 (R² = 0.96), and quadrupeds ∝ L^2.72 (R² = 0.93). Real robots are therefore not built isometrically.
- They also confirm v ∝ L^0.5 (Froude number held constant) and that walkable foot dimensions scale ≈ linearly with leg length.

### 2c. Available actuator torque "between L² and L³". Verdict: PARTIALLY / CONTRADICTED (it understates torque scaling and mixes up force and torque)
- Oke et al. 2026 §I-A collect the literature. Theoretical motor models range from **τ ∝ L^3.5** (Caprari 2001; Haddadin 2012), through **τ ∝ L⁴** (Honsinger 1987; Chatzakos & Papadopoulos 2008; Reichert, Nussbaumer & Kolar 2009), to **τ ∝ L⁵** (Spletzer 1999; Caprari), "depending on assumptions about magnetic loading, current density, and cooling". Empirical exponents are **L³** (Dermitzakis et al. 2011, "Scaling laws in robotics", Procedia CS), **L^3.5** (Waldron & Hubert 2000, "Scaling of robotic mechanisms", ICRA, pp. 40–45), **L^3.8** (Dermitzakis 2011; Seok et al. 2015 MIT Cheetah; Saerens et al. 2020, "Scaling laws for parallel motor-gearbox arrangements", IROS), **L⁴** (Kenneally, De & Koditschek 2016) and L⁵ (Spletzer).
- Dermitzakis et al. (as cited in secondary sources): maximum motor torque ∝ mass^1.00 to mass^1.27 in two motor groups. That is L³ to L^3.8.
- **Hydraulics:** force = p·A ∝ L² at fixed pressure, so the doc's L² is correct for *force*. Joint **torque** = F × lever arm ∝ **L³**.
- **Net:** isometric requirement ≈ L⁴ versus available ≈ L³ (hydraulic, fixed pressure) to L^3.5–L⁴ (electric, heat-limited to ideal). The deficit grows only as **~L^0–L^1**, not L² to L³. It is a power law; the doc calls it "exponencial", which is wrong. The direction of the doc's argument is right, but its size is exaggerated.
- I could not obtain the full text of Hollerbach, Hunter & Ballantyne 1991. It is known from citing works as a force/mass and power/mass comparison of motors, hydraulics, SMA and muscle. **UNVERIFIABLE** for specific numbers.

---

## 3. Dynamic similarity, Froude number, and animal scaling

### 3a. Froude number and gait. Verdict: CONFIRMED (supports the analysis; the doc does not address it)
- Fr = v²/(g·L_leg). Humans and other bipeds switch from walking to running at **Fr ≈ 0.5**. **Kram, Domingo & Ferris 1997**, *J Exp Biol* 200:821–826 (PMID 9076966): bipeds switch "at approximately the same Froude number (0.5)", and in reduced gravity the transition happened "at progressively slower absolute speeds but at approximately the same Froude number".
- Preferred walking speed is around **Fr ≈ 0.25**, where potential/kinetic energy exchange is optimal (Sci Rep 2016, srep28825 / PMC4933880: "In humans, Fr is ~0.25 at preferred speed, and ~0.5 at" the walk-run transition). Caveats: preferred Fr falls in larger species, and Donelan & Kram showed Fr is "necessary but not sufficient" for dynamic similarity.
- Under dynamic similarity, speed ∝ √(gL) and stride or step period ∝ √(L/g).

### 3b. Biewener: posture, EMA and constant bone stress. Verdict: CONFIRMED (also refutes "nature cannot hack the law, only thickens bones")
- **Biewener 1989**, *Science* 245:45–48, DOI 10.1126/science.2740914. Quotes: "peak bone stress is independent of size"; "small animals run with crouched postures, whereas larger species run more upright"; "By adopting an upright posture, large animals align their limbs more closely with the ground reaction force"; this "likely limits the maneuverability" of large animals.
- **Biewener 2005**, *J Exp Biol* 208:1665–1676, DOI 10.1242/jeb.01520. Limb EMA increases ∝ body weight^0.25. Bone and muscle stresses stay roughly constant "across a size range 0.04-300 kg". "Above this size, extremely large mammals exhibit more pronounced skeletal allometry and reduced locomotor ability."
- Bone safety factors are **2–4**: peak locomotor stresses are 25–50% of failure strength. Peak compressive stresses are typically **−40 to −80 MPa** (mean −55 ± 23 MPa), and up to −80 to −110 MPa when galloping or jumping (Biewener lab summaries and JEB 1983 papers).
- **Implication for the doc:** animals do not hold stress constant mainly through thicker bones (the doc's §2 claim). Up to ~300 kg they do it mainly by **changing posture and mechanical advantage**. Above that size they add skeletal allometry and slow down. The doc's statement is incomplete rather than wrong.

### 3c. Elephants and sauropods. Verdict: CONFIRMED (supports the doc's thesis)
- **Elephants** (Hutchinson et al. 2003 *Nature*; JEB 2006). Asian elephants reached **≈6.8 m/s**, Fr up to 3.4, and duty factors down to 0.37, but they never adopt a gallop or a whole-body aerial phase. The 2006 study finds a mechanics change near Fr ≈ 1. https://www.sciencedaily.com/releases/2003/04/030404071405.htm , https://spot.colorado.edu/~kram/elephants.pdf
- **Sauropods.** Sellers et al. 2013, "March of the Titans", *PLoS ONE* 8(10):e78733 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3864407/):
  - Argentinosaurus is modelled at **83,230 kg** (literature range 60–88 t), 7.3 m at the shoulder.
  - The most efficient gait had a **2.8 s cycle**; tested cycles ran 1.0–4.0 s, and natural limb periods were 3.1 s (forelimb) and 3.7 s (hindlimb).
  - Max speed is "equivalent to a human with 0.9 m leg length walking at 1 ms−1", i.e. Fr ≈ 0.11. That works out to **≈2.1–2.4 m/s** for a 4–5 m hip height; this is my derivation, not the paper's.
  - "restricting the joint ranges of motion is necessary". The best-estimate ROM model "was never able to generate a cyclic walking gait".
- **Alexander 2006 review** (PMC1634776): trackway speeds are generally "<4 m s−1 for bipedal dinosaurs and 2 m s−1 for sauropods". Apatosaurus (35 t) "may have been about as athletic as an elephant", based on a strength indicator that scales ∝ mass^−0.33 under geometric similarity.
- **Takeaway:** the largest walkers known (50–80+ t) walk slowly at low Fr, with restricted joint ranges and upright columnar limbs. This supports the doc's §2 argument.

### 3d. Galileo 1638. Verdict: CONFIRMED
- *Discorsi… intorno a due nuove scienze* (Leiden 1638) contains the square-cube argument for bones and ships. https://arxiv.org/pdf/physics/0110031 ("Galileo's Discovery of Scaling Laws").

---

## 4. MIT Cheetah 3 "vectorizing its elastic spine". Verdict: CONTRADICTED (based on all available evidence)
- Cheetah 3 papers: Bledt et al., IROS 2018 (https://dspace.mit.edu/handle/1721.1/126619) and Di Carlo et al., IROS 2018, "Dynamic Locomotion in the MIT Cheetah 3 Through Convex MPC" (https://dspace.mit.edu/handle/1721.1/138000).
  - The robot is a **45 kg** quadruped. The design contribution is the **leg**: "proprioceptive actuation on the abduction/adduction degrees of freedom in addition to an expanded range of motion on the hips and knees".
  - The MPC uses a simplified "3D, 12 DoF model", i.e. the 12-state single rigid body. It reaches 3 m/s forward and 180°/s yaw, with gaits including a 3D gallop. Lowest CoT is 0.45 (trot).
  - Neither abstract nor the MIT News article (https://news.mit.edu/2018/blind-cheetah-robot-climb-stairs-obstacles-disaster-zones-0705, "90-pound", Labrador-sized) mentions a spine. The full PDFs were rate-limited (HTTP 429), so the claim of a rigid torso with no spine joint rests on these descriptions plus the rigid-body MPC model.
- **What did have a spine:** the earlier **MIT Cheetah I** (2012–13) had "a spine composed of rigid vertebrae interspersed with polyurethane rubber rings", coupled to the hind legs through a differential (Jiang et al. 2024, *Biomimetics* 9(3):132, PMC10968056; Folkertsma, Kim & Stramigioli, IROS 2012, "Parallel stiffness in a bounding quadruped with flexible spine": parallel springs cut power by >50%). Boston Dynamics' DARPA "Cheetah" (hydraulic, tethered, treadmill) also flexed its back.
- Real cheetahs do flex and extend the spine to lengthen the stride (Hildebrand 1959/1961; the 1961 correction puts the speed benefit at about 6 mph).
- **Fix for the doc:** say "MIT Cheetah I / BD Cheetah" or "biological cheetahs". Cheetah 3, Mini Cheetah, Spot and ANYmal use rigid trunks.

---

## 5. Hydraulic efficiency, EHA efficiency, power density, Atlas

### 5a. Servo-valve or valve-controlled hydraulics "sometimes <30%". Verdict: CONFIRMED (often much lower)
- **ORNL/TM-2011/14**, Love, Lanke & Alles (2012), "Estimating the impact (energy, emissions and economics) of the US fluid power industry" (https://info.ornl.gov/sites/publications/files/pub28014.pdf):
  - "fluid power system efficiencies range from less than 9% to as high as 60% (depending upon the application), with an average efficiency of 22%."
  - "a typical mobile hydraulic powered systems have an overall efficiency of approximately 14%."
  - Losses come from valve tare leakage and "metering losses associated with pressure drops across the valves… much like using resistors to control electric motors". Pump efficiency approaches 90% ideally but drops "well below 75%" under time-varying loads.
- **Hagen, Padovani & Choux 2019**, *Actuators* 8(4):78, DOI 10.3390/act8040078. The valve-controlled constant-pressure system runs at about **22%** overall efficiency, versus about **57%** for the self-contained electro-hydraulic cylinder during actuation. The abstract reports "62% energy savings", up to 77% usable energy with recovery, and >20% recovered energy.
- Aircraft study (MDPI *Actuators* 13(4):118): valve-controlled actuator losses are mainly servo-valve throttling plus internal leakage. EHA losses are mainly motor copper loss.

### 5b. EHA efficiency ">70%". Verdict: PARTIALLY (achievable as peak; typical operating points are 30–60%)
- **Du, Zhou, Zhao, Ma 2024**, *Energy* 291:130417, DOI 10.1016/j.energy.2024.130417. EHA for a wheel-legged robot joint: "a drive efficiency of up to 87 %" and "an energy recovery efficiency of up to 88 %". The main loss is pressure drop in the circuit. https://ideas.repec.org/a/eee/energy/v291y2024ics0360544224001889.html
- **Du et al. 2026**, *Tribology International* 223:112258, DOI 10.1016/j.triboint.2026.112258. In the efficiency map, "The majority fall in the 30%-60% interval", with maximum efficiency >70%. Model error is <5%. https://pure.bit.edu.cn/en/publications/high-fidelity-modeling-and-thermal-efficiency-performance-of-an-e/
- A Moog vendor case (Ampelmann gangway) needed 300 kW valve-controlled versus 30 kW with an electro-hydrostatic system. This is a vendor claim.
- **Doc fix:** "eficiencias pico de 70–87%, típicamente 30–60% en ciclo de trabajo de robot."

### 5c. Pressures, power and force density, Atlas specs
- **Typical robot hydraulic pressure is about 20.7 MPa (3000 psi).**
  - IIT HyQ/HyQReal Moog Integrated Smart Actuator: operating pressure 20.7 MPa; valve ratings 21–31.5 MPa; relief at 22 MPa. One ISA actuator unit weighs 0.92–1.3 kg (Frontiers Robot. AI 2018, 10.3389/frobt.2018.00051).
  - HyQReal joint torques at 20 MPa: HAA 165 N·m, HFE 270 N·m, KFE 240 N·m peak. Original HyQ: 120 / 181 N·m peak at 20 MPa, ~90 kg, ~1 m tall.
  - Boston Dynamics patent US 10,533,542 ("Rapidly modulated hydraulic supply for a robotic device"): "high pressures upwards of 3000 psi are maintained in a typical robotic hydraulic system".
  - IHMC Atlas: "electric pump and an accumulator… to maintain a hydraulic fluid at a desired pressure of 2300 PSI" (≈15.9 MPa). Source: Dafarra 2020 PhD thesis, arXiv:2004.07699.
- **Force density, simple physics:** a cylinder at 21 MPa gives 21 N/mm² of piston area, about 60× peak muscle stress. Mammalian muscle is 0.1 MPa sustained and 0.35 MPa peak, with 50 W/kg typical and 284 W/kg max (Madden et al. 2004, *IEEE J. Oceanic Eng.*, Table I).
- **Atlas power unit density:** Boston Dynamics VP Aaron Saunders (IFK 2018) said the hydraulic power unit was "approaching a kilowatt per kg". https://www.fluidpowerworld.com/april-2018-issue-hydraulic-hybrid-powers-fuel-efficient-tug/
- **Atlas specs:**
  - DRC Atlas (2013): ~1.88 m, ~150 kg, tethered.
  - **Atlas-Unplugged (2015):** 1.88 m, **156.5 kg** per IEEE Spectrum, or 182 kg per the Ficht & Behnke review. It carried a 3.7 kWh Li-ion battery, a "variable-pressure pump" with mid-pressure and burst modes, and had about 1 h mixed-mission runtime. https://spectrum.ieee.org/atlas-drc-robot-is-75-percent-new-completely-unplugged
  - **Atlas (2016 and later, hydraulic):** about **1.5 m and 75–80 kg**, 28 hydraulic DOF, custom servo valves, 30–60 min runtime (Fluid Power World 2018; Ficht & Behnke 2021, *Curr. Robot. Rep.*, arXiv:2103.04675). Hydraulic Atlas was retired in 2024. The electric production Atlas was unveiled at CES 2026; its production specs were not found.
- **Hydra (U-Tokyo, whole-body EHA humanoid):** about 1.80–1.85 m, 130–135 kg, 40–41 DOF, each EHA with its own pump. Ficht & Behnke say it is "yet to be optimised for size and weight". Kaminaga et al., ISER 2016.

---

## 6. Real giant walking machines (empirical anchors)

| Machine | Size / mass | Legged locomotion? | Speed | Source |
|---|---|---|---|---|
| **Tradinno** (Zollner Elektronik, 2010) | 15.72 m long × 12.33 m wide × **8.20 m tall**, **11 t** | **Quadruped**, 4 legs × 7 DOF, hydraulic, 2.0 L 140 hp turbo-diesel, radio-controlled | not published | Guinness "largest walking robot", re-posted by GWR in **April 2026**: https://www.guinnessworldrecords.com/news/2013/9/video-fanny-the-fire-breathing-dragon-the-worlds-largest-walking-robot-51369 ; https://en.wikipedia.org/wiki/Tradinno |
| **LW Mononofu** (Sakakibara Kikai, 2017–18) | **8.46 m, ~7.3 t** | Bipedal-looking but **rolls on wheels**: "Mononofu does have wheels but isn't driven by them… uses its pelvis and knees to move forward and backward along the wheels" | <1 km/h; AC 200 V tethered, short battery life | Guinness "Largest humanoid vehicle", 7 Dec 2018: https://www.guinnessworldrecords.com/world-records/515616-largest-humanoid-vehicle ; SoraNews24: https://soranews24.com/2017/12/31/the-tragedy-of-mononofu-the-functional-two-and-a-half-story-bipedal-robot%E3%80%90pics-video%E3%80%91/ ; VOA (<1 km/h) |
| **Gundam RX-78F00** (Gundam Factory Yokohama, 2020–24) | **18 m, 25 t**, 24 joints; 36 DOF total (22 body + 12 hands + 2 carrier) | **No.** It hangs from the waist on the GUNDAM-CARRIER: "2足歩行ではないし、そもそも自分の脚で立ってもいない" ("it is not bipedal and does not even stand on its own legs"). Feet do not bear load. **All actuators electric, no hydraulics**: "アクチュエータはすべて電動で、油圧は使われていない"; high-torque joints use electric cylinders | scripted motions only | https://news.mynavi.jp/article/20201204-1554044/ . Refurbished as a static 17 m statue for Expo 2025 Osaka |
| **METHOD-2** (Hankook Mirae Technology, 2016) | **4 m, ~1.5 t**, arms 130 kg each, piloted | **Yes, bipedal steps**, but tethered by a power cable; balance and power still under development | very slow "baby steps" | https://phys.org/news/2016-12-avatar-style-korean-robot-baby.html |
| **Archax** (Tsubame Industries, 2023–) | **4.5 m, 3.5 t**, ¥400M (~US$2.7M) | **No walking.** Wheeled legs, robot and vehicle modes | 10 km/h vehicle, ~2 km/h robot mode | https://www.malaymail.com/news/tech-gadgets/2023/10/02/japan-startup-develops-gundam-like-robot-with-us3m-price-tag/93907 |
| **Kuratas** (Suidobashi, 2012) | ~4 m, 4–4.5 t (Guinness lists 3.62 t) | No, 4 wheels; diesel; ~30 joints | 10 km/h | https://www.guinnessworldrecords.com/world-records/108652-largest-mecha-robot-controlled-by-smartphone |
| **MegaBots Eagle Prime** (2017) | ~4.9 m (16 ft), ~12 t, 430 hp LS3 V8 | No legs (ground drive; track details not confirmed) | not published | https://spectrum.ieee.org/watch-the-worlds-first-giant-robot-fight |
| **Plustech/Timberjack walking harvester "Plusjack"** (1999) | ~**13 t**, 5.75 × 2.75 × ~4.5 m, foot Ø ~54 cm, step 30–90 cm | **Yes, hexapod**, hydraulic; prototype only (3 built, last donated to the Lusto museum 2011) | slow (no figure found) | https://shvachko.net/?p=1012 (secondary) |
| Largest *humanoid* bipeds that genuinely walk (2025–26) | ~1.5–1.9 m, 40–150 kg (e.g., AgiBot A2 walked 106 km, Nov 2025) | yes | ~1–2 m/s | https://www.guinnessworldrecords.com/news/2026/2/humanoid-robot-stuns-passersby-as-it-walks-over-100-km-across-china-in-big-tech-milestone |

**Takeaways for the doc:**
- No machine above ~1.5 t has demonstrated free, untethered bipedal walking. The largest legged walker is Tradinno, an 11 t quadruped. The largest walking hexapod prototype (Plusjack) was about 13 t.
- Every larger "mecha" (Mononofu 7.3 t, Gundam 25 t) either rolls on wheels or is suspended from a support.
- The Gundam (25 t, all-electric) is a counterexample to the doc's claim (§7) that electric actuation is ruled out at large scale. Electric cylinders moved an 18 m frame, although without bearing weight on its legs.
- Mass compared with isometric scaling from a 1.75 m, 70 kg human (my calculation): Mononofu 0.92×, Gundam 0.33× (hollow shell, supported), Archax 2.9×, Method-2 1.8×, Atlas 1.6–1.8×.

---

## 7. Gyroid TPMS as heat exchanger. Verdict: PARTIALLY (high Nu confirmed; large pressure-drop penalty omitted; gyroid often not the best TPMS)
- **Prussack et al. 2024**, *Applied Thermal Engineering*, DOI 10.1016/j.applthermaleng.2024.123291 (experimental, volumetrically heated gyroid and diamond, air flow; OSTI 2396699, https://www.osti.gov/biblio/2396699):
  - "TPMS geometries showed Nusselt numbers 8–10 times higher than that of the rod bundle"
  - this allows "250–275 % higher power density than the rod bundle for a given centerline temperature"
  - but "The gyroid TPMS presented a friction factor 1.5 times higher than the diamond TPMS and 90 times that of the rod bundle."
- **Chtourou et al. 2026**, *Int. J. Eng. Res. Africa* 80:59–80 (CFD, Re 1000–2500): gyroid gives "a 35.24% enhancement in the Nusselt number" over a smooth channel, and 16.85% better overall performance than a β = 30° chevron plate heat exchanger. https://www.scientific.net/JERA.80.59
- **Reynolds, Fee, Morison, Holland 2023**, *IJHMT* 212:124264, DOI 10.1016/j.ijheatmasstransfer.2023.124264 (experimental, 3D-printed). A secondary review cites it as finding gyroid Nu "112% higher than that of straight tubes", with the lowest friction factor among the TPMS tested. Original abstract not retrieved.
- **Iyer, Moore, Nguyen, Roy, Stolaroff (LLNL) 2022**, *Appl. Therm. Eng.* 209:118192 (OSTI 1846336). The related LLNL patent says **Schwarz-D**, not gyroid, has the highest Nu. At fixed pressure drop it matches a tubular heat exchanger's duty "in an order of magnitude smaller volume".
- **Liu et al. 2024**, *Energies* 17:5141: gyroid, diamond and Split-P are "nearly identical when the surface-to-volume ratio is kept constant". The recommended operating point is ~0.3 m/s, Re 300–800.
- **Doc fixes:**
  - The "high Nusselt number" claim is supported.
  - "Disipando excepcionalmente todo efecto de estrangulamiento termal" ignores the 10–90× friction-factor penalty, i.e. pumping power. That matters a great deal for viscous EHA oil inside a load-bearing lattice.
  - A gyroid is **not a fractal**.
  - "Nusselt de absorción convectiva transitoria" is not a standard term.

---

## 8. Numbers for the MuJoCo model (scale factor s relative to a 1.75 m / 70 kg / 0.90 m-leg human)

Isometric rules: length ∝ s, mass ∝ s³, I ∝ s⁵. Under dynamic similarity: time ∝ s^0.5, v ∝ s^0.5, ω ∝ s^−0.5, α ∝ s^−1, required torque ∝ s⁴, power ∝ s^3.5, GRF ∝ s³, stress ∝ s. Available hydraulic torque at fixed pressure ∝ s³, so the deficit ∝ s.

| s | Height | Mass (iso) | I rel. | v @Fr 0.25 | v @Fr 0.5 (walk-run) | Period × | τ req × | Power × | Stress × |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.75 m | 70 kg | 1 | 1.49 m/s | 2.10 m/s | 1.00 | 1 | 1 | 1 |
| 2.5 | 4.4 m | 1.09 t | 98 | 2.35 | 3.32 | 1.58 | 39 | 25 | 2.5 |
| 4.83 (Mononofu) | 8.45 m | 7.9 t | 2.6e3 | 3.27 | 4.62 | 2.20 | 544 | 248 | 4.8 |
| 10 (Gundam) | 17.5 m | 70 t | 1e5 | 4.70 | 6.64 | 3.16 | 1e4 | 3.2e3 | 10 |
| 20 | 35 m | 560 t | 3.2e6 | 6.64 | 9.40 | 4.47 | 1.6e5 | 3.6e4 | 20 |

Sanity anchors:
- Sauropod gait cycle ≈ 2.8 s, with speed ≈ Fr 0.11 (Sellers 2013).
- Elephant top speed 6.8 m/s without an aerial phase.
- Human vertical GRF: walking 1.0–1.5 BW, running 2.0–2.9 BW.
- Bone safety factor 2–4.
- Hydraulic supply 15.9–20.7 MPa (2300–3000 psi).
- EHA efficiency 30–60% typical, 70–87% peak.
- Valve-controlled hydraulics ≈ 22% average (14% mobile).

Real robots scale as m ∝ L^~2 rather than L³ (Oke 2026), so a "realistic" heavy-robot sweep might use m ∝ s^2–2.5 rather than s³.

---

## Summary of verdicts
| Claim (doc) | Verdict |
|---|---|
| GRF 2–3+ BW in trot *or walking* | PARTIALLY: running 2.0–2.9 BW is right; walking is 1.0–1.5 BW |
| MDPI 6377 supports the GRF claim | PARTIALLY: it asserts "about three times" for walking and running, with no citation and no measurement |
| I ∝ L⁵ | CONFIRMED (isometric) |
| Required torque ∝ L⁵ | PARTIALLY: only at constant α; under dynamic similarity it is ∝ mL ∝ L⁴ |
| Actuator torque ∝ L²–L³ | PARTIALLY/CONTRADICTED: hydraulic force ∝ L² but torque ∝ L³; electric L³–L⁴ (theory up to L⁵); the gap is ~L^0–1, and "exponential" is a misnomer |
| Giants have massive columnar limbs | CONFIRMED, but up to ~300 kg posture and EMA, not bone thickness, keep stress constant (Biewener) |
| Cheetah 3 uses an elastic spine | CONTRADICTED: Cheetah 3 has a rigid torso (rigid-body MPC); MIT Cheetah I had a flexible spine |
| Servo-valve hydraulics sometimes <30% | CONFIRMED (22% average, 14% mobile, as low as <9%) |
| EHA >70% net | PARTIALLY: 70–87% peak, 30–60% typical |
| Gyroid gives high Nusselt numbers | PARTIALLY: confirmed, but with a large friction penalty, and diamond / Schwarz-D are often as good or better |
| No agile building-sized humanoids exist | CONFIRMED: the largest walker is Tradinno (11 t quadruped); 7–25 t "mechas" roll or are suspended |
