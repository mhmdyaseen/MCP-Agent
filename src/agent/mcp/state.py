from typing import TypedDict,Annotated,Any
from src.message import BaseMessage
from operator import add

class State(TypedDict):
    input:str
    agent_data:dict[str,Any]
    messages:Annotated[list[BaseMessage],add]
    output:str