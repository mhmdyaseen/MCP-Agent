from typing import TypedDict,Annotated
from src.message import BaseMessage
from operator import add

class State(TypedDict):
    input:str
    agent_data:dict[str,str]
    messages:Annotated[list[BaseMessage],add]
    output:str