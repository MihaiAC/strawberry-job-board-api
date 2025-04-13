FROM continuumio/miniconda3

WORKDIR /app

# Create environment.
COPY environment.yml .
RUN conda env create -f environment.yml

# Install Postgres client, needed in order to wait for DB to be ready.
RUN apt-get update && apt-get install -y postgresql-client

# Copy application code.
COPY ./app /app

# Expose port.
EXPOSE 8000