from src.mcp.utils import create_transport_from_server_config
from src.mcp.session import MCPSession
from typing import Any
import json

class MCPClient:
    '''
    Client for managing MCP servers.

    This class provides a unified interface for working with MCP servers,
    handling the configuration, connection creation and session management.
    '''

    def __init__(self,config:dict[str,dict[str,Any]]={}):
        self.config=config
        self.sessions:dict[str,MCPSession]={}

    @classmethod
    def from_config_file(cls,config_path:str)->'MCPClient':
        '''Create a MCPClient instance from a JSON file'''
        with open(config_path,'r') as f:
            config=json.load(f)
        return cls(config=config)
    
    @classmethod
    def from_config(cls,config:dict[str,Any])->'MCPClient':
        '''Create a MCPClient instance from a dictionary'''
        return cls(config=config)
    
    def get_server_names(self)->list[str]:
        '''Get the names of all configured MCP servers'''
        return list(self.config.get('mcpServers').keys())
    
    def add_server(self,name:str,server_config:dict[str,Any])->None:
        '''Add a new MCP server to the client'''
        if self.config.get('mcpServers') is None:
            self.config['mcpServers']={}
        self.config['mcpServers'][name]=server_config

    def remove_server(self,name:str)->None:
        '''Remove a MCP server from the client'''
        if name in self.sessions:
            pass
        del self.config['mcpServers'][name]

    def save_config(self,config_path:str)->None:
        '''Save the client configuration to a JSON file'''
        with open(config_path,'w') as f:
            json.dump(self.config,f,indent=4)

    async def create_session(self,name:str)->MCPSession:
        '''
        Create a new session for the specified MCP server

        Args:
            name: The name of the MCP server to create a session for
        
        Returns:
            The session for the specified MCP server
        
        Raises:
            ValueError: If the specified MCP server is not found
        '''
        servers:dict[str,dict[str,Any]]=self.config.get('mcpServers')
        if not servers:
            raise ValueError('No MCP servers configured')
        if name not in servers:
            raise ValueError(f'MCP server {name} not found')
        
        server_config=servers.get(name)
        transport=create_transport_from_server_config(server_config)

        session=MCPSession(transport=transport)
        await session.initialize()
        self.sessions[name]=session
        return session
    
    def get_session(self,name:str)->MCPSession:
        '''Get the session for the specified MCP server'''
        if name not in self.sessions:
            raise ValueError(f'MCP server {name} not found')
        return self.sessions.get(name)
    
    async def close_session(self,name:str)->None:
        '''
        Close the session for the specified MCP server

        Args:
            name: The name of the MCP server to close the session for

        Raises:
            ValueError: If the specified MCP server is not found
        '''
        if name not in self.sessions:
            raise ValueError(f'MCP server {name} not found')
        session=self.sessions[name]
        try:
            await session.disconnect()
        except Exception as e:
            print(f'Error while disconnecting from the MCP server: {e}')
        finally:
            del self.sessions[name]

    async def create_all_sessions(self)->None:
        '''
        Create sessions for all configured MCP servers
        '''
        servers:dict[str,dict[str,Any]]=self.config.get('mcpServers')
        if not servers:
            raise ValueError('No MCP servers configured')
        for name in servers:
            await self.create_session(name=name)

    async def close_all_sessions(self)->None:
        '''
        Close all sessions for all configured MCP servers
        '''
        for name in self.sessions:
            await self.close_session(name=name)
        