from src.agent.mcp.tools.views import Done,Service,Explore,Connect,Disconnect,Resource,Execute,Download,Read,Install,Shell,Uninstall
from src.mcp.client import Client as MCPClient
from subprocess import run
from src.tool import Tool
from github import Github
from pathlib import Path
from git import Repo
import glob
import json
import os

@Tool('Done Tool',params=Done)
async def done_tool(answer:str,client:MCPClient=None):
    '''To indicate that the task is completed'''
    return answer

@Tool('Download Tool',params=Download)
async def download_tool(server_name:str,client:MCPClient=None):
    '''To Download the MCP server from Github'''
    def search_repo(server_name):
        github=Github()
        repo=github.search_repositories(server_name)[0]
        url=repo.git_url.replace('git://','https://')
        name=repo.name
        return url,name

    url,_=search_repo(server_name)
    to_path=Path.cwd()/'mcp_servers'/server_name
    Repo.clone_from(url=url,to_path=to_path)
    # os.chdir(to_path)
    return f'Downloaded {server_name} from {url} and saved to {to_path}.'

@Tool('Shell Tool',params=Shell)
async def shell_tool(server_name:str,command:str,client:MCPClient=None):
    '''To execute shell command inside the given MCP server folder'''
    os.chdir(Path.cwd()/'mcp_servers'/server_name)
    result=''
    try:
        process=run(command,shell=True,capture_output=True,check=True,text=True)
        if process.returncode==0:
            result=process.stdout.strip() or 'Command executed successfully.'
        else:
            result=f'Error: {process.stderr.strip()}'
    except Exception as e:
        result=f'Error: {e}'
    finally:
        os.chdir(Path.cwd().parent.parent)
    return result

@Tool('Install Tool',params=Install)
async def install_tool(server_name:str,command:str,args:list[str],env:dict[str,str]={},client:MCPClient=None):
    '''To install the MCP server and add it to the config.json file'''
    config_path=Path.cwd()/'mcp_servers/config.json'
    with open(config_path,'r+') as f:
        config:dict=json.load(f)
        if config.get('mcpServers') is None:
            config['mcpServers']={}
        servers=config.get('mcpServers')
        servers[server_name]={
            'command':command,
            'args':args,
            'env':env
        }
        f.seek(0)
        json.dump(config,f,indent=4)
        f.truncate()
    # os.chdir(Path(Path.cwd().parent.parent))
    return f'Installed {server_name} successfully.'

@Tool('Uninstall Tool',params=Uninstall)
async def uninstall_tool(server_name:str,client:MCPClient=None):
    '''To uninstall the MCP server and remove it from the config.json file'''
    config_path=Path.cwd()/'mcp_servers/config.json'
    mcpserver=Path.cwd()/'mcp_servers'/server_name.lower()
    if mcpserver.exists():
        mcpserver.rmdir()
    with open(config_path,'r+') as f:
        config:dict=json.load(f)
        if config.get('mcpServers') is None:
            config['mcpServers']={}
        servers=config.get('mcpServers')
        if server_name.removesuffix('-mcp') in servers:
            del servers[server_name]
        f.seek(0)
        json.dump(config,f,indent=4)
        f.truncate()
    return f'Uninstalled {server_name} successfully.'

@Tool('Read Tool',params=Read)
async def read_tool(server_name:str,client:MCPClient=None):
    '''To read and understand the installation and configuration of this MCP server'''
    def find_file(start_dir:Path,filename:str):
        pattern = os.path.join(start_dir, '**', filename)
        matches = glob.glob(pattern, recursive=True)
        return Path(matches[0]).as_posix() if matches else None
        
    def read_file(file_path):
        content = ''
        with open(file_path, 'r',encoding='utf-8') as f:
            content=f.read()
        return content
    
    server_path=Path.cwd()/'mcp_servers'/server_name
    file_path=find_file(server_path,'README.md')
    if file_path is None:
        return f'README.md file not found in {server_name}.'
    content=read_file(file_path)
    return content

@Tool('Service Tool',params=Service)
async def service_tool(client:MCPClient=None):
    '''List all the available MCP servers'''
    server_names=client.get_server_names()
    if not server_names:
        return 'No MCP servers available.'
    return '\n'.join(server_names)

@Tool('Connect Tool',params=Connect)
async def connect_tool(server_name:str,client:MCPClient=None):
    '''Connect to a MCP server to access its resources and tools'''
    if server_name in client.sessions:
        return f'Server {server_name} already connected.'
    session=await client.create_session(server_name)
    client.sessions[server_name]=session
    return f'Server {server_name} now connected.'

@Tool('Explore Tool',params=Explore)
async def explore_tool(server_name:str,client:MCPClient=None):
    '''To explore the tools and resources available inside a specific MCP server'''
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
    resources=await session.resources_list()
    if resources:
        prompt+=f'Resources available in {server_name}:\n'
        for resource in resources:
            prompt+=f'- Resource Name: {resource.name}\n'
            prompt+=f'- Resource Description: {resource.description}\n'
            prompt+=f'- Resource URI: {resource.uri}\n'
            prompt+='\n'
    return prompt

@Tool('Disconnect Tool',params=Disconnect)
async def disconnect_tool(server_name:str,client:MCPClient=None):
    '''Disconnect from a MCP server'''
    if server_name not in client.sessions:
        return f'Server {server_name} already disconnected.'
    await client.close_session(server_name)
    return f'Server {server_name} now disconnected.'

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
    content=tool_result.content[0]
    return content.get('text')

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
    content=resource_result.contents[0]
    return content.text