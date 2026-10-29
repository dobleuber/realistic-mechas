# Verificación de fuentes del documento «Mechas, Ley Cuadrado-Cúbica y Giroides»

Revisión hecha el 29 de octubre de 2026. Cada afirmación del documento original
(`docs/documento_original.txt`) se contrastó con fuentes primarias siempre que
fue posible: artículos, normas y fichas técnicas. Las notas de investigación
completas, con citas textuales, están en `docs/investigacion/` (en inglés).

**Veredictos:**

- ✅ **Confirmado**: las fuentes lo respaldan.
- 🟡 **Parcial**: hay algo de verdad, pero exagerado, incompleto o mal atribuido.
- ❌ **Contradicho**: las fuentes dicen otra cosa.
- ❔ **No verificable**: no encontramos fuente.

Algunas webs (MDPI, ScienceDirect, Wiley, ASME) bloquearon el acceso
automático. En esos casos usamos copias abiertas: PubMed Central, Europe PMC y
repositorios universitarios. Lo que no se pudo leer de primera mano está
marcado.

---

## Sección 2: Ley cuadrado-cúbica

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| Galileo la formuló en 1638 (*Dos nuevas ciencias*) | ✅ | *Discorsi… intorno a due nuove scienze*, Leiden 1638 ([arXiv physics/0110031](https://arxiv.org/pdf/physics/0110031)) |
| La tensión por peso propio crece ∝ L | ✅ | Es geometría pura. Nuestra simulación lo reproduce: la presión del pie crece ∝ H a densidad constante. |
| Los animales grandes solo pueden engrosar los huesos («la naturaleza no puede hackear la ley») | 🟡 | Biewener ([*Science* 1989](https://doi.org/10.1126/science.2740914); [*JEB* 2005](https://doi.org/10.1242/jeb.01520)): entre 0.04 y 300 kg, los mamíferos mantienen la tensión ósea **constante** cambiando la **postura** (más erguida, mayor ventaja mecánica ∝ peso^0.25), no el grosor del hueso. Solo por encima de ~300 kg aparece la alometría esquelética y baja la agilidad. |
| La inercia rotacional escala ∝ L⁵ | ✅ | Identidad geométrica (I ∝ m·L²). |
| El par necesario escala ∝ L⁵ (misma aceleración angular) | 🟡 | Solo si se exige la misma aceleración angular, que no es la escala natural. Con **similitud dinámica** (mismo número de Froude) el par escala ∝ m·L ∝ **L⁴** ([Oke et al. 2026, arXiv:2603.22560](https://arxiv.org/abs/2603.22560), simulaciones en Drake: L^3.90–4.07). **Nuestra simulación MuJoCo lo confirma:** par/(peso·altura) = 0.126–0.127 de 1.75 m a 28 m. |
| El par disponible de los actuadores escala entre L² y L³ | 🟡 / ❌ | La **fuerza** hidráulica a presión fija escala ∝ L², pero el **par** (fuerza × brazo) ∝ L³. Los motores eléctricos escalan L³–L⁴ empíricamente (Dermitzakis 2011; Waldron & Hubert 2000; Seok 2015). El déficit real es ~L⁰–L¹, no L²–L³. Además es una ley de **potencia**, no «exponencial». |
| No existen robots humanoides ágiles del tamaño de edificios | ✅ | El mayor robot que camina es Tradinno (cuadrúpedo, 11 t, 8.2 m de alto; Guinness, abril 2026). LW Mononofu (8.5 m, 7.3 t) **rueda** sobre ruedas. Gundam Yokohama (18 m, 25 t) **cuelga** de una estructura y no carga peso en las piernas. Ningún bípedo de más de ~1.5 t ha caminado libre y sin cable. |

## Sección 3: Giroide y TPMS

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| Alan Schoen descubrió el giroide en la NASA (1970) | ✅ | [NASA TN D-5541](https://ntrs.nasa.gov/citations/19700020472), mayo de 1970 |
| Curvatura media cero, dos laberintos entrelazados | ✅ | Matiz: el giroide impreso es una lámina engrosada o una red, construida con una aproximación trigonométrica; sus paredes ya no tienen curvatura media cero. |
| Rigidez «marcadamente isotrópica» | 🟡 | Cierto para el giroide tipo **lámina**: nuestro FEA da razón de Zener 1.08–1.14 ([Li 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6650998)). El giroide tipo **red** es claramente anisótropo: nuestro FEA da E[111]/E[100] = 1.8–2.2 (Zener 1.9–2.3) a densidades de 0.1–0.2. |
| Estudio del MIT (2017): 5 % de la densidad del acero y 10 veces su resistencia | 🟡 | Las cifras están en el artículo ([Qin et al., *Sci. Adv.* 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5218516)) y en la [nota de prensa](https://news.mit.edu/2017/3-d-graphene-strongest-lightest-materials-0106). Pero salen de una **simulación** de dinámica molecular de un ensamblaje desordenado de grafeno, no de un bloque giroide medido. Se compara la resistencia a tracción **absoluta**, y su módulo (2.8 GPa) es ~1.4 % del del acero. |
| Fusionaron grafeno con calor y presión y lo ensayaron destructivamente | ❌ | El ciclo de calor y presión fue **simulado**. Lo único ensayado físicamente fueron giroides de **polímero** impresos en 3D (VeroMagenta), ~10⁷ veces más grandes. |
| Buehler: «la geometría es el factor dominante» | ✅ | Cita textual en MIT News. |
| Por tanto, un giroide de metal o polímero mejora drásticamente la resistencia por peso sin perder módulo | ❌ | El propio artículo concluye que sus propiedades «disminuyen con la densidad mucho más rápido que las de espumas poliméricas» (E ∝ ρ^2.73, resistencia ∝ ρ^2.0–3.0). |

## Sección 4: Leyes de Gibson-Ashby

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| E/Es = C₁(ρ/ρs)^m y σ/σs = C₂(ρ/ρs)^n | ✅ | Marco clásico (Gibson & Ashby, *Cellular Solids*). |
| Para giroide m ≈ 2.0, n ≈ 1.5, C₁ ≈ 1.11, C₂ ≈ 0.197 | 🟡 | Los exponentes publicados para giroides son m ≈ 1.1–1.6 (lámina) y 1.7–2.4 (red); n ≈ 1.3–2.0. Para Ti-6Al-4V LPBF lámina: C₁ = 0.9, m = 1.58, C₂ = 0.536, n = 1.45 ([Naghavi et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9598079/)). Nuestro FEA da E\*/Es = 0.069 a ρ = 0.2, frente a 0.071 de esa ley. |
| A densidad 20 % la resistencia queda en «8.9 % (0.2^1.5)» | ❌ (incoherencia interna) | El documento usa C₂ ≈ 0.197 en su tabla pero lo omite en el cálculo: con su propia constante da **1.8 %**. Con datos reales de Ti-6Al-4V lámina: **5.2 %**. El 8.9 % corresponde a C₂ = 1, el extremo más optimista. |
| Bajar la masa un 80 % «anula en gran medida» los problemas de la ley cuadrado-cúbica | ❌ | Lo que importa en un miembro cargado por su peso es la resistencia **específica** (resistencia/densidad). En todas las fuentes, la del giroide es el **6–45 %** de la del sólido. La teoría impone σ\*/σs ≤ ρ\*/ρs ([Wang et al., *PNAS* 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9407660)). Para cargas límite «no hay beneficio» ([Evans, Hutchinson & Ashby 1998](https://groups.seas.harvard.edu/hutchinson/papers/473.pdf)). **Nuestro modelo de escalado:** las piernas rellenas de giroide alcanzan solo el ~60 % de la altura máxima de un tubo de pared delgada. |
| El giroide no tiene concentradores de tensión | 🟡 | Los suaviza respecto a enrejados de barras, pero no los elimina. Nuestro FEA: con giroide lámina al 20 %, el 1 % más cargado del material soporta **~15 veces** la tensión macroscópica (~3 veces más que la media). Los defectos internos y la rugosidad inician grietas (Kelly 2019). |

## Sección 5: Fibra de carbono

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| PLA+CF: módulo de 0.09 a 0.47 GPa; resistencia pico 2.98–13.89 MPa; la CF reduce la resistencia del giroide, más a densidad alta | 🟡 | Las cifras son correctas ([Saleh et al., *Polymers* 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9654767/)). Pero los rangos abarcan **todas** las probetas (ambos materiales, tres topologías, tres tamaños de celda), no una topología como sugiere la Tabla 2. El mecanismo de «microhuecos» **no aparece** en el artículo: este lo atribuye a paredes más gruesas con más fibra, y las grietas empiezan entre capas. |
| La fibra de carbono continua no puede seguir la geometría del giroide | ❌ | Ya se han impreso giroides y diamantes con fibra continua: +81 % de módulo específico ([Szederkényi et al., ECCM21 2024](https://real.mtak.hu/206352/1/1843_open_ECCM21_Proceeding_CFRP_TPMS_crush.pdf)). La debilidad entre capas (eje Z) sí se confirma. |
| Por tanto, el CFRP queda descartado para el esqueleto | 🟡 | Vale solo para CFRP **impreso** en forma de giroide. Un tubo de CFRP laminado o enrollado (lo estándar en aeronáutica) da en nuestro modelo la **mayor** altura de todos los materiales (~33 m frente a 29 m del Ti-6Al-4V). |

## Sección 6: Titanio Ti-6Al-4V

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| Densidad 4.4 g/cm³, E ≈ 110 GPa, resistencia > 1000 MPa | ✅ | Recocido: 4.43 g/cm³, 113.8 GPa, fluencia 880 / rotura 950 MPa. Más de 1000 MPa solo tal como sale de LPBF o envejecido. |
| LPBF da propiedades «casi 100 % isótropas» | ❌ | Tal como sale de la impresora es **anisótropo**: fluencia 761 frente a 820 MPa según la orientación de impresión ([Jamshidi 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7345457)). Solo tras **HIP** es «consistente e isótropo» ([Mahmud 2021, INL](https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_63131.pdf)). |
| El giroide de Ti supera a todos los metales celulares | ❌ | Los TPMS de lámina superan a los enrejados de barras, pero el **diamante** de lámina suele ganar al giroide (Al-Ketan 2018; Zhang 2018). La comparación con superaleaciones de magnesio ❔ no tiene fuente. |
| «Bisagras plásticas» con deformación «puramente elástica» | ❌ | El pasaje viene de Ataee 2018, que ensayó **Ti comercialmente puro**, no Ti-6Al-4V. Las bisagras plásticas son, por definición, deformación **plástica**. |
| Resistencia a fatiga | 🟡 | El giroide lámina es el mejor enrejado a fatiga (≈45–50 % de su fluencia en compresión), pero sigue siendo una gran reducción. Los enrejados de barras quedan por debajo de 0.2 (Yavari 2013). El Ti-6Al-4V sólido sin mecanizar baja a ~210–300 MPa por la rugosidad superficial. |

## Sección 7: Actuación, marcha y calor

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| La fuerza de reacción del suelo llega a 2–3 veces el peso «al trotar o caminar» | 🟡 | Caminando: **1.0–1.5** veces el peso ([Nilsson & Thorstensson 1989](https://pubmed.ncbi.nlm.nih.gov/2782094/)). Corriendo: 2.0–2.9. **Nuestra simulación:** 1.35 veces el peso a todas las escalas. |
| La fuente citada [1] (MDPI, robot bípedo hidráulico) respalda un «macroanálisis estadístico empírico» | ❌ | El artículo ([copia Essex](https://repository.essex.ac.uk/38034/1/Biped%20Robot.pdf)) solo dice, sin cita, «unas tres veces el peso» para caminar y correr. Es un cálculo estático de un robot de 27 kg; no mide fuerzas. |
| El MIT Cheetah 3 «vectoriza su columna elástica» | ❌ | El Cheetah 3 tiene tronco rígido: su controlador usa un modelo de un solo cuerpo rígido. La columna flexible era del MIT Cheetah I y del Cheetah de Boston Dynamics. |
| Los motores eléctricos quedan descartados a gran escala | 🟡 | El Gundam de 18 m usa solo actuadores **eléctricos** (aunque no carga peso en las piernas). Hidráulica o EHA son lo razonable para fuerzas grandes, pero no es algo absoluto. |
| Hidráulica con servoválvulas: eficiencia < 30 % | ✅ | Media del 22 %; 14 % en maquinaria móvil ([ORNL/TM-2011/14](https://info.ornl.gov/sites/publications/files/pub28014.pdf)). |
| EHA: eficiencia neta > 70 % | 🟡 | Picos del 70–87 % (Du et al. 2024); la mayoría de puntos de operación están entre el **30 y el 60 %** (Du et al. 2026). |
| El giroide como intercambiador: número de Nusselt alto | 🟡 | Confirmado: 8–10 veces el de un haz de barras ([Prussack 2024](https://www.osti.gov/biblio/2396699)). Pero el factor de fricción es ~90 veces mayor, y el documento omite ese coste de bombeo. El diamante o Schwarz-D suelen ser iguales o mejores. Además, el giroide **no** es un fractal. |

## Sección 8: Suelo

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| Capacidades portantes 95 / 144–239 / 287 / 574 kPa | 🟡 | Coinciden con la tabla del código residencial **CABO 1995** (2000 / 3000 / 5000 / 6000 / 12000 psf), vía la respuesta de Worldbuilding SE citada ([tabla CABO](https://openlab.citytech.cuny.edu/bt2-2020f/files/2020/03/Foundation-CalculationsS.pdf)). Son **valores admisibles de diseño** para casas, con factor de seguridad ~3 (2–4 según [USACE EM 1110-1-1905](https://www.tensarinternational.com/resources/articles/bearing-capacity-of-soil)), pensados para limitar asentamientos. **No** son el límite de rotura. Las etiquetas de suelo del documento tampoco coinciden con las clases del código. |
| 574 kPa es la «resistencia máxima del granito puro» | ❌ | El granito intacto resiste más de 100–250 MPa ([Marinos & Hoek 2000](https://www.rocscience.com/assets/resources/learning/hoek/GSI-A-Geologically-Friendly-Tool-for-Rock-Mass-Strength-Estimation-2000.pdf)). El código de [Nueva York 2022](https://www.nyc.gov/assets/buildings/codes-pdf/cons_codes_2022/2022BC_Chapter18_SoilsFoundationsWBwm.pdf) admite **5746 kPa** sobre roca dura sana; [Hong Kong GEO TGN 53](https://www.cedd.gov.hk/filemanager/eng/content_427/TGN%2053_Issue%202.pdf), hasta **12 500 kPa**. |
| El mecha «rompería la corteza» o perforaría la roca | ❌ | Un mecha de 50 m con densidad humana ejerce ~1 MPa bajo el pie: menos del 1 % de la resistencia del granito. Nuestra simulación sobre granito: camina sin hundirse. |
| La capacidad portante es un límite «absoluto» independiente del pie | 🟡 | En **arcilla** saturada (carga rápida) sí: q_ult ≈ 5.14·c_u, independiente del tamaño. En **arena y grava**, la capacidad crece con el ancho del pie (término ½·γ·B·N_γ de Terzaghi), y el documento lo ignora. Con pies proporcionales, presión y capacidad crecen igual. |
| Bagger 293: 96 m, 14 200 t | ✅ | [Vulović et al., *Metals* 2023](https://www.mdpi.com/2075-4701/13/3/466); 12 orugas ([de.wikipedia](https://de.wikipedia.org/wiki/Bagger_293)). Las excavadoras de su clase trabajan a **~170 kPa**, por encima de los valores de código para arena y grava, lo que confirma que esos valores no son límites de rotura. |
| Los pies tendrían que ser «del tamaño de estadios de fútbol» | ❌ | No aparece en la fuente citada. La respuesta de Worldbuilding SE (mecha de 70 t) pide pies ~90 % más largos y anchos para caminar sobre arcilla. Incluso un mecha de 14 200 t necesitaría ~3600 m² por pie (≈60 × 60 m), unas 10 veces menos que un estadio. |
| Fragata ≈ masa de referencia | ✅ | 4000–7500 t (FREMM ~6700 t; Constellation 7291 t). |

## Sección 9: Conclusiones del documento

| Conclusión | Veredicto | Qué dicen las fuentes y la simulación |
|---|---|---|
| El giroide es «la solución definitiva» contra la ley cuadrado-cúbica | ❌ | Las piernas rellenas de giroide son la opción **más pesada** de las que evaluamos: alcanzan el ~60 % de la altura de un tubo de pared delgada. El giroide sí sirve como **núcleo** de paredes delgadas, contra el pandeo local. |
| Solo el titanio LPBF es viable | 🟡 | Ti-6Al-4V con HIP es excelente, pero un tubo de CFRP laminado da algo más de altura y el acero 4340 queda cerca (25 m frente a 29 m). |
| Con EHA el problema de potencia queda resuelto | ❌ | Actuadores y energía son justamente lo que hace **divergir** la masa (≈30 m en el escenario base). La estructura no es el factor limitante. |
| El suelo es «el juez final» | 🟡 | En arcilla blanda, sí: un mecha de 20 m con densidad humana se hunde y cae en nuestra simulación. En arena densa, roca o pavimento, **no**: el límite lo pone antes la masa del propio mecha (actuadores y energía). |
| Rango viable de 15–20 m | 🟡 | El orden de magnitud coincide de forma razonable con nuestro escenario base (18 m con giroide, 29 m con tubo), pero por **otras razones**. Con supuestos optimistas se llega a ~80 m; con supuestos de la robótica actual, a ~5–6 m, que es lo que se ha construido de verdad. |
| Un mecha de 50 m hundiría los pies «en el pavimento y la roca viva» | ❌ | Roca y pavimento lo aguantan (~1 MPa frente a varios MPa admisibles). Se hundiría en arcilla (18–45 m de hundimiento de equilibrio según nuestro cálculo). |
