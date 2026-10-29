# Mechas, ley cuadrado-cúbica y giroides: versión revisada y validada

Revisión del 29 de octubre de 2026 del documento original, que se conserva sin cambios en la pestaña «Original». Cada afirmación se contrastó con fuentes primarias y los cálculos se comprobaron con simulaciones. El código, los datos, las figuras y los vídeos están en [github.com/dobleuber/realistic-mechas](https://github.com/dobleuber/realistic-mechas).


## Resumen

**Un mecha bípedo que camina puede medir unos 30 m con los materiales y actuadores actuales, en un escenario base realista.** Con supuestos optimistas el límite sube a unos 80 m; con los supuestos de la robótica actual baja a unos 6 m, que es el tamaño de lo que se ha construido. El límite no lo pone la estructura sino la masa de los actuadores y del sistema de energía, que crece más rápido que el propio mecha hasta que la masa deja de converger.

El documento original acierta en que hoy no existe ningún humanoide gigante que camine, en que la hidráulica controlada por válvulas es ineficiente y en que el suelo blando es un problema serio. Sus dos tesis centrales no se sostienen. El giroide no compensa la ley cuadrado-cúbica: rellenar las piernas de giroide reduce la altura máxima de 29 m a 18 m. Y el suelo no es un límite universal: un mecha de 50 m camina sobre arena densa, arcilla dura o roca, aunque se hunde en arcilla blanda.

Correcciones principales respecto al original:

- Con un movimiento dinámicamente similar (mismo número de Froude), el par necesario crece con L⁴, no con L⁵. El déficit frente al par de los actuadores crece como mucho con L¹: es una ley de potencia, no un crecimiento exponencial.
- El estudio del MIT de 2017 simuló grafeno por dinámica molecular; lo que se ensayó físicamente fueron giroides de polímero impresos. El propio artículo concluye que sus propiedades caen con la densidad más rápido que las de una espuma.
- Con una densidad relativa del 20 %, un giroide de Ti-6Al-4V conserva un 5 % de la resistencia del material macizo. El original dice 8.9 %, y con la constante de su propia tabla serían 1.8 %. La resistencia por kilo de un giroide es siempre menor que la del macizo.
- Al caminar, la fuerza del suelo es de 1.0 a 1.5 veces el peso. Las 2 a 3 veces del original corresponden a correr.
- Los valores de 95 a 574 kPa son capacidades admisibles de un código residencial de 1995, con un factor de seguridad de unas 3 veces, no la resistencia del terreno. El granito intacto resiste más de 100 MPa.
- Los actuadores electrohidrostáticos (EHA) llegan al 70–87 % de eficiencia en su mejor punto, pero en un ciclo de trabajo real están entre el 30 y el 60 %.

## La ley cuadrado-cúbica en máquinas que caminan

Si todas las dimensiones de un cuerpo se multiplican por k, las áreas crecen con k² y el volumen y la masa con k³ (Galileo, Dos nuevas ciencias, 1638). La tensión que produce el peso propio en una sección crece por tanto con k: a densidad constante, cualquier estructura acaba fallando bajo su propio peso si se agranda lo suficiente.

Para el movimiento hay que decidir también cómo escala el tiempo. Exigir a un gigante la misma aceleración angular que a una persona, como hace el original, lleva a un par que crece con k⁵. Ni los animales ni las máquinas grandes se mueven así. Lo natural es la similitud dinámica, con el mismo número de Froude (v²/gL), en la que los tiempos crecen con √k; entonces el par necesario crece con m·L, es decir con k⁴ ([Oke et al. 2026](https://arxiv.org/abs/2603.22560)). Nuestra simulación lo confirma: el par pico de rodilla dividido entre peso × altura vale 0.126 tanto a 1.75 m como a 28 m.

Un cilindro hidráulico a presión fija da una fuerza proporcional a su área (k²) y un par proporcional a fuerza por brazo de palanca (k³). Los motores eléctricos escalan de forma empírica entre k³ y k⁴. El déficit entre par necesario y par disponible crece entonces entre k⁰ y k¹: existe, pero es mucho menor que el que plantea el original.

Los animales grandes no compensan la ley solo con huesos más gruesos. Entre 0.04 y 300 kg mantienen constante la tensión en los huesos cambiando de postura: caminan más erguidos y alinean las patas con la fuerza del suelo ([Biewener, Science 1989](https://doi.org/10.1126/science.2740914)). Por encima de unos 300 kg aparecen huesos proporcionalmente más gruesos y menos agilidad; los saurópodos de 50 a 80 t caminaban a menos de 2 m/s.


### Lo que se ha construido

Ningún bípedo de más de unas 1.5 t ha caminado libre y sin cable. El mayor robot que camina es Tradinno, un dragón cuadrúpedo de 11 t y 8.2 m de alto. LW Mononofu (8.5 m, 7.3 t) se desplaza sobre ruedas, y el Gundam de Yokohama (18 m, 25 t) cuelga de una estructura de soporte, no carga peso en las piernas y usa solo actuadores eléctricos. Las masas de estas máquinas caen entre nuestros escenarios base y pesimista.


![masa_vs_altura.png](../results/figures/masa_vs_altura.png)


## El giroide: qué es y qué puede hacer

El giroide es una superficie mínima triplemente periódica que Alan Schoen describió en la NASA en 1970 ([NASA TN D-5541](https://ntrs.nasa.gov/citations/19700020472)). En fabricación aditiva se usa de dos formas: como una lámina engrosada sobre la superficie (giroide lámina) o rellenando uno de los dos laberintos que la superficie separa (giroide red). Se comportan como materiales distintos.


### El estudio del MIT de 2017

[Qin et al. (Science Advances, 2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5218516) obtuvieron por dinámica molecular que un ensamblaje desordenado de grafeno con el 4.6 % de la densidad del acero tenía una resistencia a tracción 10 veces mayor. La compactación con calor y presión fue simulada, y los únicos ensayos físicos se hicieron con giroides de polímero impresos en 3D, unas 10⁷ veces más grandes. Su módulo simulado, 2.8 GPa, es alrededor del 1.4 % del del acero. Buehler sí dijo que «la geometría es el factor dominante», pero el artículo concluye también que las propiedades «disminuyen con la densidad mucho más rápido que las de las espumas poliméricas»: el módulo cae con ρ^2.7 y la resistencia con ρ^2.0 a ρ^3.0.


### Leyes de Gibson-Ashby con datos reales

Las propiedades de un sólido celular dependen de su densidad relativa ρ = ρ*/ρs según E*/Es = C₁·ρ^m y σ*/σs = C₂·ρ^n. La tabla compara las constantes del original con ensayos publicados y con nuestro análisis por elementos finitos, todos a ρ = 0.2.


| Fuente | E*/Es | σ*/σs | Resistencia por kilo frente al macizo |
|---|---|---|---|
| Original, tabla (C₁ = 1.11, m = 2; C₂ = 0.197, n = 1.5) | 4.4 % | 1.8 % | 9 % |
| Original, cálculo del texto (0.2^1.5) | – | 8.9 % | 45 % |
| Ti-6Al-4V, giroide lámina (Naghavi et al. 2022) | 7.1 % | 5.2 % | 26 % |
| Acero maraging, giroide red (Al-Ketan et al. 2018) | 0.9 % | 6.0 % | 30 % |
| Nuestro FEA, giroide lámina | 6.9 % | 6.7 % (inicio de fluencia) | 34 % |
| Nuestro FEA, giroide red | 2.9 % | 2.8 % (inicio de fluencia) | 14 % |

En todos los casos la resistencia por kilo es menor que la del material macizo, y la teoría impide superarla: en cualquier material poroso σ*/σs ≤ ρ (cota de Voigt, [Wang et al., PNAS 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9407660)). Para un miembro que soporta su propio peso, lo que cuenta es justamente esa resistencia por kilo, así que una pierna rellena de giroide aguanta menos altura, no más. [Evans, Hutchinson y Ashby (1998)](https://groups.seas.harvard.edu/hutchinson/papers/473.pdf) lo resumen: los metales celulares no aportan ventaja en diseños gobernados por la carga límite.

Nuestro análisis por elementos finitos (homogenización periódica por vóxeles, con la malla convergida al 1 %) muestra además que el giroide lámina es casi isótropo (razón de Zener de 1.08 a 1.14) y el giroide red no lo es (de 1.3 a 2.3). La geometría suave tampoco elimina las concentraciones de tensión: a una densidad del 20 %, el 1 % más cargado del material soporta unas 15 veces la tensión aplicada.

El giroide sí es útil como núcleo de paredes delgadas, donde impide el pandeo local; para absorber impactos, gracias a su meseta de deformación larga; y como intercambiador de calor.


![giroide_fea.png](../results/figures/giroide_fea.png)


## Materiales

La fibra de carbono impresa en forma de giroide tiene los problemas que describe el original. [Saleh et al. (Polymers, 2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9654767/) midieron que la fibra corta reduce la resistencia pico de los giroides de PLA, y las piezas con fibra continua se delaminan entre capas. Aun así, ya se han impreso giroides con fibra continua (Szederkényi et al. 2024), y un tubo de CFRP laminado, que es lo habitual en aeronáutica, no tiene esos problemas.

El Ti-6Al-4V fundido por láser es anisótropo tal como sale de la impresora (fluencia de 761 a 820 MPa según la orientación) y su resistencia a fatiga baja a 210–300 MPa por la rugosidad superficial. Tras un prensado isostático en caliente (HIP) es isótropo, con una fluencia de 928 MPa y una fatiga de unos 450 MPa ([Mahmud et al. 2021](https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_63131.pdf)). El pasaje del original sobre las «bisagras plásticas» procede de un estudio con titanio comercialmente puro (Ataee et al. 2018), y una bisagra plástica es deformación plástica, no elástica. Entre las estructuras de lámina, el diamante suele superar al giroide.

Con el modelo de dimensionado (tubo de pared delgada, escenario base), la altura máxima por material es de 33 m para el CFRP laminado, 29 m para el Ti-6Al-4V con HIP, 25 m para el acero 4340, 23 m para el aluminio 7075-T6 y 22 m para el Ti-6Al-4V sin HIP. El material importa, pero menos que la arquitectura de la pieza.


## Actuación, energía y calor

La hidráulica controlada por válvulas tiene una eficiencia media del 22 %, y del 14 % en maquinaria móvil ([ORNL/TM-2011/14](https://info.ornl.gov/sites/publications/files/pub28014.pdf)). Los EHA llegan al 70–87 % en su mejor punto, pero la mayoría de los puntos de un ciclo real de robot están entre el 30 y el 60 % (Du et al. 2024 y 2026). Los robots hidráulicos trabajan a 16–21 MPa (Atlas, HyQ).

El problema de escala de los actuadores no es su fuerza sino su masa. La masa de un cilindro es proporcional al trabajo de su carrera (fuerza por carrera), que crece con k⁴: un gato industrial de 700 bar pesa de 0.24 a 0.34 kg por kJ, y un actuador de robótica de 2 a 3 kg por kJ. La potencia de la marcha crece con k^3.5, y un grupo diésel con su bomba rinde de 0.10 a 0.15 kW/kg. Ambas fracciones de masa crecen con la altura: en el escenario base, los actuadores de las piernas y el sistema de energía suman el 32 % de la masa a 20 m y el 42 % a 28 m.

Como intercambiador de calor, el giroide sí da números de Nusselt altos, de 8 a 10 veces los de un haz de barras ([Prussack et al. 2024](https://www.osti.gov/biblio/2396699)), pero con un factor de fricción unas 90 veces mayor, que se paga en potencia de bombeo de un aceite viscoso. El diamante o el Schwarz-D suelen ser iguales o mejores. Tampoco es un fractal.


![desglose_masa.png](../results/figures/desglose_masa.png)


## El suelo

Los valores del original (95, 144, 239, 287 y 574 kPa) coinciden con la tabla del código residencial estadounidense CABO de 1995. Son capacidades admisibles de diseño para viviendas, con un factor de seguridad de unas 3 veces y pensadas para limitar asentamientos, no el punto de rotura. El granito intacto resiste más de 100 a 250 MPa, el [código de Nueva York](https://www.nyc.gov/assets/buildings/codes-pdf/cons_codes_2022/2022BC_Chapter18_SoilsFoundationsWBwm.pdf) admite 5.7 MPa sobre roca sana y el de Hong Kong hasta 12.5 MPa. Las excavadoras de la clase de la Bagger 288 trabajan a unos 170 kPa, por encima del valor de código para arena y grava.

La capacidad portante última depende del tipo de suelo (Terzaghi, con los factores de Vesić). En arcilla saturada cargada con rapidez vale unas 5.14 veces su resistencia al corte y no depende del tamaño del pie, así que un mecha más grande acaba superándola. En arena y grava crece con el ancho del pie: si el pie crece en proporción, la presión y la capacidad crecen igual.

La tabla aplica esto a un mecha con la densidad de un cuerpo humano (13 kg/m³ × H³) y pies de proporciones humanas, apoyado en un solo pie con 1.3 veces su peso, y lo compara con la simulación con suelo deformable.


| Suelo | Mecha de 20 m (104 t), 398 kPa | Mecha de 50 m (1630 t), 996 kPa |
|---|---|---|
| Arcilla blanda (cu = 25 kPa) | Capacidad 138 kPa. Simulación: se hunde 1.4 m y cae | Capacidad 138 kPa. Simulación: se hunde 10.5 m y cae |
| Arcilla firme (cu = 75 kPa) | Capacidad 413 kPa. Simulación: camina | Capacidad 413 kPa. Hundimiento calculado de unos 19 m |
| Arcilla dura (cu = 150 kPa) | Capacidad 825 kPa | Capacidad 825 kPa. Simulación: camina |
| Arena densa | Capacidad 697 kPa. Simulación: camina | Capacidad 1743 kPa. Simulación: camina |
| Granito sano | Más de 17 MPa | Más de 17 MPa. Simulación: camina |

El original acierta en que un mecha gigante se hundiría en suelos blandos, pero no en que «rompería la corteza» ni en que hundiría los pies en el pavimento o la roca. Tampoco aparece en la fuente citada que los pies tendrían que ser «del tamaño de estadios»: incluso para 14 200 t harían falta unos 3600 m² por pie sobre arena, unos 60 por 60 m.


![presion_suelo.png](../results/figures/presion_suelo.png)


## Simulaciones

Para comprobar el análisis se construyeron tres herramientas, todas disponibles en el repositorio:

- **Elementos finitos de celdas giroides.** Homogenización periódica por vóxeles para obtener la rigidez, la anisotropía y la concentración de tensiones de giroides lámina y red entre el 10 y el 50 % de densidad.
- **Modelo de dimensionado del mecha.** Para cada altura diseña las piernas (tubos con pandeo local según NASA SP-8007, o secciones rellenas de giroide según Gibson-Ashby), los cilindros hidráulicos, el grupo de potencia y el combustible, y resuelve la masa de forma autoconsistente. Si la masa no converge, esa altura no se puede construir.
- **Simulación física de la marcha** en MuJoCo, con verificación cruzada en Gazebo Harmonic. Es un bípedo con las proporciones y masas del cuerpo humano (tablas de Winter) que camina con control predictivo del punto de momento cero (Kajita et al. 2003), con el par de cada articulación limitado al de su actuador y un suelo que se hunde según su capacidad portante.

### Similitud dinámica

Escalando el tiempo con √H, el mismo plan de marcha produce los mismos pares normalizados a cualquier altura: 0.126 en la rodilla, 0.091 en el tobillo y 0.067 en la cadera, en unidades de peso por altura, con una fuerza pico sobre el suelo de 1.35 veces el peso, dentro del rango medido en personas (de 1.0 a 1.5). En unidades humanas son 2.2, 1.6 y 1.1 N·m/kg, frente a 0.9, 1.6 y 0.9 N·m/kg medidos en personas; la rodilla trabaja más porque los robots caminan con las rodillas flexionadas.


### Resultados


| Caso | MuJoCo | Gazebo |
|---|---|---|
| Persona de referencia (1.75 m, 70 kg) | Camina 1.86 m | Camina 1.86 m |
| Mecha de 20 m, diseño base (9.5 t) | Camina 21.3 m a 0.93 m/s; potencia pico 102 kW | Camina 21.3 m |
| Mecha de 28 m, diseño base (47 t) | Camina 29.8 m a 1.11 m/s; potencia pico 603 kW | Camina 29.8 m |
| 20 m con actuadores al 50–90 % del par necesario | Cae | Cae (probado al 70 %) |
| 20 m con densidad humana en arcilla blanda | Se hunde 1.4 m y cae | No simulado |
| 50 m con densidad humana en arena densa, arcilla dura o granito | Camina | No simulado |

Con actuadores por debajo del 100 % del par pico necesario el mecha cae, y con el 100 % o más camina: no hay margen para ahorrar masa en los actuadores. Como esa masa crece con k⁴, es la que fija la altura máxima.


![simulaciones.png](../results/figures/simulaciones.png)

Vídeos en el repositorio: [marcha a 20 m](https://github.com/dobleuber/realistic-mechas/blob/main/results/videos/e1_marcha_H20.mp4), [marcha a 28 m](https://github.com/dobleuber/realistic-mechas/blob/main/results/videos/e1_marcha_H28.mp4), [actuadores al 60 %](https://github.com/dobleuber/realistic-mechas/blob/main/results/videos/e2_par_60pct_H20.mp4), [20 m en arcilla blanda](https://github.com/dobleuber/realistic-mechas/blob/main/results/videos/e3_arcilla_blanda_H20.mp4), [50 m en arcilla blanda](https://github.com/dobleuber/realistic-mechas/blob/main/results/videos/e3_arcilla_blanda_H50.mp4) y [50 m en arena densa](https://github.com/dobleuber/realistic-mechas/blob/main/results/videos/e3_arena_densa_H50.mp4).


## Conclusión: cuánto puede medir un mecha

La tabla da la altura a la que la masa deja de converger para tres conceptos de pierna y tres escenarios.


| Piernas | Optimista | Base | Pesimista |
|---|---|---|---|
| Tubo de Ti-6Al-4V de pared delgada | 79 m | 29 m | 6 m |
| Tubo con núcleo de giroide | 79 m | 28 m | 6 m |
| Sección rellena de giroide (propuesta original) | 43 m | 18 m | Menos de 3 m |

Escenario optimista: actuadores de 0.24 kg/kJ, grupo de potencia de 300 W/kg, eficiencia del 60 % y márgenes de seguridad mínimos. Base: 0.5 kg/kJ, 150 W/kg, 45 % y factor de carga de diseño de 1.5. Pesimista: actuadores de la robótica actual (2 kg/kJ), 100 W/kg y 30 %.

La estimación del original, de 15 a 20 m, cae dentro de este rango, pero por razones distintas. Un mecha de unos 30 m que camine despacio, a alrededor de 1 m/s, es físicamente posible con tubos de pared delgada de titanio o fibra de carbono, actuadores hidráulicos y pies de proporciones normales sobre suelo firme. Lo que lo limita es la masa de los actuadores y de la energía, no la resistencia de la estructura ni la roca bajo sus pies. En suelos blandos necesitaría pies varias veces más grandes que los proporcionales.


![altura_maxima.png](../results/figures/altura_maxima.png)


## Limitaciones

- La marcha simulada es lenta y con los pies planos (número de Froude de alrededor de 0.01), como la de los humanoides grandes actuales. Correr multiplicaría las cargas por 2 o 3.
- El suelo deformable es un modelo cuasi-estático de punzonamiento: sirve para decidir si el mecha se hunde, no para predecir la forma de la huella.
- El análisis por elementos finitos es lineal: da el inicio de la plastificación, no la resistencia última. Para la resistencia se usan los ensayos publicados.
- No se modelan la fatiga de las uniones, el control del equilibrio ante empujones o caídas, ni la gestión térmica detallada.

## Fuentes principales

La verificación completa, afirmación por afirmación, está en [docs/verificacion_fuentes.md](https://github.com/dobleuber/realistic-mechas/blob/main/docs/verificacion_fuentes.md).

- Qin, Jung, Kang y Buehler (2017). The mechanics and design of a lightweight three-dimensional graphene assembly. Science Advances 3:e1601536. [PMC5218516](https://pmc.ncbi.nlm.nih.gov/articles/PMC5218516)
- Naghavi et al. (2022). Bioengineering 9:504. [PMC9598079](https://pmc.ncbi.nlm.nih.gov/articles/PMC9598079/)
- Al-Ketan, Rowshan y Abu Al-Rub (2018). Topology-mechanical property relationship of 3D printed strut, skeletal, and sheet based periodic metallic cellular materials. Additive Manufacturing 19:167.
- Wang et al. (2022). PNAS 119:e2119536119. [PMC9407660](https://pmc.ncbi.nlm.nih.gov/articles/PMC9407660)
- Evans, Hutchinson y Ashby (1998). Cellular metals. Current Opinion in Solid State and Materials Science 3:288.
- Saleh, Anwar, Al-Ahmari y Alfaify (2022). Compression Performance and Failure Analysis of 3D-Printed Carbon Fiber/PLA Composite TPMS Lattice Structures. Polymers 14:4595. [PMC9654767](https://pmc.ncbi.nlm.nih.gov/articles/PMC9654767/)
- Mahmud et al. (2021). Metals 11:1671. [INL](https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_63131.pdf)
- Biewener (1989). Scaling body support in mammals: limb posture and muscle mechanics. Science 245:45.
- Oke et al. (2026). Allometric Scaling Laws for Bipedal Robots. [arXiv:2603.22560](https://arxiv.org/abs/2603.22560)
- Nilsson y Thorstensson (1989). Ground reaction forces at different speeds of human walking and running. Acta Physiologica Scandinavica 136:217.
- Love, Lanke y Alles (2012). Estimating the impact of the US fluid power industry. ORNL/TM-2011/14.
- Prussack et al. (2024). Applied Thermal Engineering. [OSTI 2396699](https://www.osti.gov/biblio/2396699)
- Código de construcción de Nueva York 2022, capítulo 18; GEO TGN 53 (Hong Kong, 2026); tabla CABO 1995.
- Vulović et al. (2023). Strength analysis of eight-wheel bogie of bucket wheel excavator. Metals 13:466.
- Kajita et al. (2003). Biped walking pattern generation by using preview control of zero-moment point. ICRA.
- Winter (2009). Biomechanics and Motor Control of Human Movement, 4.ª ed. Wiley.

