from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters
from src.mcp.connection.stdio import StdioConnection
from src.mcp.transport.base import BaseTransport
from typing import Optional

class StdioTransport(BaseTransport):
    def __init__(self,command:str,args:Optional[list[str]]=None,env:Optional[dict[str,str]]=None):
        '''
        Initialize the stdio transport

        Args:
            command: The command to run
            args: The arguments to pass
            env: The environment variables to pass
        '''
        super().__init__()
        self.command=command
        self.args=args or []
        self.env=env or {}

    async def connect(self):
        '''
        Establish a connection to the MCP server
        '''
        if self.is_connected:
            print('Already connected to the MCP server')
            return None
        try:
            # Create the stdio connection
            server_params=StdioServerParameters(command=self.command,args=self.args,env=self.env)
            self.connection=StdioConnection(server_params=server_params)
            read_stream,write_stream=await self.connection.start()

            # Create the client session
            self.client_session=ClientSession(read_stream=read_stream,write_stream=write_stream)
            await self.client_session.__aenter__()
            self.is_connected=True
        except Exception as e:
            print(f'Error while connecting to the MCP server: {e}')
            # Cleanup if the connection could not be established
            await self.cleanup()
            raise
        

        