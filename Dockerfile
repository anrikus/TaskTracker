# TaskTracker Azure Function Container
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true \
    PYTHONPATH=/home/site/wwwroot

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY azure_function/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the entire project
COPY . /home/site/wwwroot/

# Install TaskTracker package
WORKDIR /home/site/wwwroot
RUN pip install -e .

# Copy function app files to the correct location
COPY azure_function/ /home/site/wwwroot/

# Set working directory
WORKDIR /home/site/wwwroot
