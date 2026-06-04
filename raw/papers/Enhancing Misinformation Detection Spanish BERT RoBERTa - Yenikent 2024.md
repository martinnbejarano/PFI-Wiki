---
tipo: paper
titulo: "Enhancing Misinformation Detection in Spanish Language with Deep Learning: BERT and RoBERTa Transformer Models"
autores: [Yenikent, Sila, Alonso-Bartolome, Santiago, Saez-Martin, Carlos A.]
año: 2024
venue: "Applied Sciences, vol. 14, no. 21, art. 9729. MDPI"
doi: "10.3390/app14219729"
url: "https://doi.org/10.3390/app14219729"
relevancia: media-alta
temas: [fake-news-espanol, bert, roberta, clasificacion, espanol, fine-tuning, misinformacion]
---

# Enhancing Misinformation Detection in Spanish Language with Deep Learning: BERT and RoBERTa Transformer Models

## Referencia completa

Yenikent, S., Alonso-Bartolome, S. y Saez-Martin, C. A. (2024). Enhancing Misinformation Detection in Spanish Language with Deep Learning: BERT and RoBERTa Transformer Models. *Applied Sciences*, vol. 14, n.º 21, art. 9729. DOI: 10.3390/app14219729.

## Resumen

Fine-tuning y benchmark de variantes BERT y RoBERTa para detección de fake news políticas en español. Dataset sintético de 57.231 artículos en español generado con web scraping + LLMs. Modelos evaluados: BETO, MarIA, RoBERTa-BNE, BERTIN, RBNEC.

## Hallazgos clave

- Accuracy de 97.4% a 98.6% en el dataset sintético propio (en dominio)
- Al testar en dataset externo independiente (debates electorales España, julio 2023): **71% de accuracy** (caída crítica)
- RoBERTa-BNE supera a BETO en todas las métricas
- El gap de 97-98% → 71% ilustra el problema de generalización cross-domain
- Dataset sintético puede no capturar patrones de fake news reales

## Relevancia para el PFI

Evidencia directa de que incluso los mejores modelos en español sufren generalización limitada a datos reales fuera del dominio de entrenamiento. Este resultado justifica la necesidad de construir un dataset argentino real (no sintético) para el PFI. Contexto España, no LATAM.

**Clave biblio:** `YenikentEtAl2024`
