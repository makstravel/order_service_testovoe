FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    gettext \
    curl \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Устанавливаем права на скрипт
RUN chmod +x ./entrypoint.sh

# Запускаем через абсолютный путь
ENTRYPOINT ["./entrypoint.sh"]
