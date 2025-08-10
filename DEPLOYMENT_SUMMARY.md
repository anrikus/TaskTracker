# TaskTracker Azure Function Deployment Template

## 🎯 Overview

This template provides a complete solution for packaging and deploying the TaskTracker Python package as an Azure Function with REST API integration. The template includes:

- ✅ **Azure Function App** with HTTP triggers
- ✅ **REST API endpoints** for model interaction
- ✅ **Automated deployment scripts**
- ✅ **Infrastructure as Code** (ARM templates)
- ✅ **CI/CD pipeline** (GitHub Actions)
- ✅ **Local development environment**
- ✅ **API testing tools**
- ✅ **Client examples**
- ✅ **Container support** (Docker)

## 🏗️ Template Structure

```
TaskTracker/
├── azure_function/                 # Azure Function application
│   ├── function_app.py            # Main function code with API endpoints
│   ├── host.json                  # Function runtime configuration
│   ├── requirements.txt           # Python dependencies
│   └── .env.template             # Environment variables template
│
├── deployment/                    # Deployment automation
│   ├── deploy.sh                 # One-click Azure deployment
│   ├── run_local.sh              # Local development server
│   ├── test_api.sh               # API endpoint testing
│   ├── README.md                 # Comprehensive documentation
│   └── arm-templates/            # Infrastructure as Code
│       ├── azuredeploy.json      # ARM template
│       └── azuredeploy.parameters.json
│
├── .github/workflows/             # CI/CD automation
│   └── deploy-azure-function.yml # GitHub Actions pipeline
│
├── examples/                      # Usage examples
│   └── client_example.py         # Python client example
│
├── Dockerfile                     # Container support
├── docker-compose.yml            # Local container orchestration
└── DEPLOYMENT_SUMMARY.md         # This file
```

## 🚀 API Endpoints

The template provides the following REST API endpoints:

| Endpoint | Method | Description | Example |
|----------|---------|-------------|---------|
| `/api/health` | GET | Health check | `{"status": "healthy"}` |
| `/api/models` | GET | List available models | `{"models": [...]}` |
| `/api/predict` | POST | Make predictions | `{"text": "...", "model_type": "mistral"}` |
| `/api/config` | GET/POST | Configuration management | `{"default_model": "phi3"}` |

## 🛠️ Quick Start Guide

### 1. Local Development (2 minutes)
```bash
# Start local development server
./deployment/run_local.sh

# Test the API
./deployment/test_api.sh
```

### 2. Azure Deployment (5 minutes)
```bash
# Deploy to Azure (creates all resources)
./deployment/deploy.sh

# Test deployed API
BASE_URL=https://your-function-app.azurewebsites.net ./deployment/test_api.sh
```

### 3. Container Deployment (Alternative)
```bash
# Build and run with Docker
docker-compose up --build

# Test containerized API
./deployment/test_api.sh
```

## 📋 Prerequisites Checklist

- [ ] **Azure CLI** installed and logged in (`az login`)
- [ ] **Python 3.11+** installed
- [ ] **Node.js** (for Azure Functions Core Tools)
- [ ] **Git** for version control
- [ ] **Docker** (optional, for container deployment)

## 🔧 Configuration Options

### Environment Variables
```bash
# Function Runtime
FUNCTIONS_WORKER_RUNTIME=python
FUNCTIONS_EXTENSION_VERSION=~4

# TaskTracker Settings
TASKTRACKER_LOG_LEVEL=INFO
TASKTRACKER_MODEL_PATH=/models
TASKTRACKER_CONFIG_PATH=/config

# Monitoring (optional)
APPINSIGHTS_INSTRUMENTATIONKEY=your-key
```

### Deployment Settings
```bash
# Resource naming
RESOURCE_GROUP_NAME=tasktracker-rg
FUNCTION_APP_NAME=tasktracker-func
STORAGE_ACCOUNT_NAME=tasktrackerstorage
LOCATION=eastus
```

## 🔐 Security Features

- ✅ **HTTPS only** in production
- ✅ **Function key authentication** by default
- ✅ **Azure AD integration** ready
- ✅ **CORS configuration** included
- ✅ **Minimum TLS 1.2** enforced

## 📊 Monitoring & Observability

- ✅ **Application Insights** integration
- ✅ **Structured logging** throughout
- ✅ **Health check endpoint** for monitoring
- ✅ **Performance metrics** collection
- ✅ **Error tracking** and alerting

## 🚀 CI/CD Pipeline Features

The GitHub Actions workflow provides:

- ✅ **Automated testing** on pull requests
- ✅ **Code quality checks** (linting, formatting)
- ✅ **Automated deployment** on main branch
- ✅ **Infrastructure deployment** option
- ✅ **Post-deployment testing**

### Required GitHub Secrets
```
AZURE_CREDENTIALS               # Service principal credentials
AZURE_FUNCTIONAPP_PUBLISH_PROFILE  # Function app publish profile
AZURE_SUBSCRIPTION_ID           # Azure subscription ID
AZURE_RG                       # Resource group name
```

## 🧪 Testing Strategy

### 1. Unit Tests
```bash
# Run TaskTracker package tests
python -m pytest tests/
```

### 2. API Integration Tests
```bash
# Test all endpoints
./deployment/test_api.sh
```

### 3. Load Testing (Optional)
```bash
# Example with curl
for i in {1..100}; do
  curl -X POST "https://your-func.azurewebsites.net/api/predict" \
    -H "Content-Type: application/json" \
    -d '{"text": "test", "model_type": "mistral"}' &
done
wait
```

## 📈 Scaling Considerations

### Performance Optimization
- **Cold Start Mitigation**: Use Premium plan for always-on
- **Concurrent Execution**: Configure `maxConcurrentRequests`
- **Memory Allocation**: Adjust based on model size
- **Timeout Settings**: Configure for long-running predictions

### Cost Optimization
- **Consumption Plan**: Pay per execution (default)
- **Premium Plan**: Fixed cost, better performance
- **App Service Plan**: Dedicated resources

## 🔄 Integration Patterns

### 1. Synchronous API Calls
```python
# Direct HTTP requests
response = requests.post(
    "https://your-func.azurewebsites.net/api/predict",
    json={"text": "analyze this", "model_type": "mistral"}
)
```

### 2. Asynchronous Processing
```python
# Using Azure Service Bus or Storage Queues
# For long-running tasks
```

### 3. Batch Processing
```python
# Process multiple items
texts = ["text1", "text2", "text3"]
results = []
for text in texts:
    result = client.predict(text)
    results.append(result)
```

## 🛠️ Customization Guide

### Adding New Models
1. Update model list in `function_app.py`
2. Add model loading logic
3. Update configuration schema
4. Add tests

### Adding New Endpoints
1. Add function decorator in `function_app.py`
2. Implement request/response handling
3. Update API documentation
4. Add to test suite

### Custom Authentication
1. Configure Azure AD in portal
2. Update function auth level
3. Modify client examples
4. Update CI/CD pipeline

## 🐛 Troubleshooting Guide

### Common Issues

1. **Cold Starts**
   - Symptom: First request is slow
   - Solution: Use Premium plan or keep-alive requests

2. **Import Errors**
   - Symptom: Module not found errors
   - Solution: Check `requirements.txt` and PYTHONPATH

3. **Memory Issues**
   - Symptom: Out of memory errors
   - Solution: Optimize models or increase memory allocation

4. **Timeout Errors**
   - Symptom: Function times out
   - Solution: Increase timeout in `host.json`

### Debug Commands
```bash
# Check function logs
az functionapp log tail --name your-func --resource-group your-rg

# Test local function
func start --python --verbose

# Check deployment status
az functionapp show --name your-func --resource-group your-rg
```

## 📚 Next Steps

### Phase 1: Basic Setup ✅
- [x] Template structure created
- [x] Basic API endpoints implemented
- [x] Deployment scripts ready
- [x] Documentation complete

### Phase 2: Integration (TODO)
- [ ] Integrate actual TaskTracker models
- [ ] Add authentication middleware
- [ ] Implement caching layer
- [ ] Add rate limiting

### Phase 3: Production (TODO)
- [ ] Performance optimization
- [ ] Advanced monitoring
- [ ] Multi-region deployment
- [ ] API versioning

## 🤝 Contributing

1. **Development**: Make changes to `azure_function/`
2. **Testing**: Run `./deployment/test_api.sh`
3. **Documentation**: Update relevant README files
4. **Deployment**: CI/CD handles automatic deployment

## 📞 Support

- **Documentation**: See `deployment/README.md`
- **Examples**: Check `examples/client_example.py`
- **Issues**: Use GitHub Issues for bug reports
- **Questions**: Use GitHub Discussions

---

🎉 **Ready to deploy!** Start with `./deployment/run_local.sh` for local development or `./deployment/deploy.sh` for Azure deployment.
