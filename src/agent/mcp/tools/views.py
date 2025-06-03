from pydantic import BaseModel,Field
from typing import Literal

class SharedBaseModel(BaseModel):
    class Config:
        extra = 'allow'

class Done(SharedBaseModel):
    answer:str = Field(...,description="the detailed final answer to the user query in proper markdown format",examples=["The task is completed successfully."])

class Download(SharedBaseModel):
    server_name:str = Field(...,description="the name of the MCP server to install",examples=["server-456-mcp"])

class Read(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to read from",examples=["server1-123-mcp"])

class Shell(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to execute the shell on",examples=["server1-mcp"])
    command:str = Field(...,description="the command to execute in the shell",examples=["pwd"])

class Install(SharedBaseModel):
    server_name:str=Field(...,description="the name of the server",examples=["server1-mcp"])
    command:str=Field(...,description="the command to install the server",examples=["npx","uvx","python"])
    args:list[str]=Field(...,description="the arguments to pass to the server",examples=[["--directory","./mcp_servers/server1","run","main.py"]])
    env:dict[str,str]=Field(description="the environment variables to pass to the server",default={},examples=[{"key":"value"}])

class Uninstall(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to uninstall",examples=["server1-mcp"])

class Service(SharedBaseModel):
    pass

class Connect(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to connect to",examples=["server1-mcp"])

class Disconnect(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to disconnect from",examples=["server1-mcp"])

class Explore(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to explore",examples=["server1-mcp"])

class Execute(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to execute the tool on",examples=["server1-mcp"])
    tool_name:str = Field(...,description="the name of the tool to execute",examples=["tool1"])
    params:dict = Field(...,description="the parameters to pass to the tool",examples=[{"param1":"value1","param2":"value2"}])

class Resource(SharedBaseModel):
    server_name:str = Field(...,description="the name of the server to read the resource from",examples=["server1-mcp"])
    resource_uri:str = Field(...,description="the uri of the resource to read",examples=["https://example.com/resource1"])