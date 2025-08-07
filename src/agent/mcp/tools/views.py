from pydantic import BaseModel,Field
from typing import Literal

class SharedBaseModel(BaseModel):
    class Config:
        extra = 'allow'

class Done(SharedBaseModel):
    answer:str = Field(...,description="the detailed final answer to the user query in proper markdown format",examples=["The task is completed successfully."])

class Connect(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to connect to",examples=["abc-mcp"])

class Disconnect(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to disconnect from",examples=["ucd-mcp"])

class Discovery(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to discover tools and resources from",examples=["abc-mcp"])

class Execute(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to execute the tool on",examples=["mno-mcp","pqr-mcp"])
    tool_name:str = Field(...,description="the name of the tool to execute",examples=["abc_tool","xyz_tool"])
    params:dict = Field(...,description="the parameters to pass to the tool",examples=[{"param1":"value1","param2":"value2"},{"param1":"value1"}])

class Resource(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to read the resource from",examples=["abc-mcp"])
    resource_uri:str = Field(...,description="the uri of the resource to read",examples=["https://example.com/resource1"])