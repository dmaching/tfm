# Control previo de ampliación integral

## PDF inicial

- Archivo: `latex/main.pdf`.
- Páginas totales: 59.
- Páginas útiles aproximadas: 47--50, descontando portada, índices y bibliografía.
- Fecha de compilación registrada en el PDF: 20 de agosto de 2026.

Como referencias históricas también existen `MACHIN_GONZALEZ_DANIEL_ENTREGA3.pdf` (63 páginas), `version1406.pdf` (49 páginas) y `MACHIN_GONZALEZ_DANIEL_ENTREGA1.pdf` (31 páginas). La base editable actual es la versión larga de 59 páginas.

## Estructura detectada

- Capítulos: ocho capítulos principales en el orden oficial UNIR: Introducción; Contexto y estado del arte; Objetivos concretos y metodología de trabajo; Marco normativo; Desarrollo específico de la contribución; Código fuente y datos analizados; Conclusiones; Limitaciones y prospectiva.
- Secciones principales: motivación y planteamiento; teoría de carteras, información y modelos generativos; objetivos y CRISP-DM; normativa; EDA, pipeline, datos, benchmarks, VAE, escenarios, optimización y resultados; código/datos; conclusiones; limitaciones/prospectiva.
- Se detectaron 94 encabezados entre capítulos, secciones y subsecciones contando los archivos auxiliares incluidos.

## Figuras detectadas

- Siete figuras registradas en el índice compilado: dos conceptuales en el capítulo 2 y cinco figuras EDA en el capítulo 5.
- Existen además siete figuras de evaluación VAE/escenarios y una figura de comparación de estrategias en `figures/`, todavía susceptibles de integración en la memoria larga.
- Existen siete figuras EDA reproducibles en `latex/figuras/eda/`.

## Tablas detectadas

- Una tabla registrada en el índice compilado: comparación de estrategias fuera de muestra.
- Existen CSV reales para crear tablas de estadísticos EDA, reconstrucción, calidad sintética, pesos y resultados.

## Bibliografía detectada

- Total de entradas: 18.
- Total de claves citadas en los `.tex` de partida: 10.
- Citas indefinidas: ninguna en el log disponible.
- Referencias no citadas: 8 aproximadamente (`lopez2018advances`, `jiang2017deep`, `rasekhschaffe2026`, `voronina2025genai`, `opitz2017latent`, `lopezdeprado2018chapter1`, `huang2020deep` y `machin2026repositorio`).

## Apartados débiles o incompletos

- Apartado: resumen y abstract. Problema: placeholders. Acción prevista: redactar versiones de 150--300 palabras basadas en resultados reales.
- Apartado: introducción. Problema: presenta GAN y KL como fases ejecutadas. Acción prevista: conservar motivación y corregir alcance sin acortar.
- Apartado: metodología CRISP-DM. Problema: siete TODOs y coexistencia con metodología antigua contradictoria. Acción prevista: integración extensa por fases y tabla de correspondencia.
- Apartado: EDA. Problema: nueve TODOs. Acción prevista: desarrollar con cinco CSV, cinco figuras comentadas y tabla descriptiva.
- Apartado: comparación de modelos. Problema: cinco TODOs y un solo VAE. Acción prevista: evaluar e implementar AE/VAE/variante VAE si es seguro y reproducible.
- Apartado: capítulo 6. Problema: datos prácticamente vacíos y herramientas en futuro. Acción prevista: ampliar estructura, ejecución, artefactos y trazabilidad.
- Apartado: conclusiones y prospectiva. Problema: capítulos vacíos. Acción prevista: cierre académico extenso y honesto.
- Apartado: bibliografía. Problema: 18 entradas y solo 10 citadas. Acción prevista: auditar metadatos locales, retirar comentarios internos si existen y no inventar referencias.

## Riesgos conceptuales detectados

- VAE/GAN/KL: la metodología larga describe una VAE-GAN y optimización informacional que no aparecen en el código. Deben conservarse solo como planteamiento original, teoría o futuro; KL es regularización del VAE.
- Comparación multmodelo: solo existe una configuración VAE ejecutada en el estado inicial.
- Extensión: el punto de partida obligatorio son 59 páginas; el resultado final no puede quedar por debajo.
- Bibliografía: solo hay 18 entradas BibTeX locales; alcanzar 20 exige localizar dos fuentes locales con metadatos suficientes o dejar constancia honesta de la limitación.
