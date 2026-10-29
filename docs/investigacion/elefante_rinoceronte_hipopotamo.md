# Elefante, rinoceronte blanco e hipopótamo: parámetros para tres arquetipos de mecha

Revisado el 2026-10-29. Este informe amplía `cuadrupedo_fuentes.md`. No repito lo que ya está allí: la GRF y la EMA del elefante (Ren et al. 2010), la marcha del elefante (Hutchinson et al. 2003, 2006; Ren & Hutchinson 2008) ni los DF de Usherwood & Self Davies 2017. Aquí solo los uso como dato.

**Etiquetas:**
- **[fuente]**: dato leído en la fuente primaria.
- **[derivado]**: lo calculé yo a partir de datos publicados; explico el cálculo.
- **[secundario]**: lo tomo de una cita de otra obra, sin leer el original.
- **[no verificado]**: no hay dato publicado accesible, o el valor es solo una hipótesis.

**Convenciones:**
- **L** es la altura de la articulación de la cadera sobre el suelo, con el animal de pie. Es la «hip height» de Hutchinson et al. 2006.
- **Ls** es la altura de la articulación del hombro (glenoides).
- **Cruz** es la altura a la cruz («shoulder height» en casi todas las fuentes de campo).
- **V = M/ρ**, con ρ = 1000 kg/m³ (Alexander & Pond 1992 usan esa densidad).
- **Esqueleto:**
  - FLsum = húmero + antebrazo + mano.
  - HLsum = fémur + pierna (crus) + pie.
  - Todas las longitudes van entre superficies articulares, según el método de Belyaev et al. 2025.
  - Ninguna de las dos sumas incluye la escápula ni el ilion.

**Acceso:**
- **Leídos completos:**
  - Vía Europe PMC (XML): Belyaev et al. 2025 (y su Tabla S1 en .xlsx), Hutchinson & Pringle 2024, Panagiotopoulou et al. 2016 y 2019, Etienne et al. 2021 y 2024, Mallet et al. 2019, Usherwood & Self Davies 2017, Warner et al. 2013 y Kilbourne & Hoffman 2013.
  - Alexander & Pond 1992, escaneo del Rhino Resource Center.
  - Coughlin & Fish 2009, PDF del autor en wcupa.edu.
  - Larramendi 2016, PDF de app.pan.pl.
  - Pienaar et al. 1966: solo las pp. 1–5 y 16–24, que son las disponibles en koedoe.co.za.
  - Datos crudos de presión del rinoceronte en Figshare.
- **Leídos solo en parte, vía WebFetch (HTML de journals.biologists.com):** Hutchinson et al. 2006, Ren et al. 2008 y Panagiotopoulou et al. 2012.
- **Bloqueados o no leídos:**
  - peerj.com devolvió 403; usé Europe PMC.
  - int-res.com devolvió 429.
  - No descargué el PDF de JEB: la política del entorno lo denegó y no insistí.
  - Coombs 1978, Alexander et al. 1979 (alometría y tensiones), Alexander & Jayes 1983, Michilsens et al. 2009, Christiansen 1999/2002 y Fisher et al. 2010 están tras muro de pago. De ellos solo conozco el resumen o citas en otras obras.

---

## 1. Elefante (Loxodonta africana / Elephas maximus)

### 1.1 Masa y alturas

| Dato | Valor | Etiqueta / fuente |
|---|---|---|
| Masa media de machos adultos | *L. africana* 5000 kg; *E. maximus* 4000 kg | [secundario] Owen-Smith 1988, citado por Alexander & Pond 1992 |
| Machos medios (grado I, ~90 % de la población) | *L. africana* ♂: cruz 304–336 cm (media 320), **6 t** (5.2–6.9). ♀: 247–273 cm (260), **3 t**. *E. maximus* ♂: 261–289 cm (275), **4 t**. ♀: 228–252 cm (240), **2.7 t** | [fuente] Larramendi 2016, Tabla 8 |
| Récord | *L. africana* ♂: cruz 384–400 cm, 9.5–10.6 t (grado IV). El mayor bien medido: 396 cm (Angola, 1974) | [fuente] Larramendi 2016 |
| Cadera L y cruz medidas en zoológicos | Africanas: 3512 kg (L 1.91, cruz 2.72 m); 3438 kg (2.03 / 2.70); 3365 kg (1.93 / 2.60); 3265 kg (1.68 / 2.58); 4358 kg (1.68 / 2.55); 1681 kg (1.44 / 2.07). Asiáticas: 4373 kg (L 1.90); 4234 kg (1.68); 3284 kg (1.68) | [fuente] Hutchinson et al. 2006, Tabla 1. L se define como *"Hip height (h) from the hip joint to the ground during standing"* |
| Más asiáticas | 3157 kg (L 1.77 m); 2318 kg (1.51 m); 1984 kg (1.40 m) | [fuente] Warner et al. 2013, PLoS ONE 8:e54784, PMC3559824 |
| **L / cruz** | 0.694 ± 0.034 (rango 0.65–0.75, n = 9 africanos de 119 a 4358 kg). Adultos de más de 3 t: 0.70 | [derivado] de la Tabla 1 de Hutchinson 2006. El artículo no define «shoulder height»; supongo que es la cruz |
| Ls / L | ≈ 0.94–0.96 | [derivado] FLsum/HLsum = 0.94 (*E. maximus*) y 0.96 (*L. africana*), de la Tabla S1 de Belyaev 2025. Las extremidades son casi rectas (§1.4) |
| L de un macho africano medio (6 t, cruz 3.2 m) | ≈ 2.2–2.4 m | [derivado] cruz × 0.70 |

### 1.2 Tronco

Tomo los esqueletos de la Tabla S1 de Belyaev et al. 2025 (*J Anat* 246:63–85, DOI [10.1111/joa.14143](https://doi.org/10.1111/joa.14143), PMC11684385). Son 5 *E. maximus* y 5 *L. africana* adultos de museo. Los valores son medias.

| Medida (cm) | *E. maximus* | *L. africana* |
|---|---|---|
| Tronco T+L+S (columna osteológica, sin discos) | 212 (180–230) | 195 (164–214) |
| HLsum (fémur + pierna + pie) | 220 | 205 |
| Anchura máxima de la pelvis (alas del ilion) | 132 | 105 |
| Distancia mínima entre acetábulos | 41 | 33 |
| Costilla más larga (por la curva) | 119 | 116 |

Lectura de la tabla:
- **Tronco / HLsum = 0.95–0.96** [derivado]. El elefante tiene el tronco tan largo como la pata.
- Belyaev lo resume así: *"Their fore‑ and hindlimb height is ~130%–150% of their trunk length"*, contando la escápula y el ilion.
- **Glenoides–acetábulo (GAD).** Ninguna fuente lo mide directamente. Lo estimo como GAD ≈ (0.9–1.0) × (T+L+S), porque el glenoides cae a la altura de las primeras torácicas y el acetábulo bajo el sacro. Resulta **GAD/L ≈ 0.9–1.0** [derivado, supuesto]. Los discos intervertebrales, que la medida excluye, compensan en parte el recorte.
- **Anchura de vía (centro de pie izquierdo a derecho).** Supongo patas verticales en vista frontal; los elefantes tienen huella de vía estrecha. Entonces la anchura ≈ distancia mínima entre acetábulos + un diámetro de cabeza femoral (~0.08 L). Da **≈ 0.25–0.28 L** [derivado, supuesto].
- **Anchura corporal.** Larramendi 2016: *"in proboscideans the belly is generally equal to or barely wider than the hip region"*, y la pelvis mide 1.0–1.15 veces la longitud del fémur. Pelvis máxima/L ≈ 0.55–0.64 [derivado].
- **Profundidad del tronco.** Uso como proxy la costilla más larga: **≈ 0.58–0.60 L** [derivado, proxy].

### 1.3 Segmentos de las extremidades

| Segmento (media, cm) | *E. maximus* | /L* | *L. africana* | /L* |
|---|---|---|---|---|
| Escápula | 82 | 0.40 | 75 | 0.39 |
| Húmero | 91 | 0.44 | 90 | 0.47 |
| Antebrazo (cúbito) | 73 | 0.35 | 68 | 0.35 |
| Mano | 40 | 0.19 | 38 | 0.20 |
| Ilion | 66 | 0.32 | 59 | 0.31 |
| Fémur | 111 | 0.54 | 107 | 0.56 |
| Pierna (tibia) | 64 | 0.31 | 62 | 0.32 |
| Pie | 38 | 0.19 | 36 | 0.19 |

\*L se estima aquí como 0.94·HLsum [derivado, a partir de los ángulos de Ren et al. 2008: muslo a 4°, pierna a −23° y pie a 38° de la vertical]. Las longitudes en cm son [fuente] (Belyaev 2025, Tabla S1).

**Cocientes [derivado]:**
- Húmero/antebrazo = 1.25–1.32.
- Fémur/pierna = 1.74–1.75.
- (Estilopodio + zeugopodio)/autopodio: 4.1 en la mano y 4.6–4.7 en el pie. El elefante tiene segmentos proximales largos y autopodio muy corto.
- Belyaev: *"contrary to the other large herbivorous mammals, elongated due to the length of the proximal segments"*.

**Frente a la alometría de mamíferos:** Alexander & Pond 1992 (Tabla II, con las ecuaciones de Alexander, Jayes et al. 1979) dan *Loxodonta* húmero 0.97, cúbito 0.68, fémur 0.93 y tibia 0.63 veces la longitud prevista [fuente].

### 1.4 Postura en apoyo

Uso a **Ren L, Butler M, Miller C, Paxton H, Schwerda D, Fischer MS, Hutchinson JR (2008)**, *J Exp Biol* 211:2735, DOI [10.1242/jeb.018820](https://doi.org/10.1242/jeb.018820). Son 15 elefantes de 521 a 3684 kg. Los ángulos son a mitad de apoyo, al paso (û 0.25–0.50), con la articulación en ángulo interno (180° = recta) [fuente]:

| Articulación / segmento | Ángulo | Flexión desde recta |
|---|---|---|
| **Codo** | **157 ± 1°** | **23°** |
| Carpo | 186 ± 1° | −6° (hiperextendido) |
| **Rodilla** | **152 ± 1°** | **28°** |
| Tobillo | 117 ± 1° | 63° |
| Brazo (segmento), respecto a la vertical | −19° | — |
| Muslo, respecto a la vertical | 4° | — |
| Pie (segmento), respecto a la vertical | 38° | — |

- Recorrido angular en la zancada (al paso): codo 36°, carpo 66°, rodilla 42°, tobillo 30°.
- Rango máximo *in vitro* (cadáver juvenil): codo 127°, carpo 115°, rodilla 122°, tobillo 67°. Al correr usan el 31–77 % de ese rango.
- La cita clave del artículo: *"the columnar limb orientation that elephants supposedly exemplify is an oversimplification"*.
- Belyaev 2025, citando a Gambaryan 1974: los ángulos de hombro, codo, carpo, cadera y rodilla *"rarely fall below 120°"*.
- Ángulo de barrido de la pata («pace angle»): 36° la anterior y 50° la posterior. Gambaryan & Ruhkyan 1974 [secundario, vía Belyaev 2025].
- Inclinación de los huesos respecto a la fuerza en carrera rápida: húmero 18° y tibia 20° (Alexander, Maloiy et al. 1979) [secundario, vía Alexander & Pond 1992].

### 1.5 Reparto de peso y centro de masas

- **~60 % del peso sobre las patas anteriores** al caminar [fuente] (Ren et al. 2010, ya en el repo).
- De pie: *"30% body weight manus load"* y *"20% body weight pes load"*, por pata. Miller et al. 2008, *J R Soc Interface* 5:465, PMC2607390 [fuente].
- En marcha rápida de *L. africana*, la GRF pico de la anterior es 1.79 veces la de la posterior. Alexander et al. 1979 [secundario, vía Belyaev 2025].
- **Centro de masas.** Con un reparto 60:40, el CM queda a ≈ 0.40 de la distancia entre pies anteriores y posteriores, contando desde los anteriores [derivado, regla de la palanca].

### 1.6 Marcha

- **Velocidad preferida:** Fr ≈ 0.09–0.10, unos 1.0–1.3 m/s.
  - Ren & Hutchinson 2008 ya está en el repo.
  - Panagiotopoulou et al. 2012 dan *"mean steady speed of 1.0 m s–1 (mean Fr 0.10)"* [fuente].
- **DF al paso:** 0.73–0.74 [fuente, ya en el repo]. Con la regresión β = 0.53 − 0.32·log û de Hutchinson 2006, a Fr 0.09 sale β ≈ 0.70 [derivado; la base del log no se indica].
- **Zancada/L.** Hutchinson 2006, Tabla 3 [fuente]: africano L̂ = 2.0·û^0.35; asiático L̂ = 2.1·û^0.33, con L̂ = zancada/h y û = √Fr. A Fr 0.09 da **1.31–1.41** [derivado]; a Fr 0.15, 1.43–1.54.
- **Secuencia de pisadas:** lateral a todas las velocidades. La fase de la anterior respecto a la posterior del mismo lado es 17–19 % al paso (Usherwood & Self Davies 2017, Tabla 1) y tiende a 25 % (*singlefoot*) [fuente].
- **Máximo:** 6.8 m/s, sin fase aérea de todo el cuerpo, DF ≥ 0.37 [fuente, ya en el repo]. Con L = 1.9 m, Fr ≈ 2.5 [derivado].
- **Oscilación vertical:** a paso rápido, la escápula y la cadera oscilan como mucho 10–15 cm, el 3–4 % de la altura. Gambaryan & Ruhkyan 1974 y Hutchinson 2006 [secundario, vía Belyaev 2025].

### 1.7 Pie: área de contacto y presiones

- **Circunferencia del pie [fuente].** Se mide alrededor del pie, a la altura de la uña del dedo III:
  - Asiática hembra de 3400 kg (masa conocida): **mano 1.223 m, pie 1.156 m**.
  - Macho africano de ~5872 kg (estimado): mano 1.656 m.
  - Fuente: Miller et al. 2008, Tabla 2.
  - Africanos de 1500–3000 kg (estimados): pie anterior derecho 1.06–1.27 m, posterior derecho 1.07–1.24 m. Panagiotopoulou et al. 2016, *R Soc Open Sci* 3:160203, PMC5098964, Tabla 1.
- **Área [derivado, círculo de igual perímetro, cota superior].** A = C²/4π:
  - Asiática de 3400 kg: mano **0.119 m²**, pie 0.106 m².
  - Africanos: mano de 0.089 m² (1500 kg) a 0.128 m² (3000 kg).
  - Normalizado: **A/L² ≈ 0.035–0.045** y **A/V^(2/3) ≈ 0.05–0.07**.
- **Regla de campo [fuente].** Cruz ≈ 2 × circunferencia del pie anterior (Miller 2008; Wood 1982 vía Larramendi). En africanos maduros, × 2 + 10 % (Larramendi 2016).
  - De ahí sale A_mano ≈ 0.016–0.020·cruz², o sea ≈ 0.034–0.041·L² [derivado].
- **Presión media bajo la mano** con un 30 % del peso, de pie: ≈ 50–95 kPa [derivado].
- **Presiones medidas al paso** (Fr 0.05–0.08), «mean maximum pressure» por pie en africanos: **200–320 kPa**, con las anteriores por encima de las posteriores. Panagiotopoulou 2016, Tabla 1 [fuente].
  - **Incoherencia:**
    - El mismo texto da *"mean peak pressures … among all ROIs, feet and subjects … 946 kPa"*.
    - Para asiáticos da 567 kPa (Panagiotopoulou 2012, reanalizado).
    - Estos dos valores no casan con la Tabla 1.
    - Además, el Fr de la Tabla 1 parece calculado con la altura a la cruz, no con la de la cadera: 1.11²/(9.81·0.05) = 2.51 m, que coincide con la cruz del sujeto 2.
    - Mientras no se aclare, uso 200–320 kPa como pico por pie.
- **Escala de la presión.** En asiáticos, la presión pico por región crece como M^0.26–0.52 (Panagiotopoulou et al. 2012, *J Exp Biol* 215:1584, DOI [10.1242/jeb.065862](https://doi.org/10.1242/jeb.065862)) [fuente]. En 28 especies de mamíferos, la presión pico crece como ∝ M^0.5 (Michilsens et al. 2009, *J Zool* 279:236, DOI [10.1111/j.1469-7998.2009.00611.x](https://doi.org/10.1111/j.1469-7998.2009.00611.x)) [secundario, solo el resumen].

### 1.8 Masa de las extremidades

**[no verificado]:** no encontré masas de segmentos del elefante. Ren 2010 usa disecciones, pero sus tablas S1–S2 no las leí.

Como sustituto, tomo las regresiones de **Kilbourne BM & Hoffman LC (2013)**, *PLoS ONE* 8:e78392, PMC3832634. Son 44 especies, con masa en gramos y log₁₀ [fuente]:
- Posterior (desde la cadera): log m = −1.15 + 1.03·log M.
- Anterior (incluye la escápula): log m = −1.32 + 1.01·log M.

Extrapolando a 1.5–6 t: cada anterior ≈ 5.5–5.6 % M, cada posterior ≈ 11 % M, **las cuatro patas ≈ 32–34 % M** [derivado]. Ojo: es una extrapolación muy fuera del rango ajustado, cuyo animal mayor es un caballo de 446 kg; la tomo como orden de magnitud. Gambaryan 1974 da proporciones musculares dentro de la pata, pero no la masa de la pata [secundario, vía Belyaev].

---

## 2. Rinoceronte blanco (Ceratotherium simum)

### 2.1 Masa y alturas

| Dato | Valor | Etiqueta / fuente |
|---|---|---|
| Masa adulta | 1350–3500 kg, media 2300 kg (Dinerstein 2011); hasta 3600 kg (Groves 1972 y otros) | [secundario] vía Etienne et al. 2024 y Panagiotopoulou et al. 2019 |
| Masa media de machos adultos | 2200 kg | [secundario] Owen-Smith 1988, vía Alexander & Pond 1992 |
| Cruz y longitud total | cruz 150–180 cm; longitud corporal total 340–420 cm | [secundario] Dinerstein 2011, vía Mallet et al. 2019, Tabla 1 (*PeerJ* 7:e7647, PMC6766374) |
| Hembras de zoológico medidas | 2500 kg (estimada), cruz 1.50 m; 2500 kg (estimada), cruz 1.42 m | [fuente] Panagiotopoulou et al. 2019, *PeerJ* 7:e6881, PMC6525597 |
| Cadáver de modelo musculoesquelético | hembra de más de 40 años, 2160 kg. En la pose de pie, el CM del segmento escapular está a 1.19 m | [fuente] Etienne et al. 2024, *J Anat*, DOI [10.1111/joa.14041](https://doi.org/10.1111/joa.14041), PMC11259748; Etienne et al. 2021, *PeerJ* 9:e11314 |
| Hembra joven (14 meses, ~750 kg) | 2.76 m del labio superior a la base de la cola; pata anterior de 1.55 m de la cruz a la suela, medida sobre la piel | [fuente] Alexander & Pond 1992 |
| **L (cadera)** | **≈ 0.95–1.10 m** para un adulto de unos 2.3 t | **[derivado; no hay medida publicada]**: 0.87 × HLsum (113 cm, macho RG 35146). El 0.87 supone una flexión moderada de rodilla y tobillo y un pie semidigitígrado inclinado |
| Ls / L | ≈ 0.9 | [derivado] FLsum/HLsum = 0.89 |
| Cruz / L | ≈ 1.5–1.6 | [derivado] |

### 2.2 Tronco

Belyaev 2025, Tabla S1. *C. simum*: n = 2 (macho RG 35146 y una hembra del zoo de Rostov).

| Medida (cm) | Valor | /L* |
|---|---|---|
| Tronco T+L+S | 166 | 1.69 |
| Anchura máxima de la pelvis | 78–88 | 0.84 |
| Distancia mínima entre acetábulos | 20.5 | 0.21 |
| Costilla más larga | 96.5 | 0.98 |

\*L* = 0.87·HLsum = 98 cm [derivado].

- **Tronco/HLsum = 1.47** [derivado]. Otros rinocerontes: *Diceros* 1.41, *R. unicornis* 1.42.
- La región torácica ocupa el 75 % del tronco, la mayor proporción de todos los ungulados estudiados. El lumbar es unas 6 veces más corto que el torácico (Belyaev) [fuente].
- **GAD/L ≈ 1.5–1.7** [derivado, mismo supuesto que en §1.2].
- **Anchura de vía ≈ 0.3 L** [derivado: acetábulos + ~0.1 L].
- **Profundidad del tronco ≈ 1.0 L** [derivado, proxy de la costilla].

### 2.3 Segmentos

| Segmento | cm | /L* | Notas |
|---|---|---|---|
| Escápula | 52 | 0.53 | |
| Húmero | 37.6 | 0.38 | |
| Antebrazo (radio) | 32.8 | 0.33 | |
| Mano | 30.5 | 0.31 | |
| Ilion | 35.8 | 0.36 | |
| Fémur | 47.8 | 0.49 | |
| Pierna | 30.6 | 0.31 | |
| Pie | 34.0 | 0.35 | |

**Cocientes [derivado]:**
- Húmero/antebrazo = 1.15.
- Fémur/pierna = 1.56.
- (Estilopodio + zeugopodio)/autopodio = 2.3 en ambas patas. El autopodio pesa en la longitud mucho más que en el elefante (4.1–4.7).

**Frente a la alometría:** húmero 0.69, cúbito 0.62, fémur 0.63 y tibia 0.52 veces lo previsto. Son patas cortas. Alexander & Pond 1992, Tabla II [fuente].

**Interpretación:** *"The long, relatively straight legs of elephants … are contrasted with the shorter, less straight legs of the other graviportal mammals"*. Alexander & Pond 1992 [fuente].

### 2.4 Postura

- **[no verificado]:** no existe ningún estudio cinemático con ángulos articulares de rinocerontes.
- **Lo cuantitativo que hay [fuente]:**
  - Inclinación de los huesos respecto a la fuerza del pie a mitad de apoyo, al **trote**: **húmero 50°, tibia 39°**. En el elefante corriendo son 18° y 20°. Alexander & Pond 1992, Tabla III.
  - *"in trotting the bones made larger angles with the vertical at mid stance"* que al galope.
- **Cualitativo [secundario]:** *"Rhinoceros limbs are not as columnar as those of walking elephants, and still present a noticeable flexion of all joints when standing at rest"*. Christiansen & Paul 2001, vía Etienne et al. 2021.
- **Modelo estático de pie** (Etienne 2024) [fuente]:
  - Fuerzas de reacción articular, con la pata anterior cargando el 30 % del peso: hombro 37 %, codo 70 %, carpo 68 % y metacarpofalángica 12 % BW.
  - Pata posterior, cargando el 20 %: cadera 31 %, rodilla 62 %, tobillo 53 % y metatarsofalángica 13 % BW.
  - Músculo más activo: *ulnaris lateralis*, 9239 N (44 % BW, activación 0.80).
  - Brazos de momento: supraespinoso 11.3 cm (extensión del hombro), tríceps lateral 11.2 cm (codo), gluteobíceps caudal 17 cm (cadera).
  - La pose se ajustó a fotos; los ángulos en grados no se publican en el texto (Figura S2).

### 2.5 Reparto de peso y centro de masas

- **64:36 delante/detrás** según el CM de un modelo 3D «admittedly simplified, crude», con densidad homogénea. Etienne et al. 2024 [fuente] lo consideran compatible con el 60:40 típico y simulan 60:40.
- Alexander & Pond 1992 también suponen un 60 % delante (por analogía con el caballo).
- **CM a ≈ 0.36–0.40** de la distancia entre pies, contando desde los anteriores [derivado].

### 2.6 Marcha

- **Paso:**
  - DF 0.68 y fase 21 %: secuencia lateral, con pares laterales («lateral couplets»). Usherwood & Self Davies 2017, Tabla 1; N = 2 vídeos [fuente].
  - Según Hutchinson & Pringle 2024, los rinocerontes usan *"a lateral sequence walk, true trot and transverse gallop"* [fuente].
- **Velocidades medidas al paso:** solo pasos muy lentos en zoológico, 0.46–0.87 m/s. Fr = 0.001–0.054, calculado con la altura a la cruz. Panagiotopoulou et al. 2019, Tabla 1 [fuente].
  - **[no verificado]:** el Fr preferido.
- **Zancada/L.** Alexander & Jayes 1983 encontraron que *"at any particular Froude number they use about the same duty factor and relative stride length as other cursorial mammals"* (cita tomada de Alexander & Pond 1992) [fuente].
  - Por eso aplico la relación general de Alexander 1976: λ/h ≈ 2.3·Fr^0.3 [secundario, fórmula muy citada].
  - Resultado: **zancada/L ≈ 0.94–1.15 a Fr 0.05–0.10** [derivado].
- **Trote y galope [fuente].** Alexander & Pond 1992, filmados en Whipsnade:
  - DF al trote 0.43–0.54; al galope 0.39–0.49.
  - DF mínimo 0.39, tanto delante como detrás.
  - Galope transverso con fase aérea; adultos a 6.1 m/s y **hasta 7.5 m/s**.
  - Pasan del trote al galope al mismo Fr que otros mamíferos.
  - Con L ≈ 1.0 m, **Fr máx ≈ 5.5** [derivado].
- **Tensiones óseas al trotar** [fuente]: húmero −59/+47 MPa y tibia −39/+25 MPa. Son menores que en el búfalo (−113/+93) y en el elefante (−85/+69). El indicador de resistencia Z/(aWx) (GPa⁻¹) vale para húmero, fémur y tibia:
  - *Ceratotherium*: 31 / 26 / 33.
  - *Loxodonta*: 11 / 7 / 9.
  - Búfalo: 21 / 22 / 27.
  - Conclusión: el rinoceronte tiene huesos más «sobrados» que el elefante.

### 2.7 Pie: área y presiones

- **Presiones publicadas [fuente, calibración dudosa]:** «mean maximum pressure» por pie de 12–28 N/cm² en dos hembras adultas (un pie posterior da 2 N/cm²; lo trato como anómalo). La media por sujeto es 22 y 18 N/cm², es decir **180–220 kPa**, y la de todos los pies, 20 N/cm². Las anteriores quedan por encima de las posteriores. Panagiotopoulou et al. 2019, Tabla 1.
  - Los autores avisan: *"absolute pressure values may be inaccurate"*. La placa se calibró con un humano de ~95 kg.
- **Área de contacto [derivado de los datos crudos].** Calculada por mí sobre el conjunto crudo de Figshare ([10.6084/m9.figshare.7608797](https://doi.org/10.6084/m9.figshare.7608797)):
  - Tomé las huellas espacial y temporalmente completas y apliqué un umbral de 0.5 N/cm². Cada sensor mide 7.62 × 5.08 mm.
  - Hembras adultas de ~2500 kg (estimada):
    - Huella máxima: **0.036–0.042 m², media ≈ 0.039 m²** (n = 11).
    - Área instantánea máxima ≈ 0.036 m².
    - Dimensiones ≈ 27–30 cm de largo × 21–25 cm de ancho.
  - No pude separar las huellas anteriores de las posteriores.
  - **A/L² ≈ 0.035; A/V^(2/3) ≈ 0.020–0.025.** El rango depende de si la masa real es de 2.0 o 2.5 t; las masas eran estimaciones.
  - Presión media con un 30 % del peso: ≈ 150–200 kPa.
  - Los máximos de un solo sensor en los datos crudos son 52, 69 y 137 N/cm², pero los valores se repiten exactos, lo que hace pensar en saturación o cuantización del sensor. No los uso.
  - Los datos del juvenil son incoherentes: 1000 kg con 0.65 m a la cruz. Los descarto.
- **Pie:** tres dedos (II–IV) con cascos y una almohadilla adiposa bilobulada, más pequeña que la del elefante. La presión baja en la almohadilla y sube en los cascos. El centro de presión entra por el lado medial y sale por el dedo III [fuente].

### 2.8 Masa de las extremidades

**[no verificado]** en masa total.
- Etienne 2024 reconstruyó la masa y la inercia de cada segmento, pero solo en material suplementario, que no leí.
- Etienne 2021: los músculos más fuertes son los proximales. El PCSA del antebrazo es ~45 % del de los extrínsecos, frente al 85 % del caballo [fuente].
- Extrapolación de Kilbourne & Hoffman a 2.3 t: ≈ 33 % M en las cuatro patas [derivado, baja confianza].

---

## 3. Hipopótamo común (Hippopotamus amphibius)

### 3.1 Masa y alturas

| Dato | Valor | Etiqueta / fuente |
|---|---|---|
| Masa adulta típica | ~1500 kg; individuos mayores de más de 3800 kg (citado en Garland 1983) | [secundario] Owen-Smith 1988 y Silva & Downing 1995, vía Hutchinson & Pringle 2024 |
| Adultos sacrificados en Kruger (n = 68 de 104) | Clase de peso de los adultos: 2100–4000+ lb, es decir **953–1814+ kg**. El macho más pesado, 4412 lb (**2001 kg**); la hembra más pesada, 3696 lb (1676 kg). Pesados en partes con balanza de resorte | [fuente] Pienaar, Van Wyk & Fairall 1966, *Koedoe* 9:1–33, DOI [10.4102/koedoe.v9i1.778](https://doi.org/10.4102/koedoe.v9i1.778) |
| Rango y cruz | *"approximately 1,000–4,500 kg and reach a height of about 1.5 m at the shoulder"* | [secundario] Nowak 1999, vía Coughlin & Fish 2009 (*J Mammal* 90:675, DOI [10.1644/08-MAMM-A-279R.1](https://doi.org/10.1644/08-MAMM-A-279R.1)) |
| Hembras de acuario | ~1360 kg cada una | [fuente] Coughlin & Fish 2009 |
| Cruz por sexos | ♂ 1.40–1.65 m; ♀ 1.30–1.45 m | [secundario / no verificado] Wikipedia; no pude identificar la referencia primaria |
| **L (cadera) medida** | macho de 19 años **~1.3 m**; hembra de 23 años **~1.2 m**. Masas desconocidas | [fuente, aproximada] Hutchinson & Pringle 2024, *PeerJ* 12:e17675, PMC11227274 |
| L según el esqueleto | ≈ 1.0–1.1 m (0.87 × HLsum, con HLsum 112–124 cm) | [derivado]. Queda por debajo de la medida en vivo; los ejemplares de museo pueden ser más pequeños |
| **L nominal** | **≈ 1.15 m (1.0–1.3)** | [derivado] |
| Ls / L | ≈ 0.8 | [derivado] FLsum/HLsum = 0.81: la pata anterior es claramente más corta |
| Cruz / L | ≈ 1.2–1.4 | [derivado] |

### 3.2 Tronco

Belyaev 2025, Tabla S1. *H. amphibius*: n = 3. Ojo: la media de la familia en el texto del artículo incluye dos *Choeropsis*; aquí uso solo *H. amphibius*.

| Medida (cm) | Valor | /L* |
|---|---|---|
| Tronco T+L+S | 163 (155–170) | 1.58 |
| Anchura máxima de la pelvis | 71 (68–77) | 0.69 |
| Distancia mínima entre acetábulos | 29.5 (28–32) | 0.29 |
| Costilla más larga | 82 (71.5–92) | 0.80 |

\*L* = 0.87·HLsum = 103 cm [derivado]. Si se normaliza con la L medida en vivo (~1.2 m), divide estos cocientes por ~1.15.

- **Tronco/HLsum = 1.38** [derivado].
- **GAD/L ≈ 1.4–1.6** [derivado].
- **Anchura de vía ≈ 0.39 L** [derivado]. Es la más ancha de los tres, coherente con el *"wide body and relatively short legs"* del hipopótamo (Dagg 1979 y Bakker 1975, vía Hutchinson & Pringle) [secundario].
- **Profundidad del tronco ≈ 0.8 L** [derivado, proxy].
- Torácico/lumbar ≈ 3; las 15 torácicas son menos que las 18–21 de rinocerontes y elefantes. Belyaev [fuente].

### 3.3 Segmentos

| Segmento | cm | /L* |
|---|---|---|
| Escápula | 43 | 0.42 |
| Húmero | 36.2 | 0.35 |
| Antebrazo (radio) | 25.2 | 0.25 |
| Mano | 33.8 | 0.33 |
| Ilion | 33.8 | 0.33 |
| Fémur | 49.0 | 0.48 |
| Pierna | 30.0 | 0.29 |
| Pie | 38.5 | 0.37 |

**Cocientes [derivado]:**
- Húmero/antebrazo = 1.44. Es el antebrazo más corto de los tres.
- Fémur/pierna = 1.63.
- (Estilopodio + zeugopodio)/autopodio: 1.8 en la mano y 2.05 en el pie.
- Según Belyaev, *"the length of the manus is either equal to (rhinos) or exceeds the length of the antebrachium (tapirs and hippos)"* [fuente].

**Pie (Fisher, Scott & Adrian 2010, *Zool J Linn Soc* 158:661, DOI [10.1111/j.1096-3642.2009.00558.x](https://doi.org/10.1111/j.1096-3642.2009.00558.x)) [secundario, solo el resumen]:** cuatro dedos que cargan peso. La musculatura intrínseca impide que se abran en suelo blando.

### 3.4 Postura

**[no verificado]:** no hay ángulos articulares publicados.
- Alexander & Pond 1992 agrupan al hipopótamo con el rinoceronte: *"much less straight (but also much shorter) legs of rhinoceros and hippopotamus"* [fuente].
- La pelvis está a ~45° (Eltringham 1999) [secundario, vía Wikipedia].

### 3.5 Reparto de peso y centro de masas

**[no verificado]:** no hay ningún dato cinético del hipopótamo (*"no kinetic data exist for hippos"*, Hutchinson & Pringle 2024).
- Los autores suponen *"greater antigravity supportive roles of the forelimbs (typical of quadrupedal mammals)"*.
- Hutchinson & Pringle dan un DF anterior ligeramente mayor (mediana 0.76 frente a 0.75).
- Para el modelo, uso ~60 % delante como supuesto.

### 3.6 Marcha

Hutchinson & Pringle 2024 analizaron 169 zancadas de 32 hipopótamos [fuente]:
- **Siempre trotan.** Fases medias: RH 0.51 ± 0.05, RF 0.94 ± 0.04, LF 0.46 ± 0.05. Hay un «trote al paso» con DF ≥ 0.5 y un «trote corriendo» con DF < 0.5. Los datos se agrupan en DF 0.36–0.58 y 0.75–0.94.
- **DF al paso:**
  - Usherwood & Self Davies 2017: 0.76, fase 45 % [fuente].
  - Lees et al. 2016: 0.73–0.74, con apoyo de 1.12–1.48 s, vuelo de 0.41–0.52 s y SF 0.50–0.65 Hz (reanalizados por Hutchinson & Pringle) [fuente].
- **Regresiones [fuente]:**
  - Apoyo = 8.506·DF^7.188 s.
  - Vuelo = 0.4817·DF^0.7119 s.
  - SF = −4.14·DF + 3.89 Hz.
- **Fase aérea.** Al correr (DF < 0.5) hay fases aéreas breves: *"apparently a new discovery"*.
  - DF mínimo 0.36; SF hasta 3.2 Hz; apoyo mínimo 0.17 s y vuelo mínimo 0.13 s.
  - Por la geometría del trote, cada fase aérea ≈ 0.5 − DF ≈ 0.14 del ciclo, o sea ≈ 0.045–0.05 s a 2.8–3.2 Hz [derivado].
  - La cifra de «0.3 s» de la prensa no está en el artículo [secundario / no verificado].
- **Sin galope en tierra.**
  - Bajo el agua usan un galope de «punting» con fases sin apoyo, a 0.47 m/s de media (Coughlin & Fish 2009) [fuente].
  - Belyaev lo resume: *"The common hippo employs gallop to run underwater; however, it employs the trot … for fast terrestrial running"*.
- **Velocidades: [no verificado].**
  - Hutchinson & Pringle no pudieron medir velocidad ni zancada, porque no había escala en los vídeos.
  - Las cifras de ~8 m/s carecen de documentación empírica.
- **Fr al paso y zancada/L [derivado, baja confianza].** Combino SF = 0.50–0.65 Hz con λ/h = 2.3·Fr^0.3 y L = 1.1–1.25 m. Resulta Fr ≈ 0.01–0.04 (0.3–0.7 m/s) y **zancada/L ≈ 0.55–0.9**.
- **Controversia:** Slijper 1946, Dagg 1973, Niemitz 2001, Coughlin & Fish 2009 y Catavitello et al. 2018 describen un paso de secuencia lateral. Hutchinson & Pringle no lo observaron; quizá aparece solo al pastar muy despacio.

### 3.7 Pie: área y presiones

**[no verificado].**
- Michilsens et al. 2009 midieron presiones plantares en un hipopótamo: Panagiotopoulou 2019 cita las *"hippopotamus and tapir COP traces in Fig. 1 of Michilsens et al., 2009"*. Pero el artículo está tras un muro de pago y no leí los números.
- **Hipótesis para el modelo [derivado, no verificado]:** escalar el área del rinoceronte con A/V^(2/3) constante. Para 1500 kg da A ≈ 0.028 m² por pie, A/L² ≈ 0.021 y presión media ≈ 110–160 kPa.

### 3.8 Masa de las extremidades

**[no verificado].** La extrapolación de Kilbourne & Hoffman a 1.5 t da ≈ 33 % M [derivado, baja confianza].

---

## 4. Los tres comparados: graviportal, mediportal y «columnar»

- **Definición clásica [secundario, vía Mallet et al. 2019].** Graviportal (Gregory 1912; Osborn 1929; Coombs 1978) se define así:
  - masa de varios cientos de kg;
  - *"columnar limbs with stylopodium lengthening and autopodium shortening"*;
  - huesos robustos, pies grandes con almohadillas adiposas y falanges reducidas;
  - *"long strides associated with the inability to gallop"*.
  - Mediportal es la categoría intermedia.
  - Hildebrand 1974 propuso un umbral arbitrario de 900 kg.
- **Clasificación de los tres** (Mallet 2019, Tabla 1, y su texto):
  - **Elefante:** graviportal sin discusión, con Coombs 1978 y Langman et al. 1995.
  - **Hipopótamo:** mediportal para Coombs 1978 y Ross 1984; graviportal para Alexander & Pond 1992, Carrano 1999 y Stilson et al. 2016.
  - **Rinoceronte blanco:** mediportal para Gregory, Osborn y Coombs; graviportal para Eisenmann & Guérin 1984 y para Becker 2003, este con un índice de gracilidad del metápodo.
  - Etienne et al. 2021: *"very few convergences were identified between the three clades defined as graviportal"* en la musculatura.
- **Tres soluciones al mismo problema:** el rinoceronte galopa con el lomo casi rígido, el hipopótamo trota (y galopa solo bajo el agua) y el elefante camina rápido sin fase aérea. Belyaev et al. 2025 [fuente].
- **Patas largas y rectas frente a cortas y flexionadas.**
  - Alexander & Pond 1992: el elefante tiene huesos largos de bajo indicador de resistencia y compensa la tensión *"by keeping the legs much straighter than in rhinoceros"*.
  - Biewener 1989 y 1990 (ya en el repo): la postura erguida mantiene constante la tensión ósea hasta ~300 kg. Por encima hay más alometría ósea y menos rendimiento.
- **Proporciones (Belyaev 2025) [fuente]:**
  - La pata del elefante, contando la cintura, mide 130–150 % del tronco; la de rinocerontes e hipopótamos, ~85–95 %.
  - El húmero del elefante duplica en longitud relativa al de otros ungulados.
  - La escápula y la pelvis del elefante son unas dos veces más anchas que las de cualquier otro herbívoro grande.
- **Por qué son los más pesados.** Es una lectura que tomo de las fuentes, no un resultado único:
  - Postura erguida o columnar, que da un brazo pequeño a la GRF.
  - DF alto, que da GRF pico baja.
  - Pies con almohadilla.
  - Lomo rígido (dorsostable).
  - Abandono de los galopes que flexionan la columna.
  - Factores de seguridad mayores en las especies más cortas de patas.

---

## 5. Tabla resumen normalizada por L

Los arquetipos usados son:
- **Elefante:** hembra africana de zoológico de ~3.4 t (L 1.9 m).
- **Rinoceronte blanco:** adulto de ~2.3 t (L ≈ 1.0 m, derivado).
- **Hipopótamo:** adulto de ~1.5 t (L ≈ 1.15 m, derivado).

Las proporciones esqueléticas vienen de la Tabla S1 de Belyaev 2025, normalizadas con L = k·HLsum.

| Parámetro | Elefante | Rinoceronte blanco | Hipopótamo |
|---|---|---|---|
| Masa típica (máxima) | 3–6 t; ♂ africano medio 6 t (récord ~10 t) [fuente: Larramendi 2016] | 2.3 t (1.35–3.6 t) [secundario: Dinerstein 2011] | ~1.5 t; adultos de Kruger 0.95–2.0 t [fuente: Pienaar 1966]; hasta 3.8–4.5 t [secundario] |
| L (cadera) | 1.68–2.10 m a 3.3–4.6 t [fuente: Hutchinson 2006]; ~2.2–2.4 m en ♂ de 6 t [derivado] | ≈ 0.95–1.10 m [derivado] | ~1.2–1.3 m [fuente, aprox.]; 1.0–1.1 m por esqueleto [derivado] |
| Cruz / L | 1.44 (1.33–1.54); L/cruz = 0.69 ± 0.03 [derivado de fuente] | ≈ 1.5–1.6 [derivado] | ≈ 1.2–1.4 [derivado] |
| Ls / L | ≈ 0.95 [derivado] | ≈ 0.9 [derivado] | ≈ 0.8 [derivado] |
| Tronco (T+L+S) / L | 1.01–1.02 [derivado] | 1.69 [derivado] | 1.58 [derivado] |
| Glenoides–acetábulo / L | ≈ 0.9–1.0 [derivado, supuesto] | ≈ 1.5–1.7 [derivado, supuesto] | ≈ 1.4–1.6 [derivado, supuesto] |
| Anchura de vía / L | ≈ 0.25–0.28 [derivado, supuesto] | ≈ 0.3 [derivado, supuesto] | ≈ 0.39 [derivado, supuesto] |
| Anchura máxima de la pelvis / L | 0.55–0.64 [derivado] | 0.84 [derivado] | 0.69 [derivado] |
| Profundidad del tronco / L (proxy: costilla) | ≈ 0.58–0.60 [derivado, proxy] | ≈ 0.98 [derivado, proxy] | ≈ 0.80 [derivado, proxy] |
| Húmero / antebrazo | 1.25–1.32 [derivado de fuente] | 1.15 [derivado de fuente] | 1.44 [derivado de fuente] |
| Fémur / pierna | 1.74–1.75 [derivado de fuente] | 1.56 [derivado de fuente] | 1.63 [derivado de fuente] |
| Segmentos /L: hum, ant, mano / fém, pierna, pie | 0.44–0.47, 0.35, 0.19–0.20 / 0.54–0.56, 0.31–0.32, 0.19 [derivado] | 0.38, 0.33, 0.31 / 0.49, 0.31, 0.35 [derivado] | 0.35, 0.25, 0.33 / 0.48, 0.29, 0.37 [derivado] |
| Flexión a mitad de apoyo: codo / rodilla | **23° / 28°**; carpo −6°, tobillo 63° [fuente: Ren 2008] | **[no verificado]**: «flexión notable de todas las articulaciones»; huesos a 50° (húmero) y 39° (tibia) de la fuerza al trote, frente a 18° y 20° en el elefante [fuente: A&P 1992] | **[no verificado]**: patas «menos rectas» [fuente: A&P 1992] |
| Fracción del peso delante | 0.60 [fuente: Ren 2010; Miller 2008] | 0.60–0.64 [fuente: modelo de CM burdo, Etienne 2024] | ~0.6 [no verificado, supuesto] |
| CM, desde los pies anteriores (fracción de la distancia entre pies) | ≈ 0.40 [derivado] | ≈ 0.36–0.40 [derivado] | [no verificado] |
| DF al paso | 0.73–0.74 [fuente: Usherwood 2017]; 0.70 a Fr 0.09 [derivado de Hutchinson 2006] | 0.68 [fuente: Usherwood 2017, N = 2] | 0.76 [fuente: Usherwood 2017]; 0.73–0.74 [fuente: Lees 2016 vía H&P 2024]; 0.75–0.94 [fuente: H&P 2024] |
| Fase (secuencia de pisadas) | lateral, 17–19 % → 25 % [fuente] | lateral, 21 % [fuente] | trote, 45–50 % [fuente] |
| Fr al paso | 0.09–0.10 preferido [fuente: Ren & Hutchinson 2008; Panagiotopoulou 2012] | 0.001–0.054 medido en zoológico, con la cruz [fuente]; preferido [no verificado] | ≈ 0.01–0.04 [derivado, baja confianza] |
| Zancada / L al paso | 1.31–1.41 a Fr 0.09 [derivado de la regresión de Hutchinson 2006] | 0.94–1.15 a Fr 0.05–0.10 [derivado: Alexander 1976 + A&J 1983] | ≈ 0.55–0.9 [derivado, baja confianza] |
| Marchas y velocidad máxima | solo secuencia lateral; 6.8 m/s; sin fase aérea; DF mín 0.37; Fr máx ~2.5–3.4 [fuente] | paso, trote y galope transverso con fase aérea; 7.5 m/s; DF mín 0.39; Fr ≈ 5.5 [fuente; Fr derivado] | solo trote; fase aérea breve a DF < 0.5; DF mín 0.36; SF máx 3.2 Hz; velocidad [no verificado] |
| Área del pie (por pie) | mano 0.09–0.13 m² a 1.5–3.4 t; 0.22 m² a ~5.9 t [derivado de la circunferencia; cota superior] | 0.036–0.042 m² a ~2.5 t (est.) [derivado de los datos crudos] | ≈ 0.028 m² [no verificado, escalado] |
| A / L² | ≈ 0.035–0.045 [derivado] | ≈ 0.035 [derivado] | ≈ 0.02 [no verificado] |
| A / (M/ρ)^(2/3) | ≈ 0.05–0.07 [derivado] | ≈ 0.020–0.025 [derivado] | ≈ 0.02 [no verificado] |
| Presión pico al paso | 200–320 kPa por pie (Fr 0.05–0.08) [fuente: Panagiotopoulou 2016, Tabla 1]; el mismo artículo da 946 kPa (africanos) y 567 kPa (asiáticos) como «mean peak» [incoherente] | 180–220 kPa de media por sujeto; 120–280 kPa por pie [fuente: Panagiotopoulou 2019; calibración dudosa] | [no verificado] |
| Presión media bajo un pie con el 30 % del peso | ≈ 50–95 kPa [derivado] | ≈ 150–200 kPa [derivado] | ≈ 110–160 kPa [no verificado] |
| Masa de las cuatro patas / M | ≈ 0.32–0.34 [derivado: extrapolación de Kilbourne & Hoffman 2013; baja confianza] | ≈ 0.33 [ídem] | ≈ 0.33 [ídem] |

**Lectura para los tres arquetipos de mecha:**
- **Elefante:** patas largas y casi rectas, con L ≈ tronco. Autopodio muy corto y pies enormes (A/V^(2/3) unas 2.5 veces la del rinoceronte). DF alto, solo secuencia lateral, nunca aéreo. Pide un EMA alto por postura, no por brazos de palanca grandes.
- **Rinoceronte:** patas cortas y flexionadas, con L ≈ 0.6 × tronco. Tiene el mayor margen estructural: es el único de los tres que galopa. Lomo rígido.
- **Hipopótamo:** el tronco más ancho en relación con L, con la pata anterior claramente más corta (Ls ≈ 0.8 L). Marcha de diagonales sincronizadas: trote a todas las velocidades.

---

## 6. No verificado y limitaciones

- **L del rinoceronte y del hipopótamo:**
  - No hay medidas publicadas de la altura de la cadera del rinoceronte.
  - La del hipopótamo (~1.2–1.3 m) es aproximada, de solo 2 animales.
  - Mis L esqueléticas suponen k = 0.87·HLsum, sin datos angulares que lo respalden.
- **Ángulos articulares** de rinoceronte e hipopótamo: no existen estudios cinemáticos con ángulos.
- **Glenoides–acetábulo, anchura de vía y profundidad del tronco:** no los mide ninguna fuente para estas especies. Son derivaciones con supuestos explícitos: T+L+S × 0.9–1.0; acetábulos + una cabeza femoral; costilla más larga como proxy de la profundidad.
- **Reparto de peso del hipopótamo:** no hay ninguna medida cinética.
- **Área del pie:**
  - En el elefante sale de la circunferencia, con un círculo como cota superior; el pie posterior es ovalado.
  - En el rinoceronte no separé anterior de posterior, y las masas eran estimadas.
  - En el hipopótamo no hay dato; las cifras de Michilsens et al. 2009 no las leí.
- **Presiones pico del elefante:** Panagiotopoulou 2016 se contradice (Tabla 1 frente al texto), y su Fr parece calculado con la altura a la cruz.
- **Masa de las patas:** extrapolo una regresión ajustada hasta ~450 kg. Ninguna fuente publicada da la masa de las patas de los tres.
- **Leídos solo como resumen o cita secundaria:** Coombs 1978, Alexander et al. 1979 (alometría y tensiones), Alexander & Jayes 1983, Alexander 1976, Christiansen & Paul 2001, Fisher et al. 2010, Michilsens et al. 2009, Owen-Smith 1988, Dinerstein 2011 y Nowak 1999.
- **Pienaar et al. 1966:** solo pude leer las pp. 1–5 y 16–24; las alturas a la cruz de los hipopótamos sacrificados, si existen, no estaban en esas páginas.
- **Corrección a la petición:** Regnault et al. 2013 (*J Zoo Wildl Med* 44:918) trata de osteopatología del pie de rinoceronte, no de postura. Los trabajos de forma ósea de rinocerontes son Mallet et al. 2019 (*PeerJ*) y 2020 (*J Anat*).
- **Hutchinson 2006, Ren 2008 y Panagiotopoulou 2012** los leí vía HTML, solo los primeros ~100 000 caracteres; no leí el PDF.

## Referencias principales (nuevas respecto a `cuadrupedo_fuentes.md`)

- Alexander RMcN, Pond CM (1992). Locomotion and bone strength of the white rhinoceros, *Ceratotherium simum*. *J Zool* 227:63–69. DOI [10.1111/j.1469-7998.1992.tb04344.x](https://doi.org/10.1111/j.1469-7998.1992.tb04344.x). Leído en el escaneo del Rhino Resource Center.
- Belyaev RI et al. (2025). Comparative study of the body proportions in Elephantidae and other large herbivorous mammals. *J Anat* 246:63–85. DOI [10.1111/joa.14143](https://doi.org/10.1111/joa.14143), PMC11684385; Tabla S1 (xlsx).
- Coughlin BL, Fish FE (2009). *J Mammal* 90:675–679. DOI [10.1644/08-MAMM-A-279R.1](https://doi.org/10.1644/08-MAMM-A-279R.1).
- Etienne C, Houssaye A, Hutchinson JR (2021). *PeerJ* 9:e11314. DOI [10.7717/peerj.11314](https://doi.org/10.7717/peerj.11314).
- Etienne C, Houssaye A, Fagan MJ, Hutchinson JR (2024). *J Anat*. DOI [10.1111/joa.14041](https://doi.org/10.1111/joa.14041), PMC11259748.
- Hutchinson JR, Pringle EV (2024). Footfall patterns and stride parameters of Common hippopotamus on land. *PeerJ* 12:e17675. DOI [10.7717/peerj.17675](https://doi.org/10.7717/peerj.17675).
- Hutchinson JR et al. (2006). *J Exp Biol* 209:3812–3827. DOI [10.1242/jeb.02443](https://doi.org/10.1242/jeb.02443).
- Kilbourne BM, Hoffman LC (2013). *PLoS ONE* 8:e78392. DOI [10.1371/journal.pone.0078392](https://doi.org/10.1371/journal.pone.0078392).
- Larramendi A (2016). *Acta Palaeontol Pol* 61:537–574. DOI [10.4202/app.00136.2014](https://doi.org/10.4202/app.00136.2014).
- Mallet C, Cornette R, Billet G, Houssaye A (2019). *PeerJ* 7:e7647. DOI [10.7717/peerj.7647](https://doi.org/10.7717/peerj.7647).
- Miller CE et al. (2008). *J R Soc Interface* 5:465. DOI [10.1098/rsif.2007.1220](https://doi.org/10.1098/rsif.2007.1220).
- Panagiotopoulou O, Pataky TC, Hill Z, Hutchinson JR (2012). *J Exp Biol* 215:1584. DOI [10.1242/jeb.065862](https://doi.org/10.1242/jeb.065862).
- Panagiotopoulou O et al. (2016). *R Soc Open Sci* 3:160203. DOI [10.1098/rsos.160203](https://doi.org/10.1098/rsos.160203).
- Panagiotopoulou O, Pataky TC, Hutchinson JR (2019). *PeerJ* 7:e6881. DOI [10.7717/peerj.6881](https://doi.org/10.7717/peerj.6881). Datos crudos: [10.6084/m9.figshare.7608797](https://doi.org/10.6084/m9.figshare.7608797).
- Pienaar U de V, Van Wyk P, Fairall N (1966). *Koedoe* 9:1–33. DOI [10.4102/koedoe.v9i1.778](https://doi.org/10.4102/koedoe.v9i1.778).
- Ren L et al. (2008). *J Exp Biol* 211:2735. DOI [10.1242/jeb.018820](https://doi.org/10.1242/jeb.018820).
- Usherwood JR, Self Davies ZT (2017). *eLife* 6:e29495, Tabla 1. DOI [10.7554/eLife.29495](https://doi.org/10.7554/eLife.29495).
- Warner SE et al. (2013). *PLoS ONE* 8:e54784. DOI [10.1371/journal.pone.0054784](https://doi.org/10.1371/journal.pone.0054784).
