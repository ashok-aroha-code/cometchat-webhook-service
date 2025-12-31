import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock env vars
os.environ["COMETCHAT_APP_ID"] = "mock_app_id"
os.environ["COMETCHAT_API_KEY"] = "mock_api_key"
os.environ["COMETCHAT_AUTH_KEY"] = "mock_auth_key"
os.environ["COMETCHAT_AUTH_SECRET"] = "mock_auth_secret"

try:
    from app.main import app
    
    client = TestClient(app)
    
    # Check if the roles endpoint is registered
    response = client.get("/openapi.json")
    if response.status_code == 200:
        schema = response.json()
        role_schema = schema.get("components", {}).get("schemas", {}).get("RoleCreateRequest", {})
        properties = role_schema.get("properties", {})
        
        # Check for 'role' field instead of 'uid'
        if "role" in properties and "uid" not in properties:
            print("SUCCESS: 'role' field found and 'uid' field absent")
        else:
            print(f"FAILURE: Fields mismatch. Properties: {properties.keys()}")
            sys.exit(1)
            
        # Check for 'settings' field
        if "settings" in properties:
            print("SUCCESS: 'settings' field found")
        else:
            print("FAILURE: 'settings' field NOT found")
            print("FAILURE: 'settings' field NOT found")
            sys.exit(1)

        # Verify the endpoint actually works (and logging doesn't crash it)
        print("Testing POST /api/v1/roles endpoint...")
        # Verify the endpoint actually works (and logging doesn't crash it)
        print("Testing POST /api/v1/roles endpoint...", file=sys.stderr)
        # Patch httpx.AsyncClient where it is used
        with patch("app.services.cometchat_client.httpx.AsyncClient") as mock_client_cls:
            mock_instance = AsyncMock()
            mock_client_cls.return_value = mock_instance
            mock_instance.__aenter__.return_value = mock_instance
            
            mock_response = AsyncMock()
            mock_response.status_code = 200
            # Mock json() method to return dict
            mock_response.json = lambda: {
                "data": {
                    "role": "test_role",
                    "name": "Test Role"
                }
            }
            # Make sure raise_for_status doesn't raise
            mock_response.raise_for_status = lambda: None
            
            mock_instance.post.return_value = mock_response
            
            payload = {
                "role": "test_role",
                "name": "Test Role", 
                "description": "Test Description"
            }
            
            print("Sending request...", file=sys.stderr)
            try:
                response = client.post("/api/v1/roles", json=payload)
                print(f"Response status: {response.status_code}", file=sys.stderr)
            except Exception as e:
                 print(f"Request raised exception: {e}", file=sys.stderr)
                 import traceback
                 traceback.print_exc()
                 sys.exit(1)
            
            if response.status_code == 201:
                print("SUCCESS: POST /api/v1/roles returned 201 Created", file=sys.stderr)
            else:
                print(f"FAILURE: POST /api/v1/roles returned {response.status_code}", file=sys.stderr)
                # print(response.json(), file=sys.stderr)
                sys.exit(1)

            
    print("Verification script completed successfully")

except Exception as e:
    print(f"FAILURE: An error occurred: {e}")
    sys.exit(1)
