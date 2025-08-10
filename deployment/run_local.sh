#!/bin/bash

# Local Development Script for TaskTracker Azure Function
set -e

echo "🚀 Starting TaskTracker Azure Function locally"

# Navigate to azure_function directory
cd "$(dirname "$0")/../azure_function"

# Check if Azure Functions Core Tools is installed
if ! command -v func &> /dev/null; then
    echo "🔧 Installing Azure Functions Core Tools..."
    npm install -g azure-functions-core-tools@4 --unsafe-perm true
fi

# Create local.settings.json if it doesn't exist
if [ ! -f "local.settings.json" ]; then
    echo "⚙️ Creating local.settings.json..."
    cat > local.settings.json << EOF
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "TASKTRACKER_LOG_LEVEL": "DEBUG",
    "TASKTRACKER_MODEL_PATH": "../trained_linear_probes",
    "TASKTRACKER_CONFIG_PATH": "../config"
  }
}
EOF
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install tasktracker package in development mode
echo "🔧 Installing TaskTracker package..."
cd ..
pip install -e .

# Go back to azure_function directory
cd azure_function

# Start the function app
echo "🚀 Starting Azure Function locally..."
echo "🌐 Local endpoints will be available at:"
echo "   - Health Check: http://localhost:7071/api/health"
echo "   - Predict: http://localhost:7071/api/predict"
echo "   - Models: http://localhost:7071/api/models"
echo "   - Config: http://localhost:7071/api/config"
echo ""
echo "Press Ctrl+C to stop the function app"

func start --python
