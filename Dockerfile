FROM continuumio/miniconda3

WORKDIR /app

# Create environment.
COPY environment.yml .
RUN conda env create -f environment.yml

# Copy application code.
COPY ./app /app

# Expose port.
EXPOSE 8000