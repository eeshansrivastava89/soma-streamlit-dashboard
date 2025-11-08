FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Create .streamlit config directory
RUN mkdir -p ~/.streamlit

# Create Streamlit config to run headless
RUN echo '[server]\n\
headless = true\n\
port = 8501\n\
enableXsrfProtection = false\n\
\n\
[logger]\n\
level = "info"\n\
' > ~/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501').read()" || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true", "--client.showErrorDetails=false"]
