from src.inference.gemini import ChatGemini
from src.agent.mcp import MCPAgent
from src.mcp.client import MCPClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
google_api_key=os.getenv('GOOGLE_API_KEY')

config_path=Path.cwd()/'mcp_servers'/'config.json'
client=MCPClient.from_config_file(config_path.as_posix())

llm=ChatGemini(model='gemini-2.5-flash-preview-04-17',api_key=google_api_key,temperature=0.2)
agent=MCPAgent(client=client,llm=llm,verbose=True,max_iteration=100)

input=input('Enter a task: ')

async def main():
    response=await agent.invoke(input=input)
    print(response)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())