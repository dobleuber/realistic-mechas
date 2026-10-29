# Fact-check: section 8, geotechnics and very large machines

Checked 2026-10-29. In the doc, footnote numbers map to sources as follows: [2] Tensar, [3] outriggerpads (never cited in the body text), [4] Worldbuilding SE Q218215, [5] RICO Europe, [6] MDPI bogie paper. Footnote [4] carries the soil table, the "stadium-sized feet" claim, and the 574 kPa granite figure.

## 0. Bottom line

| Doc claim (section 8) | Verdict | Short reason |
|---|---|---|
| Soil and rock values (95 / 144 / 239 / 287 / 574 kPa) "well documented" | **CONFIRMED as sourced, but mislabelled.** | They are the **allowable presumptive design values** of the 1995 CABO One- and Two-Family Dwelling Code (2,000 / 3,000 / 5,000 / 6,000 / 12,000 psf). They are not failure values. The current IBC uses 1,500 / 2,000 / 3,000 / 4,000 / 12,000 psf. |
| Bearing capacity is "absolute", the pressure "before catastrophic shear failure" | **PARTIALLY** | That definition fits *ultimate* capacity. Allowable is ultimate ÷ FS (about 3), and settlement also limits it. Capacity is not absolute: it depends on footing size, depth, water table and loading rate. |
| 574 kPa = "resistencia máxima del granito puro" | **CONTRADICTED** | 574 kPa is 12,000 psf, the code's no-testing presumptive *allowable* value for crystalline bedrock. NYC allows 5,746 kPa on hard sound rock and Hong Kong allows 10,000–12,500 kPa on fresh granite. Intact granite UCS is 100 to >250 MPa. |
| A frigate-mass mech would exceed 574 kPa at each step | **CONFIRMED (arithmetic)** | 6,700–7,300 t on a human-proportioned 50 m mech foot (about 20 m²) gives 3.2–3.5 MPa static and 6–10 MPa at 2–3× GRF. |
| …and so would "break the Earth's crust / perforate the rock" | **CONTRADICTED** for sound rock | 6–10 MPa is the same order as code *allowable* values for sound rock (5.7–12.5 MPa) and far below intact UCS. On soils it would cause bearing failure and sinking (that part is plausible). "Crust" is hyperbole. |
| Feet "as big as football stadiums" (attributed to [4]) | **CONTRADICTED / unsupported** | [4] never says this. Its only answer (70 t mech) says the feet need to be "about 90% longer and wider" to walk on clay and ">3× as long and wide" to run. My own check: 14,200 t at 2.5× GRF on 96 kPa needs about 3,600 m² per foot (≈60×60 m, half a soccer pitch). A 5,000 t mech needs about 850–1,300 m². That is enormous, but not stadium-sized. |
| Bagger 293: 96 m, 14,200 t | **CONFIRMED** | MDPI paper and Wikipedia. Entered service 7 Jul 1995 at Hambach. |
| Bagger 293 has "12 bogies gigantescos" | **PARTIALLY** | It has **12 crawlers (Raupen)**, and each one rides on multi-wheel bogies. The cited MDPI paper studies a generic eight-wheel bogie (Serbian BWEs) and gives no count for Bagger 293. |
| Bagger 293 avoids sinking by spreading its weight | **CONFIRMED (qualitatively)** | Its sister machine Bagger 288 runs at about 171 kPa nominal ground pressure. That is already above the IBC/CABO presumptive values for sand and gravel, which shows those values are not failure limits. |

---

## 1. IBC Table 1806.2 "Presumptive load-bearing values"

Source: 2025 California Building Code (IBC-based) §1806 via gocodebook: https://gocodebook.com/library/us/ca/ca-building-code/chapter-18-soils-and-foundations/section-1806-presumptive-load-bearing-values-of-soils. The ICC site (codes.iccsafe.org) returned 403. The same values appear in IRC Table R401.4.1 (Massachusetts 2015 IRC, reproduced in the CUNY CityTech PDF below).

| Class (IBC 1806.2) | Vertical (psf) | kPa (×0.04788) |
|---|---|---|
| 1. Crystalline bedrock | 12,000 | **574.6** |
| 2. Sedimentary and foliated rock | 4,000 | 191.5 |
| 3. Sandy gravel and gravel (GW, GP) | 3,000 | **143.6** |
| 4. Sand, silty sand, clayey sand, silty gravel, clayey gravel (SW, SP, SM, SC, GM, GC) | 2,000 | 95.8 |
| 5. Clay, sandy clay, silty clay, clayey silt, silt, sandy silt (CL, ML, MH, CH) | 1,500 | 71.8 |

Footnotes: lateral bearing 1,200 / 400 / 200 / 150 / 100 psf/ft; friction coefficients 0.70 / 0.35 / 0.35 / 0.25; cohesion 130 psf for clay.

- **They are allowable values for ASD.** §1806.1 says they are used with allowable-stress-design load combinations and "shall be permitted to be increased by one-third" for wind or earthquake. §1806.2 says they cap capacity "unless data to substantiate the use of higher values are submitted and approved". Mud, organic soils, peat and undocumented fill get no presumptive value.
- **12,000 psf ≈ 574.6 kPa, which matches the doc's 574 kPa.**
- **144 and 239 kPa are not the current IBC sand and gravel classes.** They come from the older **CABO 1995 Table 401.4.1**: crystalline bedrock 12,000, sedimentary rock 6,000, sandy gravel or gravel 5,000, sand/silty sand/clayey sand/silty gravel/clayey gravel 3,000, clay/sandy clay/silty clay/clayey silt 2,000 psf. In kPa that is 574.6 / 287.3 / 239.4 / 143.6 / 95.8, exactly the five values in the SE answer the doc cites. The CUNY CityTech teaching PDF reproduces this table with "Source: Table 401.4.1; CABO One- and Two-Family Dwelling Code; 1995", next to the current IRC R401.4.1 (12,000 / 4,000 / 3,000 / 2,000 / 1,500): https://openlab.citytech.cuny.edu/bt2-2020f/files/2020/03/Foundation-CalculationsS.pdf. LSU AgCenter reproduces the same 1995 table (seen in search results; the page failed TLS verification).
- Note the label mismatch: the SE answer calls 144 kPa "sand or sand gravel mixture" and 239 kPa "gravel". In CABO, 3,000 psf is sand/silty sand and 5,000 psf is sandy gravel/gravel. The doc's labels ("arcilla blanda o arena suelta", "arena mezclada con grava compactada") add further imprecision. Soft clay and loose sand normally get *no* presumptive value or <75–100 kPa.
- **Factor of safety.** Tensar [2]: net safe bearing capacity "qₙₛ = qₙᵤ / F", "F is typically 3", and allowable is "always lower than the ultimate bearing pressure" because settlement is also checked. USACE EM 1110-1-1905 (via PDH Online): "FS will typically be between 2 and 4" (https://pdhonline.com/courses/c119/c119_new.htm). NYC Notes 4 and 6 require FS ≥ 2.0 against shear failure for soils and clays. Presumptive values are also set conservatively to limit settlement (about 25–30 mm for buildings), so the real ultimate capacity is commonly 3× or more the presumptive value.

## 2. Ultimate vs allowable capacity, rock, and other codes

**Granite strength (intact rock UCS):**
- Marinos & Hoek 2000, Table 1 (after Brown 1981): **R6 "Extremely strong" >250 MPa**, examples "Fresh basalt, chert, diabase, gneiss, granite, quartzite". R5 "Very strong" is 100–250 MPa. https://www.rocscience.com/assets/resources/learning/hoek/GSI-A-Geologically-Friendly-Tool-for-Rock-Mass-Strength-Estimation-2000.pdf
- Measured values: Soultz granite, mean intact UCS 140 MPa; Mórágy granite (Hungary), 133–213 MPa (search results: https://fe.up.pt/isrm-wsr2025/wp-content/uploads/2025/05/250516_Paper-Granite-Rocks.pdf and https://reference-global.com/article/10.2478/sgem-2019-0010).
- So 574 kPa is **about 0.2–0.5 % of intact granite UCS**.

**Allowable bearing on sound rock in other codes:**
- **NYC Building Code 2022, Table 1806.1 "Allowable bearing pressures"** (primary source): 1a Hard sound rock (gneiss, granite, diabase, mica schist; RQD ≥ 85 %) **60 tsf = 5,746 kPa**. 1b Medium rock 40 tsf = 3,830 kPa. 1c Intermediate rock 20 tsf = 1,915 kPa. 1d Soft rock 8 tsf = 766 kPa. Soils: dense gravel 958 kPa, medium gravel 575 kPa, dense granular 575 kPa, medium granular 287 kPa, hard clay 479 kPa, stiff clay 287 kPa, medium clay 192 kPa, medium silt 144 kPa. Class 1a may rise 25 % with tests, and +10 %/ft embedment up to 200 %. https://www.nyc.gov/assets/buildings/codes-pdf/cons_codes_2022/2022BC_Chapter18_SoilsFoundationsWBwm.pdf
- **Hong Kong GEO TGN 53, Issue 2 (17 Apr 2026), Table 2, igneous rocks** (primary source):
  - 1(a) "Fresh to slightly decomposed strong to very strong granite… UCS ≥ 75 MPa", 100 % TCR: **12,500 kPa**
  - 1(b) UCS ≥ 50 MPa: 10,000 kPa
  - 1(c) UCS ≥ 25 MPa: 7,500 kPa
  - 1(d) moderately decomposed: 3,000 kPa
  - Settlement must also be checked, and the allowable value "should not exceed the uniaxial compressive strength of the intact rock".
  - Table 1, non-cohesive soils: very dense (N>50) 500 kPa, dense 300, medium dense 100, loose <100 kPa.
  - https://www.cedd.gov.hk/filemanager/eng/content_427/TGN%2053_Issue%202.pdf
- **Massachusetts 780 CMR** (search snippet; the page itself was bot-blocked): Class 1a massive bedrock (granite, diorite, gabbro, basalt, gneiss) **100 tons/ft² ≈ 9.6 MPa** net allowable. https://www.mass.gov/doc/10th-edition-chapter-18-soils-and-foundations/download
- **BS 8004:1986 / EC7 Annex G**: these derive rock values from UCS and discontinuity spacing charts. A Sri Lankan IESL paper (seen in search) reports 10 N/mm² (10 MPa) allowable for gneiss with RQD > 75 %. Hong Kong CEDD Appendix J notes that EC7 Annex G's method "is identical to that in BS 8004:1986". I could not open the BS 8004 table itself; the commonly quoted values are 10,000 kPa for "strong igneous and gneissic rocks in sound condition" and 4,000 kPa for strong limestone and sandstone, which I'd mark as **unverified** here.
- **Canadian Foundation Engineering Manual**: no accessible copy, so **UNVERIFIABLE**.
- **Is "exceeding 574 kPa breaks the Earth's crust" fair? No.** 574 kPa is a deliberately conservative *allowable* number for building on unexamined bedrock without a geotechnical report. Codes allow 10–22× that on sound granite, and intact granite fails in compression at 100–250+ MPa. Exceeding an allowable value means "outside code design envelope", not failure. Even a local bearing failure in rock would be a crushed or punched zone under the foot, not anything to do with "the crust".

**Ultimate bearing capacity of soils (for the simulation):**
- Clay (undrained): q_ult ≈ Nc·cu, with Nc = 5.14 for a strip (IS 6403 Table 1, via search) and about 6.2 for circular or square footings. Falkingham et al. 2011 give the worked example "a substrate for which Cu = 100 kN m⁻² will fail when the load on a circular indenter" reaches **616.8 kN/m²** (PMC3119880). This term is independent of foot size.
- Sand: q_ult includes 0.5·γ·B·Nγ, which **grows linearly with foot width B** (Vesić Nγ ≈ 48 at φ = 35°). My own estimate for a dense sand surface footing (γ = 18 kN/m³, square shape factor 0.6): B = 1 m ≈ 260 kPa, 5 m ≈ 1.3 MPa, 10 m ≈ 2.6 MPa. Large feet on granular soil therefore gain capacity, which partly offsets the square-cube problem. Settlement still grows with B. The doc ignores this size effect.
- BGS/BS 5930 terms (https://earthwise.bgs.ac.uk/index.php/OR/15/065_Appendix_2_-_Strength,_consistency_and_density_classification_terms_and_descriptions):
  - Rock UCS: extremely strong 250+, very strong 100–250, strong 50–100, medium strong 25–50, weak 5–25, very weak 1–5 MPa.
  - Soil "strength": very soft <0.04, soft 0.04–0.08, firm 0.08–0.15, stiff 0.15–0.3, very stiff 0.3–0.6 MPa. The page doesn't say whether these are cu or UCS.
  - SPT density: very loose <4, loose 4–10, medium dense 10–30, dense 30–50, very dense 50+.

## 3. Dynamic and short-duration loading; real ground pressures

**Codes and rate effects:**
- IBC §1806.1 allows a one-third increase in presumptive values for wind and seismic (transient) combinations. That is a code acknowledgement that short loads may use higher values.
- Undrained shear strength of clays rises about **10 % per tenfold (log-cycle) increase in strain rate** (Kulhawy & Mayne default). Measured range is about 4–17 % per log cycle: Vicksburg 6 %, Lyndhurst 17 %, kaolin 10–16 %, compacted clay 4.1–9.7 % (search summary of ORA Oxford / Dundee / ASCE papers, e.g. https://discovery.dundee.ac.uk/ws/files/157818073/s11440-025-02797-3.pdf).
- For short dynamic loads, "the allowable pressure… mainly depends on the deformations caused by the applied load" (ISET paper, https://iset.org.in/journal/dynamic-bearing-capacity-of-soils-under-transient-loading/). In practice, sinkage per step and accumulated settlement or ratcheting govern, not a single pressure threshold.
- The 1960s US Army Corps of Engineers "Dynamic bearing capacity of soils" series found impulsive footing tests "did not appear to fit classical failure theories" (https://apps.dtic.mil/sti/pdfs/AD0680905.pdf, via search).
- **Conclusion:** a step lasting about 1 s gets roughly +20–40 % in clay from rate effects. Sand under fast loading can drop slightly (punching), and saturated loose sand risks liquefaction. There is no basis for treating the static presumptive value as an instantaneous failure trigger.

**Measured contact and ground pressures:**

| Object | Pressure | Source |
|---|---|---|
| Human standing, flat shoes (average) | 17 kPa | Wikipedia "Ground pressure" (Thompson & Sorvig 2000): https://en.wikipedia.org/wiki/Ground_pressure |
| Human, 130 kg, one foot | 55 kPa | Wikipedia (same) |
| Human walking, barefoot **local peaks** (healthy controls) | heel **294 kPa**, 2nd metatarsal 293, 3rd–5th met 252, hallux 233, 1st met 212, midfoot 95 | Stewart et al. 2016, J Foot Ankle Res, Table 4, PMC4851792 |
| M1 / M1A1 / M1A2 Abrams (nominal) | 13.3 / 14.4 / 15.4 psi = 92 / 99 / **106 kPa** (GlobalSecurity: 13.1 / 13.8 / 15.4 psi) | https://mathscinotes.com/2016/06/tank-track-ground-pressure-examples (citing afvdb); Wikipedia gives M1 103 kPa |
| Leopard 2 (55.15 t) | **0.83 kg/cm² = 81 kPa** | FAS: https://man.fas.org/dod-101/sys/land/row/leopard2.htm |
| Tiger I | 15.6 psi = 108 kPa | mathscinotes |
| Passenger car (≈ tyre inflation) | 205 kPa | Wikipedia "Ground pressure" |
| Truck tyres | design 700 kPa (Malaysia); measured up to 827 kPa; local peak about 2× inflation | https://uitm.academia.edu/HHARON, https://trid.trb.org/View/277356 |
| Aircraft tyres on pavement, ICAO ACR/PCR codes | W unlimited, X ≤ 1.75 MPa, Y ≤ 1.25 MPa, Z ≤ 0.50 MPa | FAA AC 150/5335-5D (2022) and ICAO material, via search; https://en.wikipedia.org/wiki/ACR-PCR_method |
| Bagger 288 | 1.71 bar = **171 kPa** (Wikipedia, uncited); Wikipedia "Ground pressure" table gives 170 kPa | https://en.wikipedia.org/wiki/Bagger_288 |
| TAKRAF SRs 8000 (240,000 m³/day class BWE) | average 17.5 N/cm² ≈ 175 kPa (catalogue prints "N/cm³", a typo; seen in search, page 403) | https://pdf.directindustry.com/pdf/takraf/bucket-wheel-excavator-srs-8000/58547-220763.html |
| Liebherr LR 1100.1 crawler crane | 1.14 kg/cm² ≈ 112 kPa (nominal, from search) | Liebherr datasheet via search |
| Liebherr LR 13000 crawler crane (one P-boom configuration) | reported "70-tonnes per square meter" ≈ 690 kPa | Lift & Access / Crane Hotline customer-days report: https://www.liftandaccess.com/article/liebherr-launches-telecrawler-and-cranes-customer-days. Not a datasheet value; crane pressures depend strongly on configuration. |
| African elephants, 1.5–3 t, walking 1.1–1.3 m/s | per-foot **mean maximum pressure 200–318 kPa**; mean local peaks 946 kPa (Asian elephants: 567 kPa) | Panagiotopoulou et al. 2016, R Soc Open Sci, Table 1, PMC5098964 |
| Adult elephant (static, generic) | 240 kPa | Wikipedia "Ground pressure" |

**Tensar [2]** (https://www.tensarinternational.com/resources/articles/bearing-capacity-of-soil):
- "Typical soil bearing capacity values" table of *safe* bearing capacity: soft clay <75, firm clay 75–100, loose gravel <200, dense gravel 200–600 kPa.
- Definitions: ultimate capacity is the maximum pressure before shear failure, and allowable is lower because it also covers settlement. F is typically 3.
- The page does **not** list 144 / 239 / 574 kPa and does not call bearing capacity "absolute".

**Outriggerpads [3]** (https://outriggerpads.com/understanding-ground-bearing-capacity-for-safe-equipment-operations/, dated 30 Apr 2025, no author):
- Table in PSI: loose sand 0.5–2, soft clay 1–2, firm soil 2–4, compacted gravel 5–12, asphalt/concrete 100+ psi. That is roughly 3–14, 7–14, 14–28, 34–83 and ≥690 kPa.
- The sizing steps contradict the table: soft soil 500 psf (24 kPa), compacted gravel 3,000+ psf (144 kPa), concrete 4,000+ psf (192 kPa), worked example 2,000 psf.
- **Internally inconsistent and not a reliable numeric source.** The doc does not cite [3] anywhere in the body text.

**Concrete and pavement:**
- Highway pavement concrete is typically **28–40 MPa** compressive (Alabama DOT spec: f'c ≥ 4,000 psi ≈ 27.6 MPa, flexural ≥ 650 psi ≈ 4.5 MPa; https://www.dot.state.al.us:443/publications/Construction/pdf/Specifications/2012/GASPSummary/12-0152.pdf, via search).
- A slab spreads load, so the governing limit is slab flexure and punching plus subgrade bearing, not concrete crushing.
- Roads routinely carry 0.7–0.85 MPa truck tyre contact, and airport pavements carry up to 1.75 MPa (code X).
- The doc's "hundiría sus extremidades en el pavimento" for a 50 m mech: plausible in the sense of slab or subgrade failure at several MPa, but not "sinking into the pavement like mud".

## 4. Bagger 293 (and 288)

- **Vulović et al. 2023, Metals 13(3):466, "Strength Analysis of Eight-Wheel Bogie of Bucket Wheel Excavator"** (doi 10.3390/met13030466, PDF via mdpi-res.com) says: "Bagger 293 is 96 m high, 225 m long (same as Bagger 287), weighs 14,200 tons, and requires five people to operate it". It shares the Guinness tallest-land-vehicle record with Bagger 288. **CONFIRMED.**
- The paper itself is an FEM study, per DIN 22261-2, of a generic eight-wheel bogie (two four-wheel plus four two-wheel bogies) for Serbian BWEs. It does **not** say Bagger 293 has 12 bogies.
- **de.wikipedia "Bagger 293"** (https://de.wikipedia.org/wiki/Bagger_293): height 96 m, length 226 m, weight 14,196 t, "Anzahl der Raupen" **12**, "Fahrspurbreite einer Raupe" 5.75 m, built by TAKRAF in 1995, operating at Hambach. No ground pressure is given.
- So "12 bogies" should read **"12 crawlers"**: PARTIALLY.
- **KuLaDig/LVR** (heritage database): Bagger 293 was ordered in 1991 and entered service on 7 Jul 1995 in Tagebau Hambach, mainly removing overburden (https://www.kuladig.de/Objektansicht/BKM-20103007). Bagger 288 entered service in Sep 1978; contemporary literature calls the 288/289 superstructures "13 000 t schwer" (https://www.kuladig.de/Objektansicht/BKM-20102006).
- **en.wikipedia "Bagger 288"** (https://en.wikipedia.org/wiki/Bagger_288): 96 m high, 220 m long, 13,500 t, "three rows of four caterpillar track assemblies, each 3.8 m wide", ground pressure **"1.71 bar (24.8 psi)"**, which is uncited. Your recollection of "1.71 kg/cm²" is close but the source unit is bar: 1.71 bar = 171 kPa, while 1.71 kg/cm² = 168 kPa.
- No source found for a Bagger 293 ground pressure, so that is **UNVERIFIABLE**. The 240,000 m³/day BWE class is about 170–175 kPa.
- **RICO Europe page [5]:** 403 to every fetch method, so **UNVERIFIABLE** directly. Its claims (96 m, 14,200 t) match the sources above.
- **Implication:** the heaviest land machines run on prepared mine benches at about 170 kPa nominal. That is above the doc's "normal soil" 144 kPa and the IBC sand value of 96 kPa, which shows those numbers are design allowables rather than physical limits.

## 5. Worldbuilding SE Q218215 (doc ref [4])

Retrieved via the Stack Exchange API; the site blocks WebFetch.

- **Question** (score 3, 1 answer, Nov 2021): mechs "of approx. the mass of The Iron Giant", **50 ft (≈15 m) tall**. It lists reference masses: Gundams 60–80 t, Macross about 15 t, MechWarrior 20–100 t. It asks which ground (granite, concrete, steel, dirt) can support them.
- **Only answer** (Shawn O'Neil, score 2, not accepted):
  - Gives the table: clay 95, sand or sand-gravel 144, gravel 239, sandstone 287, granite 574 kPa (= CABO 1995 values).
  - Assumes **70 t**, linear 10× human scale, foot area about 3.8 m² (two feet). Static pressure "about 170 kPa".
  - Walking: one foot carries the load, so about 340 kPa; "Nothing short of bedrock or thick reinforced concrete could withstand this load."
  - With 1.5 g peak, 510 kPa. Running at 2.2–2.7 g, 748–918 kPa: "It would leave footprints in solid bedrock".
  - To walk on clay, "feet about 90% longer and wider". To run on clay, "over 3 times as long and wide as proportional human feet".
- **No mention of football stadiums**, and no frigate. The doc extrapolates these and misattributes them to [4].
- The answer itself mixes up allowable presumptive values with failure strength ("footprints in solid bedrock" at 0.9 MPa is wrong for the reasons in section 2). The doc inherits that error.
- I found **no support anywhere** for "feet as big as football stadiums". My calculation (A = m·g·k/q):
  - 14,200 t, k = 2.5, q = 96 kPa → 3,635 m² per foot (60 m square, about 0.5 of a 105×68 m pitch).
  - Same mass, q = 144 → 2,425 m².
  - 5,000 t, k = 2.5, q = 144 → 854 m² (29 m square).
  - A stadium footprint including stands is about 3–5 ha (30,000–50,000 m²), so the claim overshoots by about 10× even at the most conservative allowable values. Using ultimate (≈3× allowable) or size-dependent sand capacity shrinks the feet further.

## 6. Naval frigate displacement

- FREMM (Italy/France): about **6,700 t full load** (Baird Maritime, The Defense Post 2025). The Italian Navy page reportedly says 6,900 t; it returned 502 when fetched.
- US Navy Constellation-class FFG-62: navy.mil fact file **7,291 t (long tons)**. https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2633250/
- **Typical modern frigate: about 4,000–7,500 t; recent large frigates 6,700–7,300 t.** A 5,000 t mech (the doc's "reduced" mass) is in frigate range. 14,200 t is about two frigates, or destroyer to cruiser class.
- Check of the doc's claim: 50 m humanoid with human-proportioned feet. Human sole ≈ 0.025 m² at 1.75 m, scaled ×(50/1.75)² gives ≈ 20 m². At 6,700–7,300 t that is 3.2–3.5 MPa static on one foot and 6.4–10.5 MPa at 2–3× GRF. It **does exceed 574 kPa (CONFIRMED)**.
  - It is comparable to code allowables on sound rock (NYC 5.7 MPa, Hong Kong 12.5 MPa) and 10–40× below intact granite UCS, so "perforating rock" is **CONTRADICTED**.
  - It exceeds the ultimate capacity of nearly all soils at that foot size, so sinking or bearing failure on soil is **CONFIRMED**.

## 7. Sauropod and dinosaur trackway anchors

- **Falkingham, Bates, Margetts & Manning 2011, J R Soc Interface 8:1142, "The 'Goldilocks' effect"** (PMC3119880), Table 1, static weight over area:

  | Trackmaker | Mass | Foot area | Pressure |
  |---|---|---|---|
  | *Brachiosaurus* manus | 25,922 kg | 0.144 m² | 662 kPa |
  | *Brachiosaurus* pes | 25,922 kg | 0.401 m² | 397 kPa |
  | *Brachiosaurus* combined | 25,922 kg | 0.545 m² | 467 kPa |
  | *Tyrannosaurus* (biped) | 7,654 kg | 0.234 m² | 320 kPa |
  | *Struthiomimus* | 423 kg | — | 161 kPa |

  A substrate with Cu = 100 kPa fails at 617 kPa under a circular indenter. A homogeneous cohesive substrate records tracks only in a narrow band: lighter animals leave no print, heavier ones sink. Track-bearing sediments were therefore soft.
- **Falkingham et al. 2010/2011, Biology Letters 7:142, "Simulating sauropod manus-only trackway formation using FEA"** (PMC3030862):
  - *Diplodocus* (11,449 kg): manus 82 kPa, pes 288 kPa.
  - *Brachiosaurus* (25,922 kg): manus 662 kPa, pes 397 kPa.
  - Manus-only trackways for *Brachiosaurus* are predicted where Cu = 65–110 kPa; *Diplodocus* pes-only prints where Cu = 13–45 kPa.
  - Simulated sinkage was capped at 5 cm (firmer layer below). A track deeper than about 1 cm requires substrate failure.
- **Plagne trackway (France), Mazin et al. 2017, Geobios; CNRS press release** (https://www.cnrs.fr/en/press/worlds-longest-sauropod-dinosaur-trackway-brought-light):
  - 155 m, 110 steps; pes prints 94–103 cm, "up to 3 meters when including the mud ring displaced by each step".
  - Trackmaker "at least 35 m long", "between 35 and 40 t", stride 2.80 m.
  - No depth reported, so **UNVERIFIABLE** here.
- **Takeaway for the simulation:** 25–40 t animals routinely walked on substrates at 400–660 kPa static per foot, about 1,000–2,000 kPa with dynamic factors. They left tracks on soft mud and none on firm ground. Biology tolerates foot pressures well above the code presumptive values. The real constraint is soil shear strength versus foot size, plus sinkage per step.

---

## Suggested ground limits for the scaled-humanoid simulation (my synthesis)

Use **ultimate** capacity, with sinkage as a soft constraint, for failure. Keep allowable (code) values as a "design comfort" line.

| Ground | Allowable (code) | Ultimate / failure scale | Notes |
|---|---|---|---|
| Very soft / soft clay, mud | <75 kPa (Tensar) | ≈ 6·cu; cu 10–40 kPa gives about 60–250 kPa | Size-independent (undrained) |
| Firm–stiff clay | 75–300 kPa (Tensar, NYC 192–287) | cu 40–150 kPa gives about 250–900 kPa | Falkingham: cu = 100 → 617 kPa |
| Loose sand | <100 kPa (HK 4(d)) | Grows with B; small feet low | Liquefaction risk if saturated |
| Medium dense to very dense sand/gravel | 100–500 kPa (HK); NYC dense gravel 958 | 0.5·γ·B·Nγ: about 0.3 MPa (B = 1 m) to 2.6 MPa (B = 10 m) at φ = 35° | Settlement governs for big B |
| Asphalt/concrete pavement | tyres 0.5–1.75 MPa (ICAO codes) | Slab flexure/punching; concrete 28–40 MPa crushing | Depends on slab and subgrade |
| Weathered / soft rock | 766 kPa (NYC 1d) – 3 MPa (HK 1(d)) | UCS 1–25 MPa | |
| Sound granite / gneiss | 574 kPa (IBC, no testing); 5.7 MPa (NYC); 10–12.5 MPa (HK) | Intact UCS 100–250+ MPa | Rock-mass strength lower (joints, RQD) |

Loading factor per step:
- Walking peak vertical GRF is about 1.2–1.5 BW; the SE answer uses 1.5 g. Running is 2–3 BW (SE: 2.2–2.7 g).
- Clay strength rate effect is about +10 % per decade of loading rate.
- IBC permits +1/3 on allowables for transient wind and seismic loads.

Unverifiable this pass:
- RICO page (403)
- BS 8004 table (paywalled)
- CFEM (no access)
- Bagger 293 ground pressure
- Leopard 2A6-specific pressure (forum only: 90 kPa)
- LR 13000 datasheet pressure
- Plagne track depth
