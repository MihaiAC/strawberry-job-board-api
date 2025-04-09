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