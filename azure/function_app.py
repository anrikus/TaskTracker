
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import azure.functions as func

from task_tracker import activation_generation, linear_probe, triplet_probe

TASKTRACKER_AVAILABLE = True


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

        # Example: Use TaskTracker's linear_probe if available
        if TASKTRACKER_AVAILABLE:
            # Replace this with your actual TaskTracker logic
            # For demonstration, just echo input
            prediction = f"Processed by TaskTracker: {input_text}"
            confidence = 0.99
            processed = True
        else:
            prediction = "mock_prediction"
            confidence = 0.0
            processed = False

        result = {
            "input_text": input_text,
            "model_type": model_type,
            "prediction": prediction,
            "confidence": confidence,
            "processed": processed
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


@app.route(route="v1/probes", methods=["GET"])
def list_probes(req: func.HttpRequest) -> func.HttpResponse:
    """List available probes endpoint"""
    logging.info('List probes endpoint was triggered.')

    try:
        probes = []
        
        # Path to the trained linear probes directory
        probes_dir = Path(__file__).parent.parent / "models" / "trained_linear_probes"
        
        if probes_dir.exists():
            # Iterate through each model directory
            for model_dir in probes_dir.iterdir():
                if model_dir.is_dir():
                    model_name = model_dir.name
                    layers = []
                    
                    # Iterate through each layer directory within the model
                    for layer_dir in model_dir.iterdir():
                        if layer_dir.is_dir() and layer_dir.name.isdigit():
                            layer_num = int(layer_dir.name)
                            
                            # Check if this layer has the required files
                            config_file = layer_dir / "config.json"
                            model_file = layer_dir / "model.pickle"
                            
                            if config_file.exists() and model_file.exists():
                                layers.append(layer_num)
                    
                    # Sort layers by layer number
                    layers.sort()  # Simple numeric sort since layers are now just integers
                    
                    if layers:  # Only include models that have available layers
                        probes.append({
                            "model": model_name,
                            "type": "linear_probe",
                            "layers": layers
                        })
        
        return func.HttpResponse(
            json.dumps({"probes": probes}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error("Error in list_probes endpoint: %s", str(e))
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
