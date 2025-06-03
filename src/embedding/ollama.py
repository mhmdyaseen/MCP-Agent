from requests import RequestException,HTTPError,ConnectionError
from src.embedding import BaseEmbedding
from httpx import Client
from typing import Literal

class OllamaEmbedding(BaseEmbedding):
    def embed(self, text):
        url=self.base_url or f'http://localhost:11434/api/embed'
        headers=self.headers
        payload={
            'model':self.model,
            'input':text
        }
        try:
            with Client() as client:
                response=client.post(url=url,json=payload,headers=headers)
            response.raise_for_status()
            json_data=response.json()
            return json_data['embeddings'][0]
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)