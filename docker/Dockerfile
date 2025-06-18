FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of the application code
COPY . .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
