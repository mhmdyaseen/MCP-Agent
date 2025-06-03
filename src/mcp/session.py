from mcp.types import Tool,Prompt,Resource,CallToolResult,ReadResourceResult,GetPromptResult
from src.mcp.transport.base import BaseTransport
from typing import Optional,List,Any

class MCPSession:
    '''
    Session for the MCP server

    This class provides an isolated interface for connecting, disconnecting, exploring tools, resources, prompts
    '''
    def __init__(self,transport:BaseTransport):
        self.transport=transport
        self.tools:Optional[List[Tool]]=None
        self.resources:Optional[List[Resource]]=None
        self.prompts:Optional[List[Prompt]]=None

    async def connect(self):
        '''
        Connect to the MCP server
        '''
        if not self.transport.is_connected:
            await self.transport.connect()
    
    async def disconnect(self):
        '''
        Disconnect from the MCP server
        '''
        if self.transport.is_connected:
            await self.transport.disconnect()

    async def initialize(self)->None:
        '''
        Initialize the MCP session to authenticate and discover tools, resources and prompts
        '''
        if not self.transport.is_connected:
            await self.connect()
        # Initialize the session
        initialize_result=await self.transport.initialize()
        server_capabilities=initialize_result.capabilities

        if server_capabilities.tools:
            # Get available tools
            tool_result=await self.transport.client_session.list_tools()
            self.tools=tool_result.tools or []
        else:
            self.tools=[]

        if server_capabilities.resources:
            # Get available resources
            resource_result=await self.transport.client_session.list_resources()
            self.resources=resource_result.resources or []
        else:
            self.resources=[]

        if server_capabilities.prompts:
            # Get available prompts
            prompt_result=await self.transport.client_session.list_prompts()
            self.prompts=prompt_result.prompts or []
        else:
            self.prompts=[]

    def list_tools(self)->List[Tool]:
        '''
        List the tools available in the MCP server
        '''
        return self.tools
    
    def list_resources(self)->List[Resource]:
        '''
        List the resources available in the MCP server
        '''
        return self.resources
    
    def list_prompts(self)->List[Prompt]:
        '''
        List the prompts available in the MCP server
        '''
        return self.prompts
    
    async def call_tool(self,name:str,arguments:dict[str,Any])->CallToolResult:
        '''
        Call a tool from the MCP server

        Args:
            name: The name of the tool to call
            arguments: The arguments to pass to the tool
        '''
        tool_result=await self.transport.client_session.call_tool(name=name,arguments=arguments)
        return tool_result
    
    async def read_resource(self,uri:str)->ReadResourceResult:
        '''
        Read a resource from the MCP server

        Args:
            uri: The URI of the resource to read
        '''
        resource_result=await self.transport.client_session.read_resource(uri=uri)
        return resource_result
    
    async def get_prompt(self,name:str,arguments:Optional[dict[str,Any]]=None)->GetPromptResult:
        '''
        Get a prompt from the MCP server

        Args:
            name: The name of the prompt to get
            arguments: The arguments to pass to the prompt
        '''
        prompt_result=await self.transport.client_session.get_prompt(name=name,arguments=arguments)
        return prompt_result
    

        
        
        

