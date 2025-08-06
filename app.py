# from src.inference.gemini import ChatGemini
from src.inference.groq import ChatGroq
from src.agent.mcp import MCPAgent
from dotenv import load_dotenv
import os

load_dotenv()

# llm=ChatGemini(model='gemini-2.0-flash',api_key=os.getenv('GOOGLE_API_KEY'),temperature=0)
llm=ChatGroq(model='openai/gpt-oss-120b',api_key=os.getenv("GROQ_API_KEY"),temperature=0)
agent=MCPAgent(config_path='./mcp_servers/config.json',llm=llm,verbose=True,max_iteration=100)

input=input('Enter a task: ')

async def main():
    response=await agent.invoke(input=input)
    print(response)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())