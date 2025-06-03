from typing import TypedDict,Annotated
from src.message import BaseMessage
from operator import add
from pydantic import BaseModel

class State(TypedDict):
    input:str
    agent_data:dict[str,str]
    messages:Annotated[list[BaseMessage],add]
    output:str