#!/usr/bin/env python3
"""
TaskTracker Azure Function Client Example

This script demonstrates how to interact with the TaskTracker Azure Function API.
"""

import json
import time
from typing import Any, Dict, Optional

import requests


class TaskTrackerClient:
    """Client for TaskTracker Azure Function API"""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the client

        Args:
            base_url: Base URL of the Azure Function (e.g., https://your-func.azurewebsites.net)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

        # Set headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'TaskTracker-Client/1.0'
        })

        if api_key:
            self.session.headers.update({
                'x-functions-key': api_key
            })

    def health_check(self) -> Dict[str, Any]:
        """Check if the API is healthy"""
        response = self.session.get(f"{self.base_url}/api/health")
        response.raise_for_status()
        return response.json()

    def list_models(self) -> Dict[str, Any]:
        """Get list of available models"""
        response = self.session.get(f"{self.base_url}/api/models")
        response.raise_for_status()
        return response.json()

    def predict(self, text: str, model_type: str = "mistral") -> Dict[str, Any]:
        """
        Make a prediction

        Args:
            text: Input text to analyze
            model_type: Type of model to use

        Returns:
            Prediction results
        """
        data = {
            "text": text,
            "model_type": model_type
        }

        response = self.session.post(
            f"{self.base_url}/api/predict",
            json=data
        )
        response.raise_for_status()
        return response.json()

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        response = self.session.get(f"{self.base_url}/api/config")
        response.raise_for_status()
        return response.json()

    def update_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update configuration

        Args:
            config: Configuration updates

        Returns:
            Update confirmation
        """
        response = self.session.post(
            f"{self.base_url}/api/config",
            json=config
        )
        response.raise_for_status()
        return response.json()


def main():
    """Main example function"""

    # Configuration
    BASE_URL = "http://localhost:7071"  # Change for deployed function
    API_KEY = None  # Set if using authentication

    # Initialize client
    client = TaskTrackerClient(BASE_URL, API_KEY)

    print("🚀 TaskTracker Azure Function Client Example")
    print(f"📡 Connecting to: {BASE_URL}")
    print()

    try:
        # 1. Health Check
        print("1. 🏥 Health Check")
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Message: {health['message']}")
        print()

        # 2. List Models
        print("2. 🤖 Available Models")
        models_response = client.list_models()
        models = models_response.get('models', [])
        for model in models:
            print(
                f"   - {model['name']} ({model['type']}) - {model['status']}")
        print()

        # 3. Get Configuration
        print("3. ⚙️ Current Configuration")
        config = client.get_config()
        print(f"   Default Model: {config.get('default_model', 'N/A')}")
        print(f"   API Version: {config.get('api_version', 'N/A')}")
        features = config.get('features', {})
        print("   Features:")
        for feature, enabled in features.items():
            status = "✅" if enabled else "❌"
            print(f"     {status} {feature}")
        print()

        # 4. Make Predictions
        print("4. 🔮 Making Predictions")

        test_texts = [
            "This is a sample text for analysis.",
            "Another example with different content.",
            "Can you analyze this text for me?"
        ]

        for i, text in enumerate(test_texts, 1):
            print(f"   Test {i}: {text[:50]}{'...' if len(text) > 50 else ''}")

            # Predict with different models
            for model in models[:2]:  # Test first 2 models
                model_name = model['name']
                try:
                    start_time = time.time()
                    result = client.predict(text, model_name)
                    end_time = time.time()

                    print(f"     {model_name}:")
                    print(
                        f"       Prediction: {result.get('prediction', 'N/A')}")
                    print(
                        f"       Confidence: {result.get('confidence', 'N/A')}")
                    print(f"       Time: {end_time - start_time:.2f}s")

                except requests.exceptions.RequestException as e:
                    print(f"     {model_name}: ❌ Error - {e}")

            print()

        # 5. Update Configuration
        print("5. 🔧 Updating Configuration")
        new_config = {
            "default_model": "phi3",
            "features": {
                "linear_probe": True,
                "triplet_probe": False,
                "activation_generation": True
            }
        }

        try:
            update_result = client.update_config(new_config)
            print(
                f"   ✅ {update_result.get('message', 'Configuration updated')}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error updating config: {e}")

        print()
        print("✅ Example completed successfully!")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the API")
        print("   Make sure the Azure Function is running")
        print("   For local testing: ./deployment/run_local.sh")

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()
