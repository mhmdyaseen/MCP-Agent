from typing import Any,Dict

def is_stdio_transport(server_config: Dict[str,Any])->bool:
    '''
    Check if the server configuration is for a stdio transport

    Args:
        server_config: The server configuration

    Returns:
        True if the server configuration is for a stdio transport, False otherwise
    '''
    return 'command' in server_config and 'args' in server_config


def is_sse_transport(server_config: Dict[str,Any])->bool:
    '''
    Check if the server configuration is for a sse transport

    Args:
        server_config: The server configuration

    Returns:
        True if the server configuration is for a sse transport, False otherwise
    '''
    return 'url' in server_config