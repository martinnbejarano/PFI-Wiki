---
tipo: paper
titulo: "\"Liar, Liar Pants on Fire\": A New Benchmark Dataset for Fake News Detection"
autores: [Wang, William Yang]
año: 2017
venue: "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL 2017), Short Papers"
doi: "10.18653/v1/P17-2067"
acl: "https://aclanthology.org/P17-2067/"
arxiv: "https://arxiv.org/abs/1705.00648"
url: "https://aclanthology.org/P17-2067/"
relevancia: alta
temas: [dataset, liar, fake-news, benchmark, politifact, clasificacion-multiclase]
citaciones: ~2500
---

# "Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection

## Referencia completa

Wang, W. Y. (2017). "Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection. *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, pp. 422–426. DOI: 10.18653/v1/P17-2067.

## Resumen

Introduce LIAR: 12.836 declaraciones cortas extraídas de PolitiFact.com durante una década, con etiquetas de veracidad en 6 clases finas. Propone una CNN híbrida que integra texto de la declaración + metadatos del hablante (partido, estado, cargo). Primer dataset público de escala para fake news detection.

## Hallazgos clave

- 12.836 declaraciones etiquetadas: pants-fire (4%), false (19%), barely-true (17%), half-true (21%), mostly-true (21%), true (18%)
- 12 features de metadatos por declaración: hablante, partido, estado, cargo, contexto, historial de veracidad
- Baseline CNN híbrida: 27.4% accuracy en 6 clases (techo bajo sin conocimiento externo)
- SVM lineal y RoBERTa obtienen ~62% en clasificación de 6 clases (Hasan et al. 2025)
- Binario simplificado (verdadero/falso): modelos alcanzan 99%+ (techo alto cuando se elimina la ambigüedad)
- Dataset disponible en: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip

## Limitaciones

- Fuente única (PolitiFact): sesgo hacia política estadounidense
- Declaraciones cortas sin contexto adicional (solo el enunciado + metadata)
- Escasez de declaraciones sobre ciencia, salud, economía en comparación con política
- No incluye datos de propagación en redes sociales

## Relevancia para el PFI

**Dataset de benchmark obligatorio.** Toda comparación de modelos en el PFI debe incluir resultados en LIAR (o explicitar por qué no se usa). Los resultados en LIAR permiten comparar el sistema con la literatura internacional. El techo de 62% en 6 clases justifica la necesidad de información externa (knowledge retrieval).

**Clave biblio:** `Wang2017`
