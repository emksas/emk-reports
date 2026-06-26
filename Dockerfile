FROM python:3.12-slim

# Evita problemas de buffer (logs en tiempo real)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

EXPOSE 8084

CMD ["python", "manage.py", "runserver", "0.0.0.0:8084"]
