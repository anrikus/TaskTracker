# TaskTracker Azure Function Deployment

This directory contains all the necessary files and scripts to deploy TaskTracker as an Azure Function with API integration.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client Apps   │───▶│  Azure Function  │───▶│  TaskTracker    │
│                 │    │     (API)        │    │   Package       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Application      │
                       │ Insights         │
                       └──────────────────┘
```

## 📁 Directory Structure

```
azure_function/
├── function_app.py          # Main Azure Function code
├── host.json               # Function app configuration
├── requirements.txt        # Python dependencies
└── .env.template          # Environment variables template

deployment/
├── deploy.sh              # Automated deployment script
├── run_local.sh           # Local development script
├── test_api.sh            # API testing script
└── arm-templates/
    ├── azuredeploy.json           # ARM template
    └── azuredeploy.parameters.json # ARM parameters

.github/workflows/
└── deploy-azure-function.yml # CI/CD pipeline
```

## 🚀 Quick Start

### Prerequisites

- Azure CLI installed and logged in
- Python 3.11+ installed
- Node.js (for Azure Functions Core Tools)
- Git

### 1. Local Development

```bash
# Clone and setup
git clone <repository-url>
cd TaskTracker

# Run locally
./deployment/run_local.sh
```

The function will be available at `http://localhost:7071`

### 2. Test the API

```bash
# Test local instance
./deployment/test_api.sh

# Test deployed instance
BASE_URL=https://your-function-app.azurewebsites.net ./deployment/test_api.sh
```

### 3. Deploy to Azure

```bash
# Quick deployment (creates resources and deploys)
./deployment/deploy.sh

# Or set custom names
RESOURCE_GROUP_NAME=my-rg FUNCTION_APP_NAME=my-func ./deployment/deploy.sh
```

## 🔧 Configuration

### Environment Variables

Copy `.env.template` to `.env` and configure:

```bash
# Required
FUNCTIONS_WORKER_RUNTIME=python
FUNCTIONS_EXTENSION_VERSION=~4
AzureWebJobsStorage=UseDevelopmentStorage=true

# TaskTracker specific
TASKTRACKER_MODEL_PATH=/models
TASKTRACKER_CONFIG_PATH=/config
TASKTRACKER_LOG_LEVEL=INFO

# Optional: Application Insights
APPINSIGHTS_INSTRUMENTATIONKEY=your-key-here
```

### Function App Settings

These are automatically configured during deployment:

- `FUNCTIONS_WORKER_RUNTIME`: Python runtime
- `TASKTRACKER_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `TASKTRACKER_MODEL_PATH`: Path to model files
- `TASKTRACKER_CONFIG_PATH`: Path to configuration files

## 📡 API Endpoints

All endpoints are available at `https://{function-app-name}.azurewebsites.net/api/`

### Health Check
```bash
GET /api/health
```
Response:
```json
{
    "status": "healthy",
    "message": "TaskTracker API is running"
}
```

### Prediction
```bash
POST /api/predict
Content-Type: application/json

{
    "text": "Input text for analysis",
    "model_type": "mistral"
}
```
Response:
```json
{
    "input_text": "Input text for analysis",
    "model_type": "mistral",
    "prediction": "prediction_result",
    "confidence": 0.95,
    "processed": true
}
```

### List Models
```bash
GET /api/models
```
Response:
```json
{
    "models": [
        {
            "name": "llama3_70b",
            "type": "large_language_model",
            "status": "available"
        }
    ]
}
```

### Configuration Management
```bash
# Get configuration
GET /api/config

# Update configuration
POST /api/config
Content-Type: application/json

{
    "default_model": "phi3",
    "features": {
        "linear_probe": true,
        "triplet_probe": false
    }
}
```

## 🔐 Security

### Authentication

Azure Functions supports multiple authentication methods:

1. **Function Keys** (default): Add `?code=<function-key>` to requests
2. **Azure AD**: Configure in Azure portal
3. **API Management**: For advanced scenarios

### HTTPS

All endpoints enforce HTTPS in production. Local development uses HTTP.

## 📊 Monitoring

### Application Insights

Automatically configured for:
- Request/response logging
- Performance metrics
- Error tracking
- Custom telemetry

### Logs

Access logs via:
- Azure Portal → Function App → Monitor
- Azure CLI: `az functionapp log tail`
- Application Insights queries

## 🛠️ Troubleshooting

### Common Issues

1. **Cold starts**: First request may be slow
   - Solution: Use Premium plan for always-on
   
2. **Import errors**: Missing dependencies
   - Solution: Check `requirements.txt` is complete
   
3. **Authentication failures**: Missing or invalid keys
   - Solution: Verify function keys in Azure portal

### Debug Locally

```bash
# Enable debug logging
export TASKTRACKER_LOG_LEVEL=DEBUG

# Run with verbose output
func start --python --verbose
```

### Check Deployment Status

```bash
# View deployment logs
az functionapp log tail --name your-function-app --resource-group your-rg

# Check function status
az functionapp show --name your-function-app --resource-group your-rg
```

## 🚀 CI/CD Pipeline

GitHub Actions workflow automatically:

1. **Tests**: Runs linting and unit tests
2. **Builds**: Installs dependencies
3. **Deploys**: Publishes to Azure Function
4. **Validates**: Tests deployed endpoints

### Setup Secrets

Required GitHub repository secrets:

```
AZURE_CREDENTIALS: Service principal credentials
AZURE_FUNCTIONAPP_PUBLISH_PROFILE: Function app publish profile
AZURE_SUBSCRIPTION_ID: Azure subscription ID
AZURE_RG: Resource group name
```

## 📝 Customization

### Adding New Endpoints

1. Add new function in `function_app.py`:
```python
@app.route(route="myendpoint", methods=["GET", "POST"])
def my_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    # Your logic here
    return func.HttpResponse("Hello")
```

2. Update tests in `test_api.sh`
3. Deploy changes

### Integrating TaskTracker Logic

Replace TODO comments in `function_app.py` with actual TaskTracker functionality:

```python
# Replace mock prediction with real logic
from task_tracker.models import YourModel
model = YourModel.load(model_path)
result = model.predict(input_text)
```

## 📚 Additional Resources

- [Azure Functions Python Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [ARM Template Reference](https://docs.microsoft.com/en-us/azure/templates/)
- [GitHub Actions for Azure](https://github.com/Azure/actions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes to Azure Function code
4. Test locally with `./deployment/run_local.sh`
5. Run tests with `./deployment/test_api.sh`
6. Submit a pull request

The CI/CD pipeline will automatically test and deploy approved changes.
