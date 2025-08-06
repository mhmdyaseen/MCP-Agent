from src.agent.mcp.tools.views import Done,Discovery,Connect,Disconnect,Resource,Execute
from src.mcp.client import MCPClient
from src.tool import Tool

@Tool('Done Tool',params=Done)
async def done_tool(answer:str,client:MCPClient=None):
    '''To indicate that the task is completed'''
    return answer

@Tool('Connect Tool',params=Connect)
async def connect_tool(server_name:str,client:MCPClient=None):
    '''Connect to a specific MCP server'''
    if server_name in client.sessions:
        return f'Server {server_name} already connected.'
    session=await client.create_session(server_name)
    client.sessions[server_name]=session
    return f'Server {server_name} now connected.'

@Tool('Disconnect Tool',params=Disconnect)
async def disconnect_tool(server_name:str,client:MCPClient=None):
    '''Disconnect from a specific MCP server'''
    if server_name not in client.sessions:
        return f'Server {server_name} not connected.'
    await client.close_session(server_name)
    return f'Server {server_name} now disconnected.'

@Tool('Discovery Tool',params=Discovery)
async def discovery_tool(server_name:str,client:MCPClient=None):
    '''To discover the tools and resources available inside this specific MCP server'''
    if server_name not in client.sessions:
        return f'Server {server_name} not connected.'
    prompt=''
    session=client.get_session(server_name)
    tools=await session.tools_list()
    if tools:
        prompt+=f'Tools available in {server_name}:\n'
        for tool in tools:
            prompt+=f'- Tool Name: {tool.name}\n'
            prompt+=f'- Tool Description: {tool.description}\n'
            prompt+=f'- Tool Parameters: {tool.inputSchema.model_dump_json(indent=4)}\n'
            prompt+='\n'
    # resources=await session.resources_list()
    # if resources:
    #     prompt+=f'Resources available in {server_name}:\n'
    #     for resource in resources:
    #         prompt+=f'- Resource Name: {resource.name}\n'
    #         prompt+=f'- Resource Description: {resource.description}\n'
    #         prompt+=f'- Resource URI: {resource.uri}\n'
    #         prompt+='\n'
    return prompt

@Tool('Execute Tool',params=Execute)
async def execute_tool(server_name:str,tool_name:str,params:dict,client:MCPClient=None):
    '''Execute a tool from the currently connected MCP server'''
    if server_name not in client.sessions:
        return f'Server {server_name} not connected.'
    session= client.get_session(server_name)
    tools=await session.tools_list()
    if tool_name not in [tool.name for tool in tools]:
        return f'Tool {tool_name} not found in server {server_name}.'
    tool_result=await session.tools_call(tool_name,params)
    return tool_result.content[0].text

@Tool('Resource Tool',params=Resource)
async def resource_tool(server_name:str,resource_uri:str,client:MCPClient=None):
    '''Read a resource from the currently connected MCP server'''
    if server_name not in client.sessions:
        return f'Server {server_name} not connected.'
    session= client.get_session(server_name)
    resources=await session.resources_list()
    if resource_uri not in [resource.uri for resource in resources]:
        return f'Resource {resource_uri} not found in server {server_name}.'
    resource_result=await session.resources_read(resource_uri)
    return resource_result[0].text