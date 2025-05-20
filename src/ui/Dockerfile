# src/ui/Dockerfile

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

# Install dependencies
COPY src/ui/ui_requirements.txt .
RUN pip install --no-cache-dir -r ui_requirements.txt

# Copy UI app code
COPY src/ui/ .

# Expose the port for Render/local
EXPOSE 7860

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
