# El entrenamiento corrió con Python 3.13.
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "-m", "uvicorn", "app:app", "--host", "::", "--port", "7860"]
