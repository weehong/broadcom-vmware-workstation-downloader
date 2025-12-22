FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

WORKDIR /app

# Install Playwright Python package
RUN pip install playwright

COPY Scripts/download_software.py .

CMD ["python3", "download_software.py"]
