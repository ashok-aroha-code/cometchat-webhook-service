import sys
import os
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append("d:\\workspace\\Murphy\\cometchat-webhook-service")

# Mock env vars
os.environ["COMETCHAT_APP_ID"] = "mock_app_id"
os.environ["COMETCHAT_API_KEY"] = "mock_api_key"
os.environ["COMETCHAT_AUTH_KEY"] = "mock_auth_key"
os.environ["COMETCHAT_AUTH_SECRET"] = "mock_auth_secret"

try:
    from app.main import app
    
    print("Successfully imported app")
    
    client = TestClient(app)
    
    # Check if the roles endpoint is registered
    response = client.get("/openapi.json")
    if response.status_code == 200:
        schema = response.json()
        paths = schema.get("paths", {})
        if "/api/v1/roles" in paths:
            print("SUCCESS: /api/v1/roles endpoint found in OpenAPI schema")
        else:
            print("FAILURE: /api/v1/roles endpoint NOT found in OpenAPI schema")
            sys.exit(1)
            
    print("Verification script completed successfully")

except Exception as e:
    print(f"FAILURE: An error occurred: {e}")
    sys.exit(1)
