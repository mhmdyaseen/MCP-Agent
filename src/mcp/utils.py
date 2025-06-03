from src.mcp.transport.utils import is_sse_transport,is_stdio_transport
from src.mcp.transport.stdio import StdioTransport
from src.mcp.transport.base import BaseTransport
from src.mcp.transport.sse import SSETransport
from typing import Any

def create_transport_from_server_config(server_config:dict[str,Any])->BaseTransport:
    '''
    Create a transport based on the server configuration

    Args:
        server_config: The server configuration

    Returns:
        The transport instance for the server
    '''
    if is_sse_transport(server_config):
        return SSETransport(**server_config)
    if is_stdio_transport(server_config):
        return StdioTransport(**server_config)
    raise ValueError(f'Invalid server configuration: {server_config}')
    