from pydantic import BaseModel

class ResourceRequest(BaseModel):
    resource_type: str
    resource_name: str
    environment: str
    iac_tool: str