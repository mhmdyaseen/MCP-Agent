from src.mcp.connection.base import BaseConnection
from mcp.client.sse import sse_client
from typing import Any,Optional


class SSEConnection(BaseConnection):
    '''
    Connection for the SSE based MCP connections.

    This class handles the proper task isolation for SSE based connections.
    '''
    def __init__(self,url:str,headers:Optional[dict[str,str]]=None,timeout:float=5,sse_read_timeout:float=5*60):
        '''
        Initialize the SSE connection

        Args:
            url: The SSE endpoint URL
            headers: The headers to pass
            timeout: The timeout for the SSE connection
            sse_read_timeout: The timeout for the SSE read operation
        '''
        super().__init__()
        self.url=url
        self.headers=headers or {}
        self.timeout=timeout
        self.sse_read_timeout=sse_read_timeout
        self.sse_context=None

    async def establish_connection(self)->tuple[Any,Any]:
        '''
        Establish a SSE connection.

        Returns:
            A tuple of (read_stream,write_stream)

        Raises:
            Exception: If the connection could not be established
        '''
        # Create the SSE context
        self.sse_context= sse_client(self.url,headers=self.headers,timeout=self.timeout,sse_read_timeout=self.sse_read_timeout)

        # Enter the context manager
        read_stream,write_stream=await self.sse_context.__aenter__()
        return read_stream,write_stream
    
    async def close_connection(self)->None:
        if self.sse_context:
            try:
                await self.sse_context.__aexit__(None,None,None)
            except Exception as e:
                print(f'Error while closing the SSE connection: {e}')
            finally:
                self.sse_context=None
            