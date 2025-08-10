#!/bin/bash

# Azure Function Deployment Script for TaskTracker
set -e

echo "🚀 Starting TaskTracker Azure Function Deployment"

# Configuration
RESOURCE_GROUP_NAME="${RESOURCE_GROUP_NAME:-tasktracker-rg}"
FUNCTION_APP_NAME="${FUNCTION_APP_NAME:-tasktracker-func-$(date +%s)}"
STORAGE_ACCOUNT_NAME="${STORAGE_ACCOUNT_NAME:-tasktrackerstorage$(date +%s)}"
LOCATION="${LOCATION:-eastus}"
PYTHON_VERSION="${PYTHON_VERSION:-3.11}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Login check
echo "🔐 Checking Azure CLI login status..."
if ! az account show &> /dev/null; then
    echo "🔑 Please login to Azure CLI first:"
    az login
fi

# Create resource group
echo "📦 Creating resource group: $RESOURCE_GROUP_NAME"
az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"

# Create storage account
echo "💾 Creating storage account: $STORAGE_ACCOUNT_NAME"
az storage account create \
    --name "$STORAGE_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --sku Standard_LRS

# Create function app
echo "⚡ Creating function app: $FUNCTION_APP_NAME"
az functionapp create \
    --name "$FUNCTION_APP_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --storage-account "$STORAGE_ACCOUNT_NAME" \
    --consumption-plan-location "$LOCATION" \
    --runtime python \
    --runtime-version "$PYTHON_VERSION" \
    --functions-version 4 \
    --os-type Linux

# Configure app settings
echo "⚙️ Configuring app settings..."
az functionapp config appsettings set \
    --name "$FUNCTION_APP_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --settings \
        "FUNCTIONS_WORKER_RUNTIME=python" \
        "TASKTRACKER_LOG_LEVEL=INFO" \
        "TASKTRACKER_MODEL_PATH=/tmp/models" \
        "TASKTRACKER_CONFIG_PATH=/tmp/config"

# Deploy the function
echo "📤 Deploying function code..."
cd "$(dirname "$0")/../azure_function"

# Install Azure Functions Core Tools if not present
if ! command -v func &> /dev/null; then
    echo "🔧 Installing Azure Functions Core Tools..."
    npm install -g azure-functions-core-tools@4 --unsafe-perm true
fi

# Deploy using Azure Functions Core Tools
func azure functionapp publish "$FUNCTION_APP_NAME" --python

echo "✅ Deployment completed successfully!"
echo "🌐 Function App URL: https://$FUNCTION_APP_NAME.azurewebsites.net"
echo "🔗 API Endpoints:"
echo "   - Health Check: https://$FUNCTION_APP_NAME.azurewebsites.net/api/health"
echo "   - Predict: https://$FUNCTION_APP_NAME.azurewebsites.net/api/predict"
echo "   - Models: https://$FUNCTION_APP_NAME.azurewebsites.net/api/models"
echo "   - Config: https://$FUNCTION_APP_NAME.azurewebsites.net/api/config"

# Save deployment info
echo "💾 Saving deployment information..."
cat > "$(dirname "$0")/deployment_info.json" << EOF
{
    "resource_group": "$RESOURCE_GROUP_NAME",
    "function_app_name": "$FUNCTION_APP_NAME",
    "storage_account": "$STORAGE_ACCOUNT_NAME",
    "location": "$LOCATION",
    "deployment_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "endpoints": {
        "base_url": "https://$FUNCTION_APP_NAME.azurewebsites.net",
        "health": "https://$FUNCTION_APP_NAME.azurewebsites.net/api/health",
        "predict": "https://$FUNCTION_APP_NAME.azurewebsites.net/api/predict",
        "models": "https://$FUNCTION_APP_NAME.azurewebsites.net/api/models",
        "config": "https://$FUNCTION_APP_NAME.azurewebsites.net/api/config"
    }
}
EOF

echo "📋 Deployment information saved to deployment_info.json"
