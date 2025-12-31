from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class RoleCreateRequest(BaseModel):
    role: str = Field(..., description="The unique identifier for the role")
    name: str = Field(..., description="The name of the role")
    description: Optional[str] = Field(None, description="Description of the role")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    settings: Optional[Dict[str, Any]] = Field(None, description="Role settings")

class RoleResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]

