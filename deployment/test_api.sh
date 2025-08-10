#!/bin/bash

# Test script for TaskTracker Azure Function API
set -e

BASE_URL="${BASE_URL:-http://localhost:7071}"
API_KEY="${API_KEY:-}"

echo "🧪 Testing TaskTracker Azure Function API"
echo "🌐 Base URL: $BASE_URL"

# Function to make API calls
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    
    echo "📡 Testing $method $endpoint"
    
    if [ -n "$API_KEY" ]; then
        auth_header="x-functions-key: $API_KEY"
    else
        auth_header=""
    fi
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -H "$auth_header" \
            -d "$data" \
            "$BASE_URL/api/$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -H "$auth_header" \
            "$BASE_URL/api/$endpoint")
    fi
    
    # Split response and status code
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    echo "   Status: $status_code"
    echo "   Response: $body"
    
    if [ "$status_code" -eq "$expected_status" ]; then
        echo "   ✅ Test passed"
    else
        echo "   ❌ Test failed - Expected $expected_status, got $status_code"
    fi
    echo ""
}

# Test 1: Health Check
make_request "GET" "health" "" 200

# Test 2: List Models
make_request "GET" "models" "" 200

# Test 3: Get Configuration
make_request "GET" "config" "" 200

# Test 4: Valid Prediction Request
prediction_data='{
    "text": "This is a test input for the model",
    "model_type": "mistral"
}'
make_request "POST" "predict" "$prediction_data" 200

# Test 5: Invalid Prediction Request (missing text)
invalid_data='{
    "model_type": "mistral"
}'
make_request "POST" "predict" "$invalid_data" 400

# Test 6: Update Configuration
config_data='{
    "default_model": "phi3",
    "features": {
        "linear_probe": true,
        "triplet_probe": false
    }
}'
make_request "POST" "config" "$config_data" 200

echo "🏁 API testing completed!"
echo ""
echo "💡 To test against deployed function:"
echo "   BASE_URL=https://your-function-app.azurewebsites.net ./test_api.sh"
echo ""
echo "💡 To test with API key:"
echo "   API_KEY=your-function-key ./test_api.sh"
