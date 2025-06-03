from mcp.client.stdio import stdio_client, StdioServerParameters
from src.mcp.connection.base import BaseConnection
from typing import Any

class StdioConnection(BaseConnection):
    '''
    Connection for the stdio based MCP connections.

    This class handles the proper task isolation for stdio based connections
    '''

    def __init__(self,server_params:StdioServerParameters):
        '''
        Initialize the stdio connection

        Args:
            server_params: The parameters for the stdio server
        '''
        super().__init__()
        self.server_params=server_params
        self.stdio_context=None

    async def establish_connection(self)->tuple[Any,Any]:
        '''
        Establish a stdio connection.

        Returns:
            A tuple of (read_stream,write_stream)

        Raises:
            Exception: If the connection could not be established
        '''
        # Create the stdio context
        self.stdio_context= stdio_client(self.server_params)
        # Enter the context manager
        read_stream,write_stream=await self.stdio_context.__aenter__()
        return read_stream,write_stream
    
    async def close_connection(self)->None:
        '''
        Close the stdio connection
        '''
        if self.stdio_context:
            try:
                await self.stdio_context.__aexit__(None,None,None)
            except Exception as e:
                print(f'Error while closing the stdio connection: {e}')
            finally:
                self.stdio_context=None
        
        
        



