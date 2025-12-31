import sys
import os
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append("d:\\workspace\\Murphy\\cometchat-webhook-service")

# Set mock env vars BEFORE importing app modules
os.environ["COMETCHAT_AUTH_KEY"] = "mock_auth_key"
os.environ["COMETCHAT_AUTH_SECRET"] = "mock_auth_secret"
# Also need these to avoid validation errors
os.environ["COMETCHAT_APP_ID"] = "mock_app_id"
os.environ["COMETCHAT_API_KEY"] = "mock_api_key"

try:
    from app.main import app
    from app.core.config import get_settings
    
    # Mock settings since we might not have the env vars set
    # But wait, we modified the settings class, so we might need to patch it
    # For now, let's just see if we can instantiate the app and client
    
    print("Successfully imported app")
    
    client = TestClient(app)
    
    # Check if the apps endpoint is registered
    response = client.get("/openapi.json")
    if response.status_code == 200:
        schema = response.json()
        paths = schema.get("paths", {})
        if "/api/v1/apps" in paths:
            print("SUCCESS: /api/v1/apps endpoint found in OpenAPI schema")
        else:
            print("FAILURE: /api/v1/apps endpoint NOT found in OpenAPI schema")
            sys.exit(1)
            
    print("Verification script completed successfully")

except Exception as e:
    print(f"FAILURE: An error occurred: {e}")
    sys.exit(1)
