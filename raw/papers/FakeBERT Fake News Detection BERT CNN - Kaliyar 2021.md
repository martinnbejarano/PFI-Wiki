---
tipo: paper
titulo: "FakeBERT: Fake news detection in social media with a BERT-based deep learning approach"
autores: [Kaliyar, Rohit Kumar, Goswami, Anurag, Narang, Pratik]
año: 2021
venue: "Multimedia Tools and Applications, vol. 80. Springer"
doi: "10.1007/s11042-020-10183-2"
url: "https://link.springer.com/article/10.1007/s11042-020-10183-2"
relevancia: media
temas: [fakebert, bert, cnn, fake-news, deep-learning, clasificacion, estado-del-arte]
---

# FakeBERT: Fake news detection in social media with a BERT-based deep learning approach

## Referencia completa

Kaliyar, R. K., Goswami, A. y Narang, P. (2021). FakeBERT: Fake news detection in social media with a BERT-based deep learning approach. *Multimedia Tools and Applications*, vol. 80, pp. 11765–11788. DOI: 10.1007/s11042-020-10183-2.

## Resumen

Propone FakeBERT: arquitectura que combina BERT (para representación contextual) con capas CNN paralelas (3 capas convolucionales + 2 MaxPooling) en la cabeza de clasificación. El objetivo es capturar tanto representaciones contextuales (BERT) como patrones locales de n-gramas (CNN).

## Hallazgos clave

- 98.90% de accuracy en dataset Kaggle Fake-News (clasificación binaria, inglés)
- Combina fortalezas de BERT (contexto global) + CNN (patrones locales)
- Supera a BiLSTM+BERT y otros baselines en el mismo dataset
- Limitación: evaluado en un solo dataset con posible sobreajuste al dominio

## Limitaciones

- Solo inglés; dataset Kaggle tiene sesgo hacia medios occidentales
- Alta accuracy puede indicar sobreajuste: el dataset Kaggle es relativamente simple en clasificación binaria
- No evaluado en datasets multidominio ni en condiciones de producción real

## Relevancia para el PFI

Arquitectura de referencia BERT+CNN. El sistema propuesto en el PFI puede compararse contra FakeBERT como baseline. En el Estado del Arte, documenta el resultado de 98.9% en clasificación binaria para contextualizar el rendimiento esperado del clasificador propio.

**Clave biblio:** `KaliyarEtAl2021`
