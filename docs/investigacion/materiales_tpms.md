# Fact-check: materials & TPMS cluster (sections 3–6)

Checked 2026-10-29. Where I could open primary full text (PMC/Europe PMC, open PDFs), quotes come from it. MDPI, ScienceDirect, Wiley, ASME and RSC pages returned 403 to the fetch tool. For a few constants I therefore used tables in open-access reviews, and each one is flagged where it appears.

## Verdict summary

| # | Claim in doc | Verdict |
|---|---|---|
| 1a | MIT 2017: "5% density of steel, 10× stronger" | **PARTIALLY.** The numbers match the paper and press release. But they come from an MD simulation (tensile) of a disordered 3D-graphene assembly. They do not come from a physical gyroid block. |
| 1b | The graphene was "fused with heat and pressure" and tested destructively | **CONTRADICTED.** The heat-and-pressure cycle was a simulated MD protocol. The physical tests were on 3D-printed **polymer** (VeroMagenta) gyroids about 10⁷× larger. |
| 1c | Buehler: geometry dominates | **CONFIRMED** (quote below) |
| 1d | So gyroid polymers/metals "will inexorably" gain dramatically in strength-to-weight "without significantly altering modulus" | **CONTRADICTED** by the paper itself: properties "decrease with density much faster than those of polymer foams". |
| 2 | Gibson–Ashby, m≈1.5. At ρ*/ρs=0.2, strength is "~X%" of solid | **Framework CONFIRMED.** Sourced gyroid constants give **≈1–9 %** yield strength and **≈1–7 %** modulus at ρ̄=0.2. **Specific strength is always below the solid's.** |
| 3 | Gyroid stiffness "markedly isotropic" | **PARTIALLY.** Sheet gyroids are near-isotropic. Skeletal/network gyroids are clearly anisotropic (cubic symmetry). |
| 4 | PLA vs PLA+CF TPMS numbers and conclusions | **Numbers CONFIRMED; interpretation PARTIALLY.** The ranges cover all specimens, not one topology. The "micro-void" mechanism is not in the paper. |
| 5 | Continuous carbon fiber (CCF) gyroids infeasible; weak in Z | **"Infeasible" CONTRADICTED** (CCF gyroids have been printed). **Z/interlayer weakness CONFIRMED.** |
| 6a | Ti-6Al-4V: ρ≈4.4, E≈110 GPa, UTS often >1000 MPa | **CONFIRMED / roughly right.** Annealed wrought UTS is ≈950 MPa typical. Above 1000 MPa applies to as-built LPBF or STA. |
| 6b | Gyroid Ti "exceeds all other cellular metals" | **CONTRADICTED / overstated.** Sheet TPMS beat strut lattices, but sheet-**Diamond** usually beats Gyroid. |
| 6c | "Plastic hinges… purely elastic and isotropic deformation" | **CONTRADICTED / misattributed.** The plastic-hinge description is from **CP-Ti** skeletal gyroids (Ataee 2018). Hinges are plastic, so the deformation is not elastic. |
| 6d | LPBF gives "almost 100% isotropic" properties | **CONTRADICTED** for as-built material. Only HIP'd solid material is reported isotropic. |
| 6e | Fatigue: gyroid eliminates stress concentrators | **PARTIALLY.** Sheet gyroids have the best normalized fatigue among lattices (≈45–50 % of yield in compression). Internal voids and roughness still start cracks. |
| 7 | Lattice/gyroid gives higher strength-to-weight than the solid | **No source supports it.** Theory bounds make it impossible: σ*/σs ≤ ρ̄ (Voigt bound). |
| 8 | Alan Schoen, NASA, 1970 | **CONFIRMED** |

---

## 1. MIT 2017 graphene gyroid (Qin, Jung, Kang, Buehler, *Sci. Adv.* 3:e1601536, DOI 10.1126/sciadv.1601536)

**Paper (open access):** https://pmc.ncbi.nlm.nih.gov/articles/PMC5218516

Abstract, verbatim:
> "Our study reveals that although the 3D graphene assembly has an exceptionally high strength at relatively high density (given the fact that it has a density of 4.6% that of mild steel and is 10 times as strong as mild steel), its mechanical properties decrease with density much faster than those of polymer foams. Our results provide critical densities below which the 3D graphene assembly starts to lose its mechanical advantage over most polymeric cellular materials."

**What was simulated:**
- Everything carbon was simulated: full-atom molecular dynamics with the AIREBO reactive potential.
- The heat-and-pressure step was simulated too: "We design a cyclic protocol to condense the material… we control both the temperature and pressure for each stage."
- The 4.6%/10× structure is the disordered **3D-graphene assembly**, not the ideal gyroid: "It has a density of 366.2 mg/cm³, which is 4.6% that of mild steel."
- Its simulated properties: "Young's modulus of 2.8 GPa… and a tensile strength of 2.7 GPa… an order of magnitude higher than that of mild steel."
  - So the comparison is **absolute tensile strength**, not strength per weight.
- Simulated compressive strength: "0.6 GPa".
- Note: E = 2.8 GPa is about 1.4 % of steel's ~200 GPa (the steel figure is general knowledge, not from the paper). A gyroid-graphene block would therefore be far *less stiff* than steel.

**What was measured physically:**
- Only 3D-printed **polymer** gyroids were tested: "The material we used for printing is called VeroMagenta", printed on a Stratasys Objet500 at 20 µm resolution.
- The prints were "10⁷ times longer than the full atomic models".
- Printed-sample densities were 92.2–401.6 mg/cm³ (≈8–34 % of VeroMagenta). Measured E was 3.0–184.9 MPa.
- Results were normalized by the bulk polymer and fall on the same scaling laws.

**Scaling exponents (graphene assembly and printed gyroids):**
- E ∝ ρ^2.73±0.09
- σ_tension ∝ ρ^2.01±0.05
- σ_compression ∝ ρ^3.01±0.01
- The paper says these are "overall larger than those of conventional polymeric open-cell foams" (foam values: 2 and 1.5). It calls the behaviour bending-dominated.
- Lighter-than-air/helium idea: "these two conditions cannot be satisfied simultaneously."

**Geometry dominates (confirmed):**
- Paper: "the mechanics of the 3D graphene assembly are mainly governed by its geometry."
- MIT News: Buehler: "The geometry is the dominant factor." "You could either use the real graphene material or use the geometry we discovered with other materials, like polymers or metals."

**MIT News press release:** https://news.mit.edu/2017/3-d-graphene-strongest-lightest-materials-0106
- "with a density of just 5 percent, can have a strength 10 times that of steel"
- Qin: "one of our samples has 5 percent the density of steel, but 10 times the strength"
- "The team was able to compress small flakes of graphene using a combination of heat and pressure." This is ambiguous; in the paper it is the MD simulation.
- "The team used 3-D-printed models of the structure, enlarged to thousands of times their natural size, for testing purposes."

**Corrections or criticism:** No erratum on the paper or editor's note on the release was found. The strongest "correction" is the paper's own conclusion (properties fall faster than polymer foams), which the press framing and the doc leave out.

**For the doc:**
- It wrongly says physical destructive tests showed the 10× figure on a gyroid graphene block.
- Its inference that gyroid geometry preserves modulus while cutting mass is the opposite of what the exponents (2.7–3.0) show.

---

## 2. Gibson–Ashby constants for gyroids: E*/Es = C1(ρ̄)^n, σ*/σs = C2(ρ̄)^m

Classical open-cell foam values (Gibson & Ashby): C1≈1, n=2; C2≈0.3, m=1.5. Li et al. 2019 confirm the ranges C1 "0.1 to 4.0" and C2 "0.25 to 0.35" (https://pmc.ncbi.nlm.nih.gov/articles/PMC6650998).

| Source | Material / type | C1 | n | C2 | m | E*/Es @0.2 | σ*/σs @0.2 | specific σ vs solid |
|---|---|---|---|---|---|---|---|---|
| Classical foam (G&A) | – | 1 | 2 | 0.3 | 1.5 | 4.0 % | 2.7 % | 13 % |
| If C2 = 1, m = 1.5 (likely the doc's ~8.9 %) | – | 1 | 2 | 1 | 1.5 | 4.0 % | **8.9 %** | 45 % |
| Naghavi 2022, *Bioengineering* 9:504 (DOI 10.3390/bioengineering9100504) [1] | Ti6Al4V LPBF, **sheet** gyroid | 0.9 | 1.58 | 0.536 | 1.45 | 7.1 % | 5.2 % | 26 % |
| Al-Ketan, Rowshan & Abu Al-Rub 2018, *Addit. Manuf.* 19:167 (DOI 10.1016/j.addma.2017.12.006) [2] | Maraging steel LPBF, **sheet** gyroid | 0.10 | 1.23 | 0.885 | 1.43 | 1.4 % | 8.9 % | 44 % |
| same [2] | Maraging steel LPBF, **skeletal** gyroid | 0.14 | 1.68 | 1.189 | 1.86 | 0.9 % | 6.0 % | 30 % |
| Yan 2015, *JMBBM* 51:61 [3] | Ti6Al4V SLM, skeletal gyroid | 0.19 | 1.71 | 1.31 | 1.83 | 1.2 % | 6.9 % | 34 % |
| Ataee 2018, *Acta Mater* 158:354 [3] | **CP-Ti** SLM, skeletal gyroid | 0.29 | 2 | 0.46 | 1.5 | 1.2 % | 4.1 % | 21 % |
| Polley 2022, *JMBBM* 125:104882 [3] | Ti6Al4V EBM, sheet gyroid | 0.20 | 1.2 | 0.67 | 1.3 | 2.9 % | 8.3 % | 41 % |
| Sun 2022, *Mech. Mater.* 166:104241 [3] | Ti6Al4V SLM, sheet gyroid | 0.12 | 1.1 | 2.07 | 2.03 | 2.0 % | 7.9 % | 39 % |
| Li 2019, *Materials* 12:2183 [4] (n=2, m=1.5 fixed) | SLA resin, sheet / strut gyroid | 0.817 / 0.512 | 2 | 0.179 / 0.135 | 1.5 | 3.3 / 2.0 % | 1.6 / 1.2 % | 8 / 6 % |
| Abou-Ali, Lee & Abu Al-Rub 2022, *Polymers* 14:4583 [5] | PA11 SLS, sheet / ligament gyroid | (in MPa, not normalized) | 1.08 / 2.40 | – | 1.01 / 2.05 (yield) | – | – | – |

Notes on the sources:
- [1] https://pmc.ncbi.nlm.nih.gov/articles/PMC9598079/ (Table 7). Bulk values used: Es = 35.77 GPa, σs = 1012 MPa, both from "fully dense, additively manufactured" material. The low Es means it was measured with crosshead compliance.
  - Measured sheet gyroids at ρ̄≈0.33–0.46: E 5.7–8.5 GPa, yield 94–181 MPa.
- [2] Values taken from Table 1 of Kladovasilakis et al. 2022 (https://pmc.ncbi.nlm.nih.gov/articles/PMC9456607/). Cross-checked against Abou-Ali 2022, which cites Al-Ketan's sheet-Diamond n = 0.5.
- [3] Values taken from Table 4 of Distefano, Pasta & Epasto 2023, *J Funct Biomater* 14:125 (https://pmc.ncbi.nlm.nih.gov/articles/PMC10059040/).
- [4] https://pmc.ncbi.nlm.nih.gov/articles/PMC6650998 (Table 2).
- [5] https://pmc.ncbi.nlm.nih.gov/articles/PMC9658147/ (Table 5). Its prefactors are absolute (MPa), so only the exponents compare.

Takeaways:
- **m ≈ 1.5 is defensible:** reported gyroid m runs about 1.3–2.0.
- **n splits by type:** sheet gyroids give n ≈ 1.1–1.6 (stretching or mixed); skeletal gyroids give n ≈ 1.7–2.4 (bending).
- **If the doc used C2 = 1 (≈8.9 %), that is the optimistic upper end.** With m = 1.5 fixed, fits give C2 = 0.13–0.46, i.e. **1.2–4.1 %**. Free fits on metal LPBF gyroids give 4–9 %.
- Low C1 values (0.1–0.3) in metal studies mostly reflect crosshead strain measurement, so absolute stiffness is uncertain. The E*/Es column is only indicative.
- **In every row, specific strength (σ*/ρ*) is 6–45 % of the solid's**, never above 100 %.

---

## 3. Is gyroid stiffness isotropic?

- **Li, Liao, Dai & Xie 2019** (*Materials* 12:2183), numerical homogenization with the Zener ratio A = 2C44/(C11−C12):
  > "the sheet-based gyroid cellular structure is similar to isotropic at both low-density and high-density, while the strut-based gyroid structure has obvious anisotropy."
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6650998
- **Lu et al. 2019** (*JMBBM* 99:56, DOI 10.1016/j.jmbbm.2019.07.012), on solid/scaffold TPMS:
  - Gyroid has cubic symmetry.
  - "The absolute difference between the Zener anisotropic factor and one increased the most for the Gyroid based scaffold" as porosity rises.
  - Abstract via Europe PMC: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.jmbbm.2019.07.012%22&resultType=core
- **El-Asfoury et al. 2026** (*Sci Rep* 16:4373, sheet gyroid, PLA):
  - E_max/E_min = **1.12** in the best orientation and up to **1.37** in others.
  - "most gyroid-based TPMS structures approximate cubic symmetry, although the anisotropic modulus surfaces reveal subtle variations."
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC12864783
- **Verdict: PARTIALLY.** The doc's "markedly isotropic" holds for **sheet** gyroids (roughly 10–40 % directional spread). It does not hold for network/skeletal gyroids. Process anisotropy is a separate issue (§6).

---

## 4. PLA vs PLA+CF TPMS (FDM)

**Paper:** Saleh, Anwar, Al-Ahmari & Alfaify, "Compression Performance and Failure Analysis of 3D-Printed Carbon Fiber/PLA Composite TPMS Lattice Structures", *Polymers* 2022, 14:4595, DOI 10.3390/polym14214595. https://pmc.ncbi.nlm.nih.gov/articles/PMC9654767/

**Confirmed:**
- Abstract: "compressive modulus (0.09 to 0.47 GPa), compressive strength (2.98 to 13.89 MPa), and specific energy absorption (SEA) (0.14 MJ/m³/g to 0.58 MJ/m³/g) due to the influence of CF incorporation, cell type and size, and RD."
- "All the CF-based TPMS structures showed a higher compressive modulus."
- "the peak strength of Gyroid and Primitive designs for PLA + CF lattice structures was lower compared to that of PLA, and this effect became more pronounced at higher RDs."
- Diamond: "Compressive strength and energy absorption capacity were both slightly enhanced in most PLA + CF-based Diamond structures."

**Where the doc misreads it:**
- **The ranges are global**, across both materials, all three topologies, cell sizes of 6/8/12 mm and RDs of 23–44 %. Doc Table 2 gives "2.98–13.89" to *each* topology. Doc text implies CF alone took modulus "from 0.09 to 0.47 GPa". Neither is what the paper reports.
- **SEA for gyroid** fell only in some cases: "the addition of CF to PLA reduces the SEA at a high RD (44%) and larger unit cell size (12 mm)."
- **Mechanism:** the paper does **not** invoke micro-voids at the fiber/matrix interface. Its explanation is: "P and G structures' walls get thicker as RDs increase, resulting in more CF deposition, which leads to a reduction in their strength." It adds that "thicker walls imply more CF extrusion, resulting in stiffer structures that can absorb less energy", and that "cracks always start between layers".
- **Filament data** (paper Table 2; 3DXTech CarbonX, 15 % CF in a 4043D matrix): PLA+CF tensile strength is 48 MPa vs 56 MPa for PLA, elongation 2 % vs 8 %, modulus 4950 vs 2865 MPa. So the filament itself is weaker and more brittle, only stiffer.

---

## 5. Continuous carbon fiber (CCF) printed TPMS/gyroids

**Szederkényi, Kovács & Czigány, ECCM21 (Nantes, 2024)**
- Paper: https://real.mtak.hu/206352/1/1843_open_ECCM21_Proceeding_CFRP_TPMS_crush.pdf
- **They printed CCF gyroid and diamond lattices** on a Markforged Mark Two (PA6/Onyx matrix):
  - 45 mm cubes with 15 mm cells, ρ̄ ≈ 37 %, fiber content 8.5–16.5 vol%.
  - Minimum fiber-reinforced cross-section was 2.8 mm.
  - "Fiber placement was restricted to printed layers."
- Specific modulus rose **+81 %** with 0° fibers vs PA6 (**+126 %** for the straight-column "masked" version).
- But SEA averaged only **47 % of PA6**. The fiber specimens "delaminated and separated due to weak interlayer adhesion."
- Short-fiber Onyx underperformed pure PA6 on all metrics (gyroid specific modulus −32 %).

**ASME IMECE2024 paper** "Additive Manufacturing With Continuous Carbon Fiber Composite Reinforcement for Gyroid TPMS: Compression Mechanical Properties"
- https://asmedigitalcollection.asme.org/IMECE/proceedings-abstract/IMECE2024/88605/V002T03A003/1211581 (403 to the fetch tool)
- Abstract as quoted second-hand: "up to 343% increase in compression modulus and 250% in yield strength". Layer delamination is critical under in-plane loading.
- **Not verified first-hand.**

**Polte et al. 2024**, *Prog. Addit. Manuf.*, DOI 10.1007/s40964-024-00877-6, with **continuous glass fiber** in Primitive TPMS:
- "increase in maximum strength of Δσmax = 185%", plus ΔE = 95 % and ΔW = 123 %.
- https://depositonce.tu-berlin.de/items/408aa889-24d0-4ea6-ada6-81ad326cc9d1/full

**Verdict:** "Impossible" is **wrong**. CCF TPMS/gyroids have been printed and show large stiffness gains. The real constraints are:
- fibers can only follow in-plane paths;
- cells must be large (multi-mm walls);
- interlayer (Z) delamination dominates failure. This part supports the doc's Z-weakness point.

---

## 6. Ti-6Al-4V and LPBF Ti gyroid lattices

**Wrought/annealed Grade 5, typical values (Ulbrich):**
- ρ = 4.43 g/cm³, E = 113.8 GPa, YS 880 MPa, UTS 950 MPa, elongation 15 %.
- https://www.ulbrich.com/alloys/ti-6-al-4-v-uns-r56400/
- AMS 4928 minimums: YS 862 MPa, UTS 931 MPa (Bibus datasheet): https://www.bibusmetals.cz/fileadmin/materials/PDF/BM_Datasheets/BM_datasheet_Ti_Grade_5_Ti6-4.pdf
- The doc's "~110 GPa, UTS often >1000 MPa" is OK. For annealed wrought, 950 is typical; >1000 MPa applies to STA or as-built AM.

**LPBF solid material:**
- As-built (α′ martensite): "high tensile strength (>1000 MPa), high yield strength (>900 MPa) and a low ductility (total elongation <8%)". The same review notes anisotropic microstructure (columnar prior-β grains) and anisotropic fatigue.
  - Gorsse et al. 2017, *STAM*: https://pmc.ncbi.nlm.nih.gov/articles/PMC5613834
- Stress-relieved vs HIP (Mahmud et al. 2021, *Metals* 11:1671, INL; https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_63131.pdf):
  - Stress-relieved: YS **1141**, UTS **1190 MPa**, elongation **6.9 %**, "along with mechanical anisotropy".
  - After HIP: "consistent and isotropic", YS **928**, UTS **1003 MPa**, elongation **16.1 %**, E ≈ 115–121 GPa.
- Build-orientation anisotropy (Jamshidi et al. 2020, *Materials* 13:2813; https://pmc.ncbi.nlm.nih.gov/articles/PMC7345457):
  - Horizontal builds: YS 760.9 / UTS 961.3 MPa. Vertical builds: YS 820.1 / UTS 1006.7 MPa.
  - Attributed to "the anisotropic microstructure, crystallographic orientation, and spatial distribution of defects".
- ASTM F2924 (PBF Ti-6Al-4V) minimums: UTS 895, YS 825 MPa, elongation 10 %. This is a secondary listing: https://www.totalmateria.com/en-us/material/3300110
- **"Almost 100 % isotropic"** is CONTRADICTED for as-built material. It is approximately true only after HIP, and only for the solid metal. The lattice geometry adds its own anisotropy (§3).

**Gyroid lattice strengths:**
- Sheet gyroid Ti6Al4V LPBF at ρ̄ ≈ 0.33–0.46: yield 94–181 MPa, E 5.7–8.5 GPa (Naghavi 2022, above).
- Yan et al. 2015, skeletal gyroid/diamond Ti6Al4V SLM at 80–95 % porosity: "modulus is in the range of 0.12–1.25 GPa".
- **Ataee et al. 2018, *Acta Mater* 158:354: this is CP-Ti, not Ti-6Al-4V.**
  - 68–73 % porosity; "elastic modulus and yield strength… from 1465 to 2676 MPa and from 44.9 to 56.5 MPa".
  - Mechanism: "formation of a plastic hinge which led to rotation of the struts about the plastic hinges followed by development of local shear bands in struts in the long plateau region."
  - **This is clearly the source of the doc's "bisagras plásticas" passage.** It describes plastic, localized deformation in a different alloy, not a "purely elastic and isotropic" response.
  - Abstract via Semantic Scholar API: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.actamat.2018.08.005?fields=abstract

**Deformation mode depends on lattice type:**
- Al-Ketan 2018 (maraging steel): sheet TPMS "near stretching-dominated"; skeletal TPMS "bending-dominated". https://khazna.ku.ac.ae/en/publications/topology-mechanical-property-relationship-of-3d-printed-strut-ske/
- Kelly 2019 (Ti6Al4V ELI sheet gyroid): "stretching-dominated deformation behavior"; "Internal void defects were observed within the walls… serving as sites for crack initiation leading to failure".
- Zhang 2018 (316L SLM): Diamond and Gyroid sheets give "stable collapse mechanisms", while Primitive shows "rapid diagonal shear band development".

**"Best of all cellular metals": CONTRADICTED.**
- Al-Ketan 2018: "sheet-TPMS based cellular structures showed superior mechanical properties among all the tested structures", but "sheet-based Diamond TPMS structure showed the best mechanical performance".
- Zhang 2018: "Diamond-type sheet structures performing best".
- Kelly 2021 supports the class-level claim: sheet TPMS have "superior strength, energy absorption, and fatigue resistance relative to strut-based architectures of the same volume fraction".
- The comparison with "massive magnesium superalloys" has no source: **UNVERIFIABLE**.

**Fatigue (ratio to yield/offset stress):**
- **Sheet gyroid Ti6Al4V L-PBF, as-built surfaces:** "Normalized compressive fatigue strength… >50%", and this is higher than in tension (Kelly et al. 2021, *Addit. Manuf.* 41:101916).
  - https://www.restor3d.com/wp-content/uploads/2024/07/Processing-structure-and-properties-of-additively-manufactured-titanium-scaffolds-with-gyroid-sheet-architecture.pdf
  - Kelly 2019 (*Acta Biomater* 94:610), fatigue of as-built sheet gyroids: https://www.restor3d.com/wp-content/uploads/2024/07/Fatigue-behavior-of-As-built-selective-laser-melted-titanium-scaffolds-with-sheet-based-gyroid-microarchitecture-for-bone-tissue-engineering.pdf
- **EBM Ti6Al4V gyroid:** "fatigue strength at 10⁶ cycles at 45% of their compressive offset stress" (Polley 2022, abstract via Europe PMC).
- **Strut lattices (SLM Ti6Al4V ELI, 68–84 % porosity):** "normalized endurance limit of all tested porous structures (<0.2) is lower than that of corresponding solid material (c.a. 0.4)" (Yavari et al. 2013, *MSE C*, DOI 10.1016/j.msec.2013.08.006).
- **Solid as-built AM Ti64:** "fatigue strength… only 300 MPa (at 30 million cycles) because of the poor surface finish"; milling to Ra 0.3 µm raised it to 750 MPa (Ye et al. 2021 review: https://pmc.ncbi.nlm.nih.gov/articles/PMC8312382).
- So sheet gyroids are the best lattices for fatigue, but a fatigue ratio of ≈0.45–0.5 in compression (and lower in tension) is still a large derating. Rough as-built surfaces and internal voids also stay.

---

## 7. Can a lattice beat the solid in strength-to-weight?

**No source found that shows it. Theory rules it out for a porous version of the same material.**

- **Upper bounds** (Wang et al. 2022, *PNAS* 119:e2119536119; https://pmc.ncbi.nlm.nih.gov/articles/PMC9407660):
  - Rule-of-mixtures (Voigt) limit: σ_y ≤ σ_ys·ρ̄ and E ≤ Es·ρ̄, described as "the theoretical limits… of an anisotropic porous material". This means **specific strength ≤ the solid's**, with equality only for ideally aligned material.
  - Isotropic Suquet bound: σ_y ≤ 6σ_ys·ρ̄/√(69−33ρ̄), which is **15.2 %** at ρ̄ = 0.2. The Hashin–Shtrikman bound for E is **≈11 %** at ρ̄ = 0.2 (ν = 0.3). Both are my calculations from the paper's equations.
  - Truss lattices reach only "∼25 and 20% of the HS and Suquet upper bounds".
  - The record specific strengths of nanolattices come from nanoscale size effects in the material, not from geometry.
- **Ashby 2006**, "The properties of foams and lattices", *Phil. Trans. R. Soc. A* 364:15 (DOI 10.1098/rsta.2005.1678):
  - Stretch-dominated structures are "exceptionally stiff and strong for a given mass". This is relative to other cellular solids, not the parent solid.
  - Bending-dominated ones are "compliant and, although not strong, it absorbs energy well when compressed."
- **Evans, Hutchinson & Ashby 1998**, "Cellular metals", *Curr. Opin. Solid State Mater. Sci.* 3:288 (https://groups.seas.harvard.edu/hutchinson/papers/473.pdf):
  - Sandwich weight "advantages are found in structures controlled by bending or compression [buckling], but not in those dominated by tension."
  - "There are no benefits for designs based on limit loads, wherein the system squashes plastically."
- **What lattices are good for:**
  - cores of bending- or buckling-limited sandwich panels and shells (they raise the second moment of area per unit mass);
  - energy absorption over a long plateau;
  - stiffness tailoring (e.g. bone implants);
  - surface area, heat exchange and permeability.
- **For the doc:** the claim that an 80 % mass cut "nullifies" square-cube problems ignores that load capacity falls faster than mass (σ ∝ ρ̄^1.5 or steeper). It is specific strength that matters for self-weight-limited members, and it goes down.

---

## 8. Alan Schoen, NASA, 1970: CONFIRMED

- A. H. Schoen, "Infinite periodic minimal surfaces without self-intersections", **NASA TN D-5541, 1 May 1970**, NASA Electronics Research Center, Cambridge MA. https://ntrs.nasa.gov/citations/19700020472
- Wikipedia calls him "an American physicist and computer scientist… best known for discovering (while working at NASA) a minimal surface that he named the gyroid." https://en.wikipedia.org/wiki/Alan_Schoen
- Zero mean curvature and two interpenetrating labyrinths: correct. The NTRS subtitle reads "Three dimensional Euclidean space partitioned into interpenetrating labyrinths".
  - Caveat: printed gyroids are thickened sheets or solid networks built from the trigonometric level-set *approximation*, so the printed walls do not have zero mean curvature.
