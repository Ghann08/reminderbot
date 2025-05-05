FROM python:3.11-slim-bullseye

ENV TZ=Europe/Moscow

WORKDIR /app

COPY . .

# Install dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Command to run the application
CMD ["python3", "main.py"]

