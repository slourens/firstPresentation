FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY services /app/services
COPY contracts /app/contracts
CMD ["python", "-m", "services.extract.worker"]
