# Auditoría bibliográfica APA

## Resumen cuantitativo

- Entradas totales en `latex/bibliografia.bib`: **18**.
- Claves de cita únicas usadas en archivos `.tex`: **10**.
- Entradas citadas pero ausentes del `.bib`: **0**.
- Entradas del `.bib` no citadas: **8**.
- Objetivo indicado por el tutor: mínimo 20 referencias académicas relevantes; faltan al menos 2, sujetas a selección académica manual.

## Claves citadas

`NIPS2016_8a3363ab`, `aghapour2025solving`, `arjovsky2017wasserstein`, `boyd2004convex`, `cover2006elements`, `goodfellow2014generative`, `kingma2013auto`, `markowitz1952`, `takahashi2019modeling`, `zhang2020deep`.

## Entradas no citadas

`huang2020deep`, `jiang2017deep`, `lopez2018advances`, `lopezdeprado2018chapter1`, `machin2026repositorio`, `opitz2017latent`, `rasekhschaffe2026`, `voronina2025genai`.

## Campos básicos

Todas las entradas contienen `author`, `title` y `year`. Los artículos contienen `journal`, los `inproceedings` contienen `booktitle` y los libros contienen `publisher`. Las entradas `misc` usan `howpublished`.

No se exige inventar DOI o URL. Varias entradas no los incluyen; deben completarse únicamente después de consultar una fuente fiable.

## Posibles incidencias APA o BibTeX

- `NIPS2016_8a3363ab`: campo `pages` vacío y autor `Chen, Xi` repetido.
- `arjovsky2017wasserstein`: se eliminó un carácter `´` residual situado después del cierre de la entrada, que era sintaxis ajena a BibTeX.
- Varias referencias arXiv carecen de DOI o URL verificable en la entrada.
- Las notas de `rasekhschaffe2026`, `aghapour2025solving`, `voronina2025genai` y `opitz2017latent` contienen comentarios descriptivos; revisar si deben aparecer en la bibliografía final APA.
- Existe inconsistencia de capitalización entre títulos. Debe revisarse según las reglas de `apacite` y proteger con llaves solo los nombres propios o siglas necesarios.
- `machin2026repositorio` no es una referencia académica y no debería contarse automáticamente para el mínimo de 20.

La compilación final no presenta citas indefinidas. Esta auditoría no valida la exactitud externa de autores, años, DOI o títulos.
