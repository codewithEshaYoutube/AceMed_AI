import requests
import uuid
import json
import os
from datetime import datetime

# Configuration
API_KEY = "xKQyEGwC.uCyxokv9TXGkDscfGZxVNrCLiJT7rIkv"
BASE_URL = "https://payload.vextapp.com/hook/ICYAJ67MIS/catch"

# Generate a unique channel token
def generate_channel_token():
    """Generate a unique channel token using timestamp and UUID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{random_id}"

def send_payload(payload_data, environment="dev", channel_token=None):
    """
    Send payload to Vextapp API
    
    Args:
        payload_data (str): The data to send
        environment (str): Environment (dev, stage, prod)
        channel_token (str, optional): Custom channel token, generates one if not provided
    
    Returns:
        dict: API response
    """
    # Use provided channel token or generate a new one
    token = channel_token or generate_channel_token()
    
    # Prepare URL with channel token
    url = f"{BASE_URL}/{token}"
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Apikey": f"Api-Key {API_KEY}"
    }
    
    # Prepare data
    data = {
        "payload": payload_data,
        "env": environment
    }
    
    try:
        # Make API call
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Check response
        if response.status_code == 200:
            print(f"Success! Channel token: {token}")
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.text else {},
                "channel_token": token
            }
        else:
            print(f"Error: {response.status_code}")
            return {
                "success": False,
                "status_code": response.status_code,
                "response": response.text,
                "channel_token": token
            }
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "channel_token": token
        }

# Example usage
if __name__ == "__main__":
    # Example payload
    message = "Hello World!"
    
    # Send the payload
    result = send_payload(message)
    print(json.dumps(result, indent=2))
    
    # You can also specify a custom channel token if needed
    # custom_token = "my_special_token_123"
    # result = send_payload("Custom token example", channel_token=custom_token)