---
title: Clasificador de desinformación (PFI)
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

Servicio de inferencia del Módulo 1 del PFI (UADE, 2026). `POST /clasificar` con
`{"texto": "..."}` devuelve `{"puntaje", "clase", "version_modelo"}`; el puntaje es la
probabilidad de «falso». Código fuente: `prototipo/clasificador/` en
`martinnbejarano/PFI-Wiki`.
