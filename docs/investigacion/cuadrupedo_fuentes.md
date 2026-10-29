# Cuadrúpedo vs bípedo: fuentes para parametrizar el modelo

Revisado el 2026-10-29. Cada número lleva su cita. Marco **[derivado]** lo que calculé yo a partir de datos publicados y **[secundario]** / **[no verificado]** lo que no pude leer en la fuente primaria.

**Acceso.** pmc.ncbi.nlm.nih.gov respondió a WebFetch pero bloquea curl (reCAPTCHA). cob.silverchair.com, rvc-repository.worktribe.com, digitalcommons.butler.edu y web.archive.org devolvieron 403 o un desafío de Cloudflare. journals.biologists.com (JEB) sí respondió en algunos artículos. Usé Europe PMC REST, Crossref, PMC vía WebFetch y PDFs de repositorios abiertos. No esquivé ningún bloqueo.

---

## 0. Números clave para el modelo (resumen)

| Parámetro | Valor | Fuente |
|---|---|---|
| GRF vertical pico por pierna, **bípedo** caminando (humano) | 1.05 / **1.13** / 1.23 BW (lento / cómodo / rápido) | [derivado] de Fukuchi et al. 2018; coincide con Nilsson & Thorstensson 1989 (1.0–1.5 BW) |
| GRF pico, **perro** al paso, anterior / posterior | **0.74 / 0.51 BW** | Kano et al. 2016 |
| GRF pico, perro al trote | 1.09 / 0.75 BW | Kano et al. 2016 |
| GRF pico, **caballo** al paso | ~0.66 / ~0.51 BW | Weishaupt 2005 [secundario] |
| GRF pico, caballo al trote | 1.18 / 1.04 BW (11.59 / 10.21 N/kg) | Merkens et al. 1993 |
| GRF pico, **elefante** (0.6–4.8 m/s) | **< 1 BW** anterior, **< 0.7 BW** posterior; ~60 % del peso delante | Ren et al. 2010 |
| Regla para la GRF pico por pata | F_pico/BW ≈ (π/2)·s/DF | [derivado]; se ajusta a los datos de perro con ±5 % |
| Momentos articulares humanos (marcha cómoda, 1.24 m/s) | cadera ext. 0.61, rodilla ext. 0.45, tobillo PF **1.46 N·m/kg**; M/(m·g·L) = 0.07 / 0.05 / 0.17 | [derivado] de Fukuchi et al. 2018 |
| Momentos del caballo al trote (2.5–5 m/s), pata anterior | hombro 1.5, codo 1.1, carpo −1.3, nudo −1.3 N·m/kg | Ferris et al., resumen SICB |
| EMA frente a masa | ∝ M^0.26 (Biewener 1989), ≈ M^0.25 (Biewener 2005) | Bullimore & Burn 2005; Biewener 2005 |
| EMA medida | elefante caminando **0.68**; humano caminando 0.71; caballo al trote ~1.0; la ley de escala predice 1.75 a 3 t | Ren et al. 2010 |
| Bípedos obligados más grandes | **~7–9.5 t** (T. rex, Spinosaurus, Giganotosaurus) | Benson 2014; Hutchinson 2011; Persons 2020; Sereno 2022 |
| Cuadrúpedos más grandes | **~50–90 t** (titanosaurios); mamíferos ~17–22 t | Benson 2014; Carballido 2017; Larramendi 2016 |
| Cociente de masa máxima cuadrúpedo/bípedo | ~5–13× en masa, **~1.7–2.3× en longitud** (isométrico) | [derivado] |
| Mayor máquina que camina de verdad | Tradinno, cuadrúpedo de **11 t** | Guinness (ya en `locomocion_actuadores.md`) |
| Factor de servicio dinámico del tronco | trote/galope ~**2 g**; paso, cargas menores | Kienapfel et al. 2018 (cita a Preuschoft 1985 y Witte 1995) |
| Factor de servicio (DF) del elefante | mediana 0.73–0.74 en marcha; rango 0.37–0.85 | Usherwood & Self Davies 2017; Hutchinson et al. 2006 |
| Umbral de estabilidad estática | DF ≥ 0.75 | McGhee & Frank 1968 [secundario, vía eLife 2017] |

---

## 1. Fuerza vertical de reacción del suelo (GRF) por pata

### 1a. Datos medidos

| Especie (masa) | Marcha, velocidad | Pico ant. (BW) | Pico post. (BW) | DF ant. / post. | Fuente |
|---|---|---|---|---|---|
| Humano, bípedo (68 kg, n = 24 jóvenes) | marcha lenta 0.88 m/s (Fr 0.09) | 1.05 (10.26 N/kg) | — | — | [derivado] de Fukuchi et al. 2018 (abajo) |
| Humano | marcha cómoda 1.24 m/s (Fr 0.18) | **1.13** (11.07 N/kg) | — | — | ídem |
| Humano | marcha rápida 1.58 m/s (Fr 0.30) | 1.23 (12.07 N/kg) | — | — | ídem |
| Humano | marcha 1.0–3.0 m/s | 1.0 → 1.5 | — | — | Nilsson & Thorstensson 1989 (ya citado en `locomocion_actuadores.md`) |
| Perro (≈22 kg, n = 15) | paso, 0.9–1.1 m/s | **0.74 ± 0.21** | **0.51 ± 0.17** | 0.625 / 0.601 | Kano et al. 2016, Tablas 1–2 |
| Perro (≈6.5 kg, n = 14) | trote, 0.9–1.1 m/s | 1.09 ± 0.36 | 0.75 ± 0.26 | 0.469 / 0.405 | ídem |
| Caballo (Warmblood, n = 20) | trote | **1.18** (11.59 N/kg) | **1.04** (10.21 N/kg) | — | Merkens et al. 1993 |
| Caballo | paso (pico bifásico) | ~0.66 (2.º pico) | ~0.51 (1.er pico) | — | Weishaupt 2005, AAEP [secundario] |
| Elefante asiático juvenil (2291 ± 669 kg, n = 6) | 0.64–4.83 m/s; paso a ~1.2 m/s (û 0.30–0.35) | **< 1** | **< 0.7** | — | Ren et al. 2010 |
| Elefante, extrapolado a ~7 m/s | — | ~1.1 | ~0.98 | — | ídem |

- **Perro.** La distribución del peso es ≈ 60 % delante y 40 % detrás, igual al paso que al trote: *"approximately 60% for the forelimbs and 40% for the hind limbs"*. Ojo: lo midieron con pasarela de presión, no con plataforma de fuerzas. **Kano WT, Rahal SC, et al. (2016)**, *BMC Vet Res* 12:2, DOI [10.1186/s12917-015-0631-2](https://doi.org/10.1186/s12917-015-0631-2), acceso abierto PMC5015230. El estudio clásico con plataforma de fuerzas es **Budsberg, Verstraete & Soutas-Little (1987)**, *Am J Vet Res* 48:915–918, DOI [10.2460/ajvr.1987.48.06.915](https://doi.org/10.2460/ajvr.1987.48.06.915): *"larger dogs had a lower peak force on each limb"* y *"As stance phase time increased, peak vertical forces decreased."* Solo leí el resumen, sin números.
- **Caballo al trote.** *"only one vertical force peak in forelimbs and hindlimbs (11.59 N/kg and 10.21 N/kg, respectively)"*. **Merkens HW, Schamhardt HC, van Osch GJ, van den Bogert AJ (1993)**, *Equine Vet J* 25:134–137, DOI [10.1111/j.2042-3306.1993.tb02923.x](https://doi.org/10.1111/j.2042-3306.1993.tb02923.x).
- **Caballo al paso [secundario].** El texto de Weishaupt, tal como lo devolvió la búsqueda: *"Fzpeak reaches an average of 66% (second peak) of bwt in the forelimbs and 51% (first peak) in the hindlimbs"*. **Weishaupt MA (2005)**, "Compensatory load redistribution in forelimb and hindlimb lameness", *Proc. 51st AAEP Annual Convention*, Seattle (IVIS), https://www.ivis.org/library/aaep/aaep-annual-convention-seattle-2005/compensatory-load-redistribution-forelimb-and-hindlimb-lameness. La página devolvió 403 y no pude leerla. El dato primario de paso es **Merkens et al. (1986)**, *Equine Vet J* 18:207–214, DOI [10.1111/j.2042-3306.1986.tb03600.x](https://doi.org/10.1111/j.2042-3306.1986.tb03600.x), pero su resumen no trae números.
  - Comprobación cruzada [derivado]: **Witte, Knill & Wilson (2004)**, *J Exp Biol* 207:3639–3648, DOI [10.1242/jeb.01182](https://doi.org/10.1242/jeb.01182), predicen la GRF pico a partir del DF. Al paso sobreestiman en *"0.8 ± 0.04 N kg⁻¹ (13%)"* y al trote infraestiman en *"−0.3 ± 0.06 N kg⁻¹ (3%)"*. Si 0.8 N/kg es el 13 %, el pico medio al paso es ≈ 6.2 N/kg ≈ 0.63 BW, coherente con Weishaupt.
- **Elefante.** Citas literales: *"peak vertical GRFs were ~50% higher for the forelimbs than for the hindlimbs (corresponding to a weight distribution of ~60% on the forelimbs)"*; *"Maximal vertical GRFs were <1 body weight (BW) for each forelimb and <0.7 BW for each hindlimb."*; a ~7 m/s *"should reach about 1.1 BW and 0.98 BW, respectively"*. Las componentes horizontal y mediolateral quedan por debajo de 0.1 BW. **Ren L, Miller CE, Lair R, Hutchinson JR (2010)**, *PNAS* 107(15):7078–7082, DOI [10.1073/pnas.0911396107](https://doi.org/10.1073/pnas.0911396107), acceso abierto PMC2872429.
- **Vaca.** No encontré la GRF pico por pata en BW con acceso. Sí hay presiones en la pezuña al caminar: *"average pressures determined were 50 to 80 N/cm2. Maximum pressures increased from 90 to 110 N/cm2 at heel strike to 180 to 200 N/cm2 at push off"*, es decir 0.5–0.8 MPa de media y 1.8–2.0 MPa de pico. **van der Tol PP et al. (2003)**, *J Dairy Sci* 86:2875–2883, DOI [10.3168/jds.S0022-0302(03)73884-3](https://doi.org/10.3168/jds.S0022-0302(03)73884-3). **[no verificado]**: la GRF por pata en vacas.
- **Humano [derivado].** Lo calculé del conjunto público **Fukuchi CA, Fukuchi RK, Duarte M (2018)**, "A public dataset of overground and treadmill walking kinematics and kinetics in healthy individuals", *PeerJ* 6:e4640, DOI [10.7717/peerj.4640](https://doi.org/10.7717/peerj.4640), datos en Figshare [10.6084/m9.figshare.5722711](https://doi.org/10.6084/m9.figshare.5722711).
  - Usé los ficheros `WBDSascii.zip` → `*walkO{S,C,F}knt.txt`, que son medias por sujeto en suelo, normalizadas a 101 puntos del ciclo. Tomé el grupo «Young»: 24 sujetos y 45–48 piernas válidas.
  - El pico vertical (`GRFY`) sale en unidades de ~11 al paso cómodo, lo que corresponde a N/kg (1.13 BW).

### 1b. Regla de escala por pata [derivado, física de impulsos]

En un ciclo de duración T, una pata que soporta en promedio una fracción s del peso debe aportar el impulso s·m·g·T durante el apoyo, DF·T. Si la curva de fuerza es una semisinusoide, la media vale (2/π)·F_pico, de modo que:

**F_pico / (m·g) ≈ (π/2) · s / DF**

| Caso | s | DF | Predicción | Medido |
|---|---|---|---|---|
| Perro al paso, pata anterior | 0.30 | 0.625 | 0.75 BW | 0.74 |
| Perro al paso, pata posterior | 0.20 | 0.601 | 0.52 BW | 0.51 |
| Perro al trote, pata anterior | 0.30 | 0.469 | 1.00 BW | 1.09 |
| Perro al trote, pata posterior | 0.20 | 0.405 | 0.79 BW | 0.75 |
| Humano, marcha cómoda (DF ≈ 0.62) | 0.50 | 0.62 | 1.27 BW | 1.13 (la curva en «M» aplana el pico, ~+12 %; Witte da +13 % al paso en caballos) |
| Elefante caminando (DF ≈ 0.70, 60 % delante) | 0.30 | 0.70 | 0.67 BW | < 1 BW (máximo en todo el rango de velocidad) |
| **Mecha cuadrúpedo, crawl estático** (50/50, DF 0.75–0.80) | 0.25 | 0.75–0.80 | **0.49–0.52 BW** | — |
| Mecha cuadrúpedo, 60/40 delante, DF 0.75 | 0.30 | 0.75 | 0.63 BW | — |
| Mecha bípedo caminando | 0.50 | 0.60–0.65 | 1.2–1.3 BW (medido en humanos: 1.05–1.23) | — |

**Conclusión para el modelo:** al paso lento, el pico por pata de un cuadrúpedo es ≈ 0.4–0.55 veces el de un bípedo. Pero un cuadrúpedo tiene el doble de patas, así que la masa total de actuadores no baja en la misma proporción (véase §2).

---

## 2. Momentos articulares, trabajo y potencia; EMA

### 2a. Humano caminando: datos de referencia del bípedo [derivado de Fukuchi et al. 2018]

Valores pico sagitales: media ± DE sobre piernas del grupo joven. La componente sagital es la Z de los ficheros `knt`; la X es frontal, con la doble joroba típica del momento abductor de cadera de ~0.8 N·m/kg. L es la longitud de pierna de cada sujeto, en promedio 0.876 m.

| Velocidad | Cadera, extensión | Cadera, flexión | Rodilla, extensión | Tobillo, flexión plantar | Cadera, abducción |
|---|---|---|---|---|---|
| Lenta 0.88 m/s (Fr 0.09) | 0.41 ± 0.13 | 0.47 ± 0.14 | 0.17 ± 0.19 | 1.31 ± 0.12 | 0.77 |
| **Cómoda 1.24 m/s (Fr 0.18)** | **0.61 ± 0.17** | 0.64 ± 0.16 | **0.45 ± 0.23** | **1.46 ± 0.14** | 0.80 |
| Rápida 1.58 m/s (Fr 0.30) | 0.88 ± 0.27 | 0.87 ± 0.23 | 0.69 ± 0.28 | 1.57 ± 0.17 | 0.84 |
| Adimensional M/(m·g·L), cómoda | 0.071 | — | 0.052 | **0.169** | — |

**Advertencia de unidades:** el texto de Fukuchi 2018 que leí no dice explícitamente «N·m/kg». Lo deduzco porque la GRF del mismo fichero está en N/kg (~11) y porque los valores coinciden con la literatura. Así, el «~1–1.5 N·m/kg» que se suele citar vale para el **tobillo**; la cadera y la rodilla quedan en ~0.4–0.9 a velocidades normales.

### 2b. Caballo

- **Trote, pata anterior** (4 caballos, 2.5–5 m/s, dinámica inversa). Picos de **hombro 1.5 ± 0.4** y **codo 1.1 ± 0.3 N·m/kg** (extensores). Picos flexores de **carpo −1.3 ± 0.3**, **nudo (MCP) −1.3 ± 0.3** y articulación interfalangiana distal −0.3 ± 0.2 N·m/kg. Trabajo neto de la pata anterior 0.06 ± 0.11 J/kg; hombro 0.11 ± 0.07 J/kg. **Ferris AE, Dutto DJ, Hoyt DF, Clayton HM, Cogger EA, Wickler SJ**, "Joint kinetics of the horse during trotting: the forelimb during stance", resumen de congreso SICB, https://sicb.org/?p=34064. Es un **resumen de congreso**; el año no aparece en la página.
- **Trote, trabajo por pata.** Con caballos de 491 ± 38 kg: *"Work done by the hindlimb was indeed positive (consistently 0.34 J kg–1 across all speeds)"* y la pata anterior hace un trabajo neto *"essentially zero"*. **Dutto DJ, Hoyt DF, Clayton HM, Cogger EA, Wickler SJ (2006)**, *J Exp Biol* 209:3990–3999, DOI [10.1242/jeb.02471](https://doi.org/10.1242/jeb.02471). En el texto los momentos solo aparecen en figuras (Figs. 3–5), sin números.
- **Paso, solo cualitativo.**
  - En la pata anterior, *"the peak moment [at the shoulder] was considerably higher than at any other joint"*, el codo es la única articulación que genera energía neta y el nudo funciona elásticamente. **Clayton HM, Hodson E, Lanovaz JL (2000)**, *Equine Vet J* 32:295–300, DOI [10.2746/042516400777032174](https://doi.org/10.2746/042516400777032174).
  - En la pata posterior, *"The hip joint was the main source of energy generation throughout the stride."* **Clayton HM, Hodson E, Lanovaz JL, Colborne GR (2001)**, *Equine Vet J* 33:44–48, DOI [10.2746/042516401776767359](https://doi.org/10.2746/042516401776767359).
  - **[no verificado]**: los N·m/kg al paso. Los resúmenes no los dan y no tuve acceso al texto completo.
- **Comparación adimensional [derivado, L supuesta].** Con una longitud de pata anterior L ≈ 1.3–1.5 m (supuesto para un caballo de ~500 kg; no viene de las fuentes), el hombro al trote da M/(m·g·L) ≈ 0.10–0.12 y el codo ≈ 0.075–0.086. Es el mismo orden que la cadera humana al paso rápido (0.10) y menor que el tobillo humano (0.17–0.18). Es decir, **el momento por peso × longitud es del orden de 0.1 en ambos casos**. El cuadrúpedo no cambia el orden de magnitud por articulación; reparte la carga entre más articulaciones.

### 2c. Elefante (Ren et al. 2010)

- **EMA.** *"Mean EMA in normal walking (dimensionless speed 0.33) was 0.68 ± 0.046"*. Es ≈ 0.5 en muñeca y tobillo, baja a *"0.48 ± 0.036 (all joints) at the fastest speeds"* y llega a ≈ 1.0 como máximo en una articulación en marcha lenta.
- **Frente a la ley de escala.** *"Scaling data predict a limb EMA of ~1.75 for an animal of a body mass of 3,000 kg"*, así que los elefantes quedan en ≈ un tercio de lo esperado. Del resumen: *"EMA in elephants is actually smaller than that in horses, which are only one-tenth their mass."* Los brazos de palanca musculares son *"about 36%–69% of those predicted for their size"*.
- **Referencias de EMA que compila Ren:** humano caminando 0.71 ± 0.028, humano corriendo 0.52 ± 0.016, caballo al trote ≈ 1.0 (todas atribuidas a Biewener).
- **Volumen muscular reclutado:** 45–70 cm³ kg⁻¹ m⁻¹, unas 2–4 veces el humano. El coste neto de transporte sigue la recta 0.0030·Vmusc − 0.0944 (mL O₂ kg⁻¹ m⁻¹, R² = 0.88).
- **Trabajo:** la pata anterior hace ≈ el doble de trabajo que la posterior. Los valores en J/kg y W/kg solo están en figuras y material suplementario.
- **[no verificado]**: momentos articulares del elefante en N·m/kg. No encontré ningún artículo publicado con ellos. Ren 2010 da la EMA y la potencia por pata, no los momentos.

### 2d. Biewener: EMA y tamaño

- **Biewener AA (1989)**, "Scaling body support in mammals: limb posture and muscle mechanics", *Science* 245:45–48, DOI [10.1126/science.2740914](https://doi.org/10.1126/science.2740914). Del resumen: *"peak bone stress is independent of size (maintaining a safety factor of between 2 and 4)"*; *"small animals run with crouched postures, whereas larger species run more upright"*; la postura erguida *"likely limits the maneuverability and accelerative capability of large animals."*
- **Exponente.** Bullimore & Burn citan a Biewener 1989 así: *"the mean value of EMA increases with body mass (m) in quadrupedal mammals, in proportion to m^0.26"*, medido en la transición trote–galope, y *"EMA did not change significantly with speed or gait"*. **Bullimore SR, Burn JF (2005)**, *Biol Lett* 1:57–59, DOI [10.1098/rsbl.2004.0243](https://doi.org/10.1098/rsbl.2004.0243), PMC1629047.
- **Biewener AA (2005)**, *J Exp Biol* 208:1665–1676, DOI [10.1242/jeb.01520](https://doi.org/10.1242/jeb.01520): EMA ≈ W^0.25 *"over a size range from mice to horses"* (Fig. 3, datos de Biewener 1989), con tensiones constantes *"across a size range 0.04-300 kg"*. Por encima de ese tamaño, *"extremely large mammals exhibit more pronounced skeletal allometry and reduced locomotor ability."*
- **Biewener AA (1990)**, *Science* 250:1097–1103, DOI [10.1126/science.2251499](https://doi.org/10.1126/science.2251499): tensiones pico del 25–50 % de la resistencia a rotura y factor de seguridad 2–4. La postura más erguida funciona *"over much of their size (0.1 to 300 kilograms)"*; por encima de ese rango, *"increased skeletal allometry and decreased locomotor performance"*.
- **Valores absolutos.** Caballo ≈ 1.0 (Ren 2010, citando a Biewener). Pequeños mamíferos ≈ 0.1 **[derivado]**: es la extrapolación de 1.0 a 500 kg con exponente 0.26 hasta 0.1 kg, que da 0.11. **[no verificado]**: no leí la tabla original de Biewener 1989, que está tras un muro de pago.
- **Lectura para el mecha:**
  - La EMA es una decisión de diseño: «postura columnar» significa un brazo R de la GRF pequeño.
  - Los animales mayores de ~300 kg ya no mantienen la tendencia M^0.26. El elefante tiene una EMA de 0.68, no de 1.75.
  - Por tanto, parametrizar el momento articular como ≈ 0.05–0.17·m·g·L al paso es coherente con humanos, caballos y elefantes. **[derivado]**

---

## 3. Bípedos y cuadrúpedos más grandes

### 3a. Masas

| Animal | Postura | Masa estimada | Fuente |
|---|---|---|---|
| *Tyrannosaurus rex* (adultos) | bípedo obligado | 6–8 t; «Sue» ~9.5 t (modelo mínimo 9502 kg; rango de modelos 9.5–18.5 t) | Hutchinson et al. 2011 |
| *T. rex* | ídem | 7.7 t (ES 0.135 log₁₀, ≈ ×/÷1.37) | Benson et al. 2014, Tabla 1 |
| *T. rex* «Scotty» (RSM P2523.8) | ídem | **8870 kg** [cifra de prensa; el resumen solo dice que supera a todos los T. rex y terópodos gigantes conocidos] | Persons, Currie & Erickson 2020 |
| *Spinosaurus aegyptiacus* | bípedo en tierra (debatido) | 7390 kg (densidad 833 kg/m³) / 6379 kg (7160 kg en la variante densa) | Sereno et al. 2022; Henderson 2018 |
| *Giganotosaurus carolinii* | bípedo obligado | 6.1 t | Benson et al. 2014 |
| *Shantungosaurus giganteus* (hadrosaurio) | bípedo facultativo, cuadrúpedo al caminar | **17 t** | Benson et al. 2014 |
| *Iguanodon bernissartensis* | facultativo | 15 t | Benson et al. 2014 |
| *Ledumahadi mafube* (sauropodomorfo) | cuadrúpedo de patas flexionadas | 12 t | McPhee et al. 2018 |
| *Argentinosaurus huinculensis* | cuadrúpedo | 90 t (IP 95 %: 67.4–124 t, solo con el fémur); 83.2 t; 65–75 t | Benson 2014; Sellers et al. 2013; Paul 2019 |
| *Patagotitan mayorum* | cuadrúpedo | **69 ± 17 t** (volumétrico 45–77 t); 50–55 t | Carballido et al. 2017; Paul 2019 |
| *Dreadnoughtus schrani* | cuadrúpedo | 59.3 t (por ecuación de escala) frente a **22.1–38.2 t** (volumétrico) | Lacovara et al. 2014; Bates et al. 2015 |
| *Brachiosaurus* / *Turiasaurus* | cuadrúpedo | 56 t / 51 t | Benson et al. 2014 |
| *Paraceratherium transouralicum* | cuadrúpedo | ~17 t (los mayores machos; altura a la cruz ~480 cm); la mayoría de los esqueletos, ~8–10 t | Larramendi 2016 |
| *Palaeoloxodon namadicus* | cuadrúpedo | **~22 t** (altura a la cruz ~520 cm), «with a grain of salt», margen ±20 % | Larramendi 2016 |

Citas y detalles:
- **Hutchinson JR, Bates KT, Molnar J, Allen V, Makovicky PJ (2011)**, *PLoS ONE* 6:e26037, DOI [10.1371/journal.pone.0026037](https://doi.org/10.1371/journal.pone.0026037): *"adult T. rex had body masses around 6000–8000 kg, with the largest known specimen ("Sue") perhaps ∼9500 kg"*. También: *"T. rex probably had hip and thigh muscles relatively larger than any extant animal's."*
- **Benson RBJ, Campione NE, Carrano MT, et al. (2014)**, *PLoS Biol* 12:e1001853, DOI [10.1371/journal.pbio.1001853](https://doi.org/10.1371/journal.pbio.1001853), PMC4011683. Tabla 1: *"The standard error of all mass estimates is 0.135 log10(kg)."*
- **Persons WS, Currie PJ, Erickson GM (2020)**, *Anat Rec* 303:656–672, DOI [10.1002/ar.24118](https://doi.org/10.1002/ar.24118). Los 8870 kg los tomé de la prensa (Gizmodo) y no del artículo **[secundario]**. Hutchinson señaló que la diferencia con Sue (~8460 kg en la misma cobertura) cae dentro del error.
- **Sereno PC et al. (2022)**, *eLife* 11:e80092, DOI [10.7554/eLife.80092](https://doi.org/10.7554/eLife.80092): *"the flesh model of S. aegyptiacus has a body mass of 7390 kg"*, y *"on land S. aegyptiacus was bipedal"*.
- **Henderson DM (2018)**, *PeerJ* 6:e5409, DOI [10.7717/peerj.5409](https://doi.org/10.7717/peerj.5409): masa del modelo 6379 kg; el centro de masas *"much closer to the hips than previously estimated"*. En contra, **Ibrahim N et al. (2014)**, *Science* 345:1613, DOI [10.1126/science.1258750](https://doi.org/10.1126/science.1258750), propuso un centro de masas por delante de la rodilla y cuadrupedia en tierra.
- **Carballido JL et al. (2017)**, *Proc R Soc B* 284:20171219, DOI [10.1098/rspb.2017.1219](https://doi.org/10.1098/rspb.2017.1219), PMC5563814: *"estimated body mass of 69 tonnes (±17 tonnes standard error"*. Argentinosaurus y Puertasaurus serían *"approximately 10% smaller"* según el área de las vértebras dorsales.
- **Lacovara KJ et al. (2014)**, *Sci Rep* 4:6196, DOI [10.1038/srep06196](https://doi.org/10.1038/srep06196): 59,291 kg con logBM = 2.749·log C(H+F) − 1.104 (Campione & Evans 2012).
- **Bates KT, Falkingham PL, Macaulay S, Brassey C, Maidment SCR (2015)**, *Biol Lett* 11:20150215, DOI [10.1098/rsbl.2015.0215](https://doi.org/10.1098/rsbl.2015.0215): *"masses above 40 000 kg require high body densities and expansions of soft tissue volume outside the skeleton several times greater than found in living quadrupedal mammals."*
- **Sellers WI, Margetts L, Coria RA, Manning PL (2013)**, *PLoS ONE* 8:e78733, PMC3864407: Argentinosaurus de 83,230 kg (ya en `locomocion_actuadores.md`).
- **Paul GS (2019)**, *Annals of Carnegie Museum* 85(4):335 (página final no verificada), DOI [10.2992/007.085.0403](https://doi.org/10.2992/007.085.0403): Argentinosaurus 65–75 t y Patagotitan 50–55 t. Solo leí el resumen **[secundario]**.
- **Larramendi A (2016)**, "Shoulder height, body mass, and shape of proboscideans", *Acta Palaeontol Pol* 61(3):537–574, DOI [10.4202/app.00136.2014](https://doi.org/10.4202/app.00136.2014). PDF abierto: https://app.pan.pl/archive/published/app61/app001362014.pdf (leído).
  - Paraceratherium: *"A body mass of around 17 tonnes is therefore expected for the largest Paraceratherium bulls."*
  - P. namadicus *"may have been about 5 tonnes heavier and 40 cm taller at the shoulders than the biggest indricotheres."* El Apéndice 1 da ~22 t y ~520 cm y advierte que debe tomarse «with a grain of salt».
  - *"The upper size for land mammals of 20 tonnes, proposed by Economos (1981) … was probably surpassed."*
- **Teoría de límites:**
  - **Economos AC (1981)**, *J Theor Biol* 89:211–214, DOI [10.1016/0022-5193(81)90307-6](https://doi.org/10.1016/0022-5193(81)90307-6): ~20 t para mamíferos.
  - **Hokkanen JEI (1986)**, *J Theor Biol* 118:491–499, DOI [10.1016/S0022-5193(86)80167-9](https://doi.org/10.1016/S0022-5193(86)80167-9): *"The limit is suggested to lie between 10(5) and 10(6) kg."*

**Cociente [derivado].** Bípedos obligados ~7–9.5 t frente a cuadrúpedos de 50–90 t: 5–13 veces en masa, o **1.7–2.3 veces en longitud** si la semejanza fuera isométrica. Los bípedos facultativos de 15–17 t caminaban normalmente a cuatro patas.

### 3b. Por qué los bípedos se quedaron más pequeños

No encontré ningún artículo que demuestre un **límite rígido de masa** para bípedos. Lo que sí hay es evidencia biomecánica y filogenética convergente:

- **Hutchinson JR & Garcia M (2002)**, "Tyrannosaurus was not a fast runner", *Nature* 415:1018–1021, DOI [10.1038/4151018a](https://doi.org/10.1038/4151018a).
  - Del resumen: *"in order to run quickly, an adult Tyrannosaurus would have needed an unreasonably large mass of extensor muscle"* y *"it is doubtful that Tyrannosaurus and other huge dinosaurs (approximately 6,000 kg) were capable runners"*.
  - Según la nota de prensa de ScienceDaily (28 feb 2002, https://www.sciencedaily.com/releases/2002/02/020228072635.htm) **[secundario]**: a 45 mph, *"would need almost 43 percent of its weight in each leg as supportive muscles"* (86 % en total) con postura agachada, y *"13 percent … in each leg"* casi con la pata recta. Un pollo escalado a 6 t necesitaría *"about 99 percent of its body mass in each leg"*.
- **Sellers WI, Pond SB, Brassey CA, Manning PL, Bates KT (2017)**, *PeerJ* 5:e3420, DOI [10.7717/peerj.3420](https://doi.org/10.7717/peerj.3420), PMC5518979.
  - Las marchas de carrera *"would probably lead to unacceptably high skeletal loads in T. rex"*.
  - Con un límite de tensión de 100 MPa (factor de seguridad 2), *"the Froude number at 100 MPa is 1.0 which typically is the upper limit for walking gaits"*. La velocidad máxima es 7.7 m/s solo si se admiten más de 200 MPa.
- **McPhee BW et al. (2018)**, *Curr Biol* 28:3143–3151, DOI [10.1016/j.cub.2018.07.063](https://doi.org/10.1016/j.cub.2018.07.063): *"quadrupedality allowed Triassic sauropodomorphs to achieve body sizes of at least 3.8 metric tons"*; *"A columnar-limbed, quadrupedal posture enabled these giant body sizes"*.
- **Sander PM et al. (2011)**, *Biol Rev* 86:117–155, DOI [10.1111/j.1469-185X.2010.00137.x](https://doi.org/10.1111/j.1469-185X.2010.00137.x), PMC3045712.
  - *"limitations to theropod body size other than prey availability (e.g. biomechanical limits to their bipedal body plan)"*.
  - Sobre la ausencia de aves terrestres de varias toneladas: *"other constraints may have been effective, such as the obligatory bipedalism of birds"*.
  - *"All sauropods were quadrupedal, graviportal animals with massive, columnar limbs."*
- **Vuelta a la cuadrupedia en ornitisquios.** Ocurrió al menos 3 veces de forma independiente y es una transición rara.
  - **Maidment SCR & Barrett PM (2012)**, *Proc R Soc B* 279:3765–3771, DOI [10.1098/rspb.2012.1040](https://doi.org/10.1098/rspb.2012.1040).
  - **Dempsey M, Maidment SCR, Hedrick BP, Bates KT (2023)**, *Proc R Soc B* 290:20222435, DOI [10.1098/rspb.2022.2435](https://doi.org/10.1098/rspb.2022.2435).
  - **Maidment & Barrett (2014; en línea 2012)**, «Osteological correlates for quadrupedality in ornithischian dinosaurs», *Acta Palaeontol Pol* 59(1), DOI [10.4202/app.2012.0065](https://doi.org/10.4202/app.2012.0065): los hadrosaurios eran «probably mostly quadrupedal» **[secundario, según el resumen devuelto por la búsqueda]**.

---

## 4. Las mayores máquinas con patas

| Máquina | Patas | Masa / tamaño | ¿Camina de verdad? | Fuente |
|---|---|---|---|---|
| **Tradinno** (Zollner, 2010) | 4 | **11 t**, 15.7 × 12.3 × 8.2 m, hidráulico, diésel de 140 hp | Sí: es el mayor robot caminante según Guinness | ya en `locomocion_actuadores.md` §6 |
| **Prosthesis «the anti-robot»** (Furrion Exo-Bionics / eatART, 2017–20) | 4 | ~3.5–4 t según la fuente; ~4 m de alto | Sí, pero lo pilota una persona sin autonomía: *"no gyros, no autonomy"*. Guinness 2020, «Largest tetrapod exoskeleton» | prensa (GearJunkie, CBC) **[secundario, cifras contradictorias]** |
| **GE Walking Truck / CAM** (Mosher, 1965–69) | 4 | ~1400 kg (3000 lb); ≤ 8 km/h | Sí, teleoperado por fuerza con retroalimentación; hidráulica desde fuera del vehículo | Wikipedia «Walking Truck», que cita al US Army Transportation Museum **[secundario]**. Primaria: Mosher RS (1969), «Exploring the potential of a quadruped», SAE Technical Paper 690191, DOI [10.4271/690191](https://doi.org/10.4271/690191) **[no leída]** |
| **ASV, Adaptive Suspension Vehicle** (Ohio State, 1985–86) | 6 | ~2.7–3.4 t según la fuente; 5.2 × 2.4 m; ~2.25 m/s | Sí, pilotado | Waldron & McGhee 1986, *IEEE Control Syst. Mag.* 6(6):7–12 **[no leído; cifras secundarias]** |
| **Plustech/Timberjack «Plusjack»** (década de 1990) | 6 | ~13 t según shvachko.net **[secundario, no verificado]** | Sí, prototipo; nunca se fabricó en serie | Museo Lusto: https://lusto.fi/en/exhibitions-and-events/whats-on-at-lusto/time-of-the-machines/ |
| **BigDog** (Boston Dynamics, 2005–08) | 4 | **109 kg**; ~1 m de alto; 1.1 × 0.3 m; motor de 15 hp | Sí: crawl ~0.2 m/s, trote ~1.6 m/s, más de 3.1 m/s al bound; ha llevado 154 kg | Raibert et al. 2008 (leído) |
| **LS3** (Boston Dynamics/DARPA, 2012) | 4 | ≤ 1250 lb (≈ 567 kg) **cargado** (especificación del programa); carga útil 400 lb, 20 millas en 24 h | Sí | DARPA: https://www.darpa.mil/research/programs/legged-squad-support-system ; el límite de 1250 lb, vía Defense Industry Daily **[secundario]** |
| **HyQ** (IIT, 2011) | 4 | ~80 kg (otras fuentes dicen 70–90); ~1 m de largo; pata de 0.78 m | Sí | Semini et al. 2011, *Proc IMechE I* 225:831–849, DOI [10.1177/0959651811402275](https://doi.org/10.1177/0959651811402275) (la masa la tomo del informe técnico del IIT, arXiv:1604.06818) |
| **HyQReal** (IIT/Moog, 2019) | 4 | **130 kg** (prensa 2019) / **140 kg** (página actual del IIT); 1.33–1.35 × 0.9 m | Sí: arrastró un Piaggio P180 de 3.3 t más de 10 m | https://dls.iit.it/hyqreal ; IEEE Spectrum 2019 |
| **ANYmal** (ETH, 2016) / ANYmal D | 4 | ~30 kg / ~50 kg **[secundario]** | Sí; corre a máxima velocidad con < 280 W y > 2 h de autonomía | Hutter et al. 2016, IROS, pp. 38–44, DOI [10.1109/IROS.2016.7758092](https://doi.org/10.1109/IROS.2016.7758092) (resumen) |
| **Spot** (Boston Dynamics) | 4 | **32.5 kg**; carga útil 14 kg; 1.6 m/s | Sí | https://dev.bostondynamics.com/docs/concepts/about_spot ; https://support.bostondynamics.com/articles/Knowledge/Spot-Specifications-49916 |
| **Hyundai Elevate** (CES 2019) / TIGER X-1 (2021) | 4 patas con ruedas | Elevate: concepto presentado como animación, con maquetas a escala 1:8. TIGER X-1: ~50 × 30 × 18 cm | **No** a escala real | prensa (TechRadar, TechCrunch, Engadget) **[secundario]** |
| **Big Muskie** (Bucyrus-Erie 4250-W, 1969–91) | 4 «zapatas» | **13,200 t** (Guinness); 46 m de ancho; cuchara de 168 m³ | **No es marcha con patas.** Según Guinness, *"'walked' around on site on four 6 x 20 m (20 x 65 ft) hydraulically powered 'shoes'"*: la máquina descansa en una base circular y las zapatas la levantan y la arrastran a pasos, de forma cuasiestática y sin ciclo de apoyo ni fase de vuelo | https://www.guinnessworldrecords.com/world-records/77535-largest-dragline-excavator |
| Mononofu / Gundam Yokohama / Archax / Kuratas | 2 (aparentes) | 7.3 t / 25 t / 3.5 t / 4–4.5 t | **No caminan**: van sobre ruedas o colgados de una estructura | ya en `locomocion_actuadores.md` §6 |

- **BigDog**, cita literal: *"BigDog weighs about 109 kg (240 lbs), is about 1 meter tall, 1.1 meters long, and 0.3 m wide"*. Otra: *"Travel speed for the crawl is about 0.2 m/s, for the trot is about 1.6 m/s (3.5 mph), for the running trot is about 2 m/s (4.4 mph) and BigDog briefly exceeded 3.1 m/s (7 mph) while bounding"*. Es decir, **el crawl estático es ~8 veces más lento que el trote**. **Raibert M, Blankespoor K, Nelson G, Playter R (2008)**, "BigDog, the Rough-Terrain Quadruped Robot", *IFAC Proc. Vol.* 41(2):10822–10825, DOI [10.3182/20080706-5-KR-1001.01833](https://doi.org/10.3182/20080706-5-KR-1001.01833). Copia leída: https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/bigdog.pdf
- **Por número de patas, con marcha real:**
  - Cuadrúpedos: hasta **11 t** (Tradinno).
  - Hexápodos: ~3 t (ASV) y quizá ~13 t (Plusjack, sin verificar).
  - Bípedos: ≤ ~1.5 t (Method-2, con cable; véase `locomocion_actuadores.md`).
- Oke et al. 2026 (arXiv:2603.22560, ya en el repo) encuentran que la masa crece como **L^2.72** en robots cuadrúpedos (R² = 0.93) y como L^1.91 en bípedos.

---

## 5. El tronco del cuadrúpedo como viga

- **Gray J (1944)**, "Studies in the mechanics of the tetrapod skeleton", *J Exp Biol* 20:88–116, DOI [10.1242/jeb.20.2.88](https://doi.org/10.1242/jeb.20.2.88). Solo leí el resumen.
  - Punto 15: el cuerpo es *"essentially that of a flexible overhung beam supported by four elastic legs"*; *"only under very special circumstances can the body be compared to two balanced cantilevers"*.
  - Punto 19: la secuencia diagonal de las patas es la única que mantiene *"static equilibrium with its own weight at all phases of the movement"*, de modo que el animal puede detenerse en cualquier momento sin caer.
- **Kienapfel K, Preuschoft H, Wulf A, Wagner H (2018)**, "The biomechanical construction of the horse's body and activity patterns of three important muscles of the trunk in the walk, trot and canter", *J Anim Physiol Anim Nutr* 102(2), DOI [10.1111/jpn.12840](https://doi.org/10.1111/jpn.12840). PDF leído: https://www.ruhr-uni-bochum.de/ecoevo/Bilder/pubs/kiena/kienapfel2017emg.pdf
  - *"The body stem of a quadruped can be compared to a heavy beam on two supports. This beam is exposed to shearing forces and bending stresses under its own weight."*
  - El voladizo anterior (cabeza y cuello) se flecta hacia abajo. *"Between the supports, the trunk tends to sag ventrally downwards, so that compressing forces occur along the upper margin and tension at the lower"*: la columna y el esternón trabajan a compresión y la musculatura a tracción.
  - El cortante es máximo en el hombro y cambia de signo hacia la región toracolumbar.
  - El apoyo diagonal produce **torsión** del tronco, que resisten los músculos oblicuos.
  - Carga dinámica: *"the accelerations in the gaits trot and canter commonly are two times earth acceleration"*, citando a Preuschoft 1985 y a Witte et al. 1995. En el salto: 2.5 g al despegar y 3.7 g al aterrizar.
  - *"In walking, muscle activities are minor"*.
  - La EMG de cinco caballos confirma las predicciones del modelo de viga. Proponen la «teoría de la viga» como ampliación de la «bow-and-string» de **Slijper EJ (1946)**, *Comparative biologic-anatomical investigations on the vertebral column and spinal musculature of mammals*, North-Holland, Ámsterdam. No leí a Slijper directamente; en su modelo, la columna es el arco y la musculatura ventral con el esternón, la cuerda.
- **Voladizos de saurópodo.** Cuello y cola tienen flexión y **torsión**; las colas *"seem to have been carried more or less in a horizontal, extended posture"*. **Preuschoft H, Klein N (2013)**, *PLoS ONE* 8:e78574, DOI [10.1371/journal.pone.0078574](https://doi.org/10.1371/journal.pone.0078574).
- **Para el modelo:**
  - Representar el tronco como una viga de Euler–Bernoulli apoyada en las cinturas escapular y pélvica, con voladizos de cuello y cola y carga distribuida m·g/L.
  - Factor dinámico ~1–1.2 g al paso [interpretación a partir de que la actividad muscular sea «minor» al paso] y ~2 g al trote.
  - Añadir torsión en las fases de apoyo diagonal.
  - Mientras haya solo tres apoyos, la viga queda apoyada en un único punto en uno de sus extremos y en dos en el otro.

---

## 6. Elefantes: velocidad y factor de servicio; marcha estáticamente estable

- **Hutchinson JR, Famini D, Lair R, Kram R (2003)**, "Are fast-moving elephants really running?", *Nature* 422:493–494, DOI [10.1038/422493a](https://doi.org/10.1038/422493a). Leí el PDF.
  - Midieron 42 elefantes asiáticos en 188 ensayos. Alcanzan *"up to 6.8 m s⁻¹ (25 km h⁻¹)"*.
  - Fr = v²/(g·altura de cadera). *"The elephants routinely exceeded Fr 1.0, reaching Fr values as high as 3.4"*.
  - Siempre tienen al menos una pata en el suelo, con *"duty factors as low as 0.37"*.
  - El artículo recuerda que la mayoría de los animales pasan de paso a carrera a Fr ≈ 0.5 y que los cuadrúpedos pasan de trote a galope a Fr ≈ 2.5.
- **Hutchinson JR, Schwerda D, Famini DJ, Dale RH, Fischer MS, Kram R (2006)**, *J Exp Biol* 209:3812–3827, DOI [10.1242/jeb.02443](https://doi.org/10.1242/jeb.02443).
  - Más de 2400 zancadas de 14 elefantes africanos y 48 asiáticos (116–4632 kg), entre 0.40 y 6.8 m/s.
  - La secuencia de pisadas es lateral a todas las velocidades y tiende a un desfase del 25 % (*singlefoot*).
  - El DF de la pata anterior es ≈ 0.03 mayor que el de la posterior.
  - Tabla 3: β = a − b·log û, con û = v/√(g·h): a = 0.53 y b = 0.32 (R² = 0.89) en africanos; a = 0.51 y b = 0.32 (R² = 0.84) en asiáticos.
  - Tabla 2: β entre 0.44 y 0.85 en africanos y entre 0.37 y 0.78 en asiáticos.
  - *"At least two limbs supported the body at speeds less than Fr=1"*, y β ≈ 0.5 hacia Fr ≈ 1.
  - [derivado, suponiendo log₁₀ porque la base no se indica; con ln saldría β ≈ 0.9, más que el máximo observado]: a Fr 0.09 (û 0.30), β ≈ 0.68–0.70.
- **Ren L, Hutchinson JR (2008)**, *J R Soc Interface* 5:195–211, DOI [10.1098/rsif.2007.1095](https://doi.org/10.1098/rsif.2007.1095), PMC2705974.
  - Velocidad óptima *"(a Froude number (Fr) of 0.09)"*, ≈ 1.3 m/s. La transición de marcha es suave a *"approx. 2.2 m s⁻¹, Fr 0.25"*.
  - La recuperación de energía tiene un máximo de 0.35–0.50 a û = 0.30 y cae a ~0.10 por encima de û = 0.50. En cuadrúpedos típicos es ~60–75 %.
  - El centro de masas oscila ~30 mm en vertical.
- **Usherwood JR, Self Davies ZT (2017)**, "Work minimization accounts for footfall phasing in slow quadrupedal gaits", *eLife* 6:e29495, DOI [10.7554/eLife.29495](https://doi.org/10.7554/eLife.29495).
  - Tabla 1, medianas al paso: elefante asiático DF 0.73 (N = 1), africano 0.74 (N = 4), vaca 0.69, jirafa 0.68, rinoceronte 0.68, hipopótamo 0.76.
  - *"at DF <0.75, no footfall timing is capable of allowing continuous progression of the center of mass above a polygon of support"* (citan a Gray 1944 y a McGhee & Frank 1968).
  - *"The DF = 0.75 cut-off is not exact; it is slightly higher with increasing horizontal force amplitude."*
  - Las fases estáticamente estables *"are not adopted (even in tortoises!)"*.
- **McGhee RB, Frank AA (1968)**, "On the stability properties of quadruped creeping gaits", *Math Biosci* 3:331–351, DOI [10.1016/0025-5564(68)90090-4](https://doi.org/10.1016/0025-5564(68)90090-4). El original devolvió 403. El criterio **DF ≥ 3/4** lo tomo de la cita de eLife 2017 **[secundario]**.
- **Consecuencias para el mecha cuadrúpedo:**
  - Los animales grandes **no** caminan con estabilidad estática estricta: el elefante va a DF ~0.7 y siempre con 2 o 3 patas en el suelo.
  - Un crawl con DF ≥ 0.75 baja el pico por pata a ~0.5 BW (§1b), pero limita la velocidad: BigDog va a 0.2 m/s en crawl frente a 1.6 m/s al trote.
  - Rango razonable para el modelo: DF 0.70–0.80 y Fr 0.05–0.25. El límite superior de Fr ~1 marca el inicio de la fase aérea de las patas traseras.

---

## 7. No verificado / limitaciones

- Momentos articulares del elefante en N·m/kg: no encontré ninguna publicación con ellos.
- Momentos del caballo **al paso** en N·m/kg: los resúmenes de Clayton 2000 y 2001 son cualitativos.
- GRF por pata en **vacas**, en BW.
- La GRF del caballo al paso viene de Weishaupt 2005, que solo pude leer como fragmento devuelto por la búsqueda.
- Los 8870 kg de «Scotty» proceden de la prensa.
- Las cifras de Paul 2019 y de Maidment & Barrett 2014 proceden de sus resúmenes.
- Tabla original de Biewener 1989 y valores absolutos de EMA en mamíferos pequeños: no los leí; el ≈ 0.1 es una extrapolación mía.
- La base del logaritmo en la regresión de DF de Hutchinson 2006 no se indica.
- Las unidades de momento de Fukuchi 2018 (N·m/kg) son deducidas, no leídas.
- Robots: GE Walking Truck, ASV, Plusjack, Prosthesis, ANYmal y LS3 cargado tienen cifras de fuentes secundarias, contradictorias entre sí.
- El resumen de Ferris et al. en el SICB no tiene año visible en la página.
