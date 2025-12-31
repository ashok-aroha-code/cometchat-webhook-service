"""Test database operations"""
from app.core.database import SessionLocal
from app.models.tenant import Tenant
from app.core.init_db import init_db

# Initialize database
init_db()

# Create session
db = SessionLocal()

# Create test tenant
tenant = Tenant(
    user_first_name="John",
    user_last_name="Doe",
    user_email="john.doe@example.com",
    user_phone="+1234567890",
    cometchat_app_id="123456789abc",
    cometchat_api_key="test_api_key",
    cometchat_region="us",
    metadata={"company": "Acme Corp"}
)

db.add(tenant)
db.commit()
db.refresh(tenant)

print(f"Created tenant with user_id: {tenant.user_id}")
print(f"Full name: {tenant.full_name}")
print(f"Email: {tenant.user_email}")

# Query tenant
queried = db.query(Tenant).filter(Tenant.user_email == "john.doe@example.com").first()
print(f"\nQueried tenant: {queried}")

db.close()
