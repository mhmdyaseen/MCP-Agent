from abc import ABC,abstractmethod
from dataclasses import dataclass,field
from typing import Sequence
from uuid import uuid4

@dataclass
class Document:
    id:str=field(default_factory=lambda: str(uuid4()))
    content:str=field(default_factory=str)
    metadata:dict=field(default_factory=dict)

class BaseVectorStore(ABC):
    @abstractmethod
    def create_collection(self,collection_name:str)->None:
        pass

    @abstractmethod
    def insert(self,documents:list[Document])->None:
        pass

    @abstractmethod
    def search(self,query:str,k:int)->list[Document]:
        pass

    @abstractmethod
    def delete(self,collection_name:str)->None:
        pass

    @abstractmethod
    def update(self,document:Document)->None:
        pass

    @abstractmethod
    def delete_collection(self,collection_name:str)->None:
        pass

    @abstractmethod
    def get(self,id:str)->Document:
        pass

    @abstractmethod
    def all(self)->list[Document]:
        pass

    @abstractmethod
    def all_collections(self)->Sequence:
        pass

