from src.mcp.connection.base import BaseConnection
from mcp.types import InitializeResult
from abc import ABC,abstractmethod
from typing import Optional,Any
from mcp import ClientSession

class BaseTransport(ABC):
    def __init__(self):
        self.client_session:Optional[ClientSession]=None
        self.connection:Optional[BaseConnection]=None
        self.is_connected:bool=False

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self,exc_type,exc_value,traceback):
        await self.disconnect()

    @abstractmethod
    async def connect(self):
        '''Establish the connection to the MCP server'''
        pass

    async def disconnect(self):
        '''Close the connection to the MCP server'''
        if not self.is_connected:
            print('Not connected to the MCP server')
            return None
        await self.cleanup()
        self.is_connected=False
        print('Disconnected from the MCP server')
    
    async def cleanup(self):
        '''
        Cleanup the connection
        '''
        if self.client_session:
            try:
                await self.client_session.__aexit__(None,None,None)
            except Exception as e:
                print(f'Error while closing the session: {e}')
            finally:
                self.client_session=None
        if self.connection:
            try:
                await self.connection.stop()
            except Exception as e:
                print(f'Error while stopping the connection: {e}')
            finally:
                self.connection=None

    async def initialize(self)->InitializeResult:
        if not self.client_session:
            raise RuntimeError('Unable to initialize the transport without a client session')
        # Initialize the session
        return await self.client_session.initialize()
        