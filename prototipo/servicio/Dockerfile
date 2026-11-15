# Imagen del servicio para Azure Container Apps (#122): la API y el job de la ingesta.
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
EXPOSE 8000
CMD ["uvicorn", "app.main:aplicacion", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
