FROM python:3.10-slim

WORKDIR /usr/src/app

# Copy only requirements first for caching
COPY requirements.txt ./
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app ./app

ENV PATH="/usr/src/app/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
