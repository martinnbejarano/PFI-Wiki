# El entrenamiento corrió con Python 3.13.
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# El modelo del embebedor (`/embeber`) se baja al construir y no en cada arranque
# en frío. Con HF_HUB_OFFLINE=1 en el entorno, `from_pretrained` ni consulta el Hub.
ENV HF_HOME=/app/.hf
RUN python -c "from transformers import AutoModel, AutoTokenizer; m = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'; AutoTokenizer.from_pretrained(m); AutoModel.from_pretrained(m)"
COPY . .
EXPOSE 7860
# `::` para la red privada de Railway (solo IPv6); Azure Container Apps prueba el
# arranque por IPv4 y corre con HOST=0.0.0.0.
ENV HOST=::
CMD python -m uvicorn app:app --host "$HOST" --port 7860
