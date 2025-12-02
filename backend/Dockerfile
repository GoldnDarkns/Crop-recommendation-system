# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files (app, model, etc.)
COPY app.py .
COPY crop_recommendation_model.joblib .
COPY sample_batch.csv .
COPY test_client.py .

# Expose the port (optional, for documentation)
EXPOSE 7860

# Environment variable for Flask / HF
ENV PORT=7860

# Start the app with gunicorn in production mode
# "app:app" means: module app.py, Flask instance variable "app"
CMD ["bash", "-c", "gunicorn -b 0.0.0.0:${PORT} app:app"]