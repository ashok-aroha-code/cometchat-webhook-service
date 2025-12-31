from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class AppCreateRequest(BaseModel):
    name: str = Field(..., description="The name of the app")
    region: str = Field("us", description="The region for the app (us or eu)")
    case_sensitive: bool = Field(True, alias="caseSensitive", description="Enable case sensitivity")
    
class AppResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]
