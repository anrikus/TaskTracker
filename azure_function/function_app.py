import json
import logging
from typing import Any, Dict

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="v1/health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    logging.info('Health check endpoint was triggered.')

    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "message": "TaskTracker API is running"
        }),
        status_code=200,
        mimetype="application/json"
    )


@app.route(route="v1/predict", methods=["POST"])
def predict(req: func.HttpRequest) -> func.HttpResponse:
    """Main prediction endpoint"""
    logging.info('Predict endpoint was triggered.')

    try:
        # Parse request body
        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "Request body is required"}),
                status_code=400,
                mimetype="application/json"
            )

        # Extract input data
        input_text = req_body.get('text', '')
        model_type = req_body.get('model_type', 'default')

        if not input_text:
            return func.HttpResponse(
                json.dumps({"error": "Text input is required"}),
                status_code=400,
                mimetype="application/json"
            )

        # TODO: Replace with actual TaskTracker logic
        # For now, return a mock response
        result = {
            "input_text": input_text,
            "model_type": model_type,
            "prediction": "mock_prediction",
            "confidence": 0.95,
            "processed": True
        }

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error("Error in predict endpoint: %s", str(e))
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="v1/models", methods=["GET"])
def list_models(req: func.HttpRequest) -> func.HttpResponse:
    """List available models endpoint"""
    logging.info('List models endpoint was triggered.')

    try:
        # TODO: Replace with actual model listing logic
        models = [
            {"name": "llama3_70b", "type": "large_language_model",
                "status": "available"},
            {"name": "llama3_8b", "type": "language_model", "status": "available"},
            {"name": "mistral", "type": "language_model", "status": "available"},
            {"name": "mixtral", "type": "mixture_of_experts", "status": "available"},
            {"name": "phi3", "type": "small_language_model", "status": "available"}
        ]

        return func.HttpResponse(
            json.dumps({"models": models}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error in list_models endpoint: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
