from mcp.client.session import ClientSession
from src.mcp.connection.sse import SSEConnection    
from src.mcp.transport.base import BaseTransport
from typing import Optional

class SSETransport(BaseTransport):
    def __init__(self,url:str,auth_token:Optional[str]=None,headers:Optional[dict[str,str]]=None,customheaders:Optional[dict[str,str]]=None,timeout:float=5,sse_read_timeout:float=5*60):
        '''
        Initialize the SSE transport

        Args:
            url: The SSE endpoint URL
            headers: The headers to pass
            timeout: The timeout for the SSE connection
            sse_read_timeout: The timeout for the SSE read operation
        '''
        super().__init__()
        self.url=url
        self.headers=headers or {}
        if auth_token:
            self.headers['Authorization'] = f'Bearer {auth_token}'
        self.timeout=timeout
        self.sse_read_timeout=sse_read_timeout

    async def connect(self)->None:
        '''
        Establish a connection to the MCP server
        '''
        if self.is_connected:
            print('Already connected to the MCP server')
            return None
        try:
            # Create the SSE connection
            self.connection=SSEConnection(url=self.url,headers=self.headers,timeout=self.timeout,sse_read_timeout=self.sse_read_timeout)
            read_stream,write_stream=await self.connection.establish_connection()

            # Create the client session
            self.client_session=ClientSession(read_stream=read_stream,write_stream=write_stream)
            await self.client_session.__aenter__()
            self.is_connected=True
        except Exception as e:
            print(f'Error while connecting to the MCP server: {e}')
            # Cleanup if the connection could not be established
            await self.cleanup()
            raise