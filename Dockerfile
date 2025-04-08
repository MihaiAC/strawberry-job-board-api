FROM continuumio/miniconda3

WORKDIR /app

# Create environment.
COPY environment.yml .
RUN conda env create -f environment.yml

# Use conda env.
SHELL [ "conda", "run", "-n", "strawberry_fast_api", "/bin/bash", "-c" ]

# Copy application code.
COPY ./app /app

# Expose port.
EXPOSE 8000

# Run app.
# Run FastAPI app
CMD ["conda", "run", "-n", "strawberry_fast_api", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]