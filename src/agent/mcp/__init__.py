from src.agent.mcp.tools import done_tool,execute_tool,discovery_tool,resource_tool,connect_tool,disconnect_tool
from src.agent.mcp.utils import extract_agent_data,read_markdown_file
from src.message import AIMessage,HumanMessage,SystemMessage
from langgraph.graph import StateGraph,END,START
from src.inference import BaseInference
from src.tool.registry import Registry
from src.agent.mcp.state import State
from src.mcp.client import MCPClient
from src.memory import BaseMemory
from src.agent import BaseAgent
from datetime import datetime
from termcolor import colored
from platform import platform
from textwrap import shorten
import json


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

tools=[
    execute_tool,discovery_tool,
    connect_tool,disconnect_tool,
    resource_tool
]

class MCPAgent(BaseAgent):
    def __init__(self,name:str='',instructions:list[str]=[],config_path:str='',memory:BaseMemory=None,llm:BaseInference=None,max_iteration=10,verbose=False):
        self.name='MCP Agent'
        self.description='The MCP Agent is capable of connecting to MCP servers and executing tools and resources to perform tasks.'
        
        self.system_prompt=read_markdown_file('./src/agent/mcp/prompt/system.md')
        self.action_prompt=read_markdown_file('./src/agent/mcp/prompt/action.md')
        self.observation_prompt=read_markdown_file('./src/agent/mcp/prompt/observation.md')
        self.answer_prompt=read_markdown_file('./src/agent/mcp/prompt/answer.md')
        
        self.instructions=self.get_instructions(instructions)
        self.llm=llm
        self.client=MCPClient.from_config_file(config_path)
        self.registry=Registry(tools+[done_tool])
        self.max_iteration=max_iteration
        self.iteration=0
        self.verbose=verbose
        self.memory=memory
        
        self.max_llm_retries = 3
        self.base_retry_delay = 1.0  # delay's in seconds
        self.max_retry_delay = 30.0  
        
        self.graph=self.create_graph()

    def get_instructions(self,instructions):
        return '\n'.join([f'{i+1}. {instruction}' for i,instruction in enumerate(instructions)])

    async def _retry_llm_invoke(self, messages, max_retries=None):
        if max_retries is None:
            max_retries = self.max_llm_retries
        
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                ai_message = await self.llm.async_invoke(messages=messages)
                return ai_message
                
            except Exception as e:
                last_exception = e
                
                if self.verbose:
                    print(colored(f'LLM invocation attempt {attempt + 1} failed: {str(e)}', color='yellow', attrs=['bold']))
                else:
                    logger.warning(f'LLM invocation attempt {attempt + 1} failed: {str(e)}')
                
                if attempt == max_retries - 1:
                    break
                
                delay = min(self.base_retry_delay * (2 ** attempt), self.max_retry_delay)
                
                if self.verbose:
                    print(colored(f'Retrying in {delay:.1f} seconds...', color='yellow'))
                
                await asyncio.sleep(delay)
        
        if self.verbose:
            print(colored(f'All {max_retries} LLM invocation attempts failed', color='red', attrs=['bold']))
        
        raise last_exception

    async def reason(self,state:State):
        mcp_servers=self.client.get_server_names_with_status()
        parameters={
            'name':self.name,
            'description':self.description,
            'instructions':self.instructions,
            'mcp_servers': '\n'.join([f'{name}: ({status})' for name,status in mcp_servers.items()]),
            'tools_prompt':self.registry.tools_prompt(),
            'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operating_system': platform(),
            'max_iteration':self.max_iteration
        }
        system_prompt=self.system_prompt.format(**parameters)
        human_prompt=f'Task: {state.get("input")}'
        messages=[SystemMessage(system_prompt),HumanMessage(human_prompt)]+state.get('messages')
        
        ai_message=await self._retry_llm_invoke(messages)
        
        agent_data=extract_agent_data(ai_message.content)
        thought=agent_data.get('Thought')
        if self.verbose:
            print(colored(f'Thought: {thought}',color='light_magenta',attrs=['bold']))
        return {**state,'messages':[ai_message],'agent_data':agent_data}

    async def action(self,state:State):
        agent_data=state.get('agent_data')
        thought=agent_data.get('Thought')
        action_name=agent_data.get('Action Name')
        action_input=agent_data.get('Action Input')
        if self.verbose:
            print(colored(f'Action Name: {action_name}',color='blue',attrs=['bold']))
            print(colored(f'Action Input: {json.dumps(action_input)}',color='blue',attrs=['bold']))
        action_result=await self.registry.async_execute(name=action_name,input=action_input,client=self.client)
        observation=action_result.content
        if self.verbose:
            print(colored(f'Observation: {shorten(observation,width=500)}',color='green',attrs=['bold']))
        state['messages'].pop()
        action_prompt=self.action_prompt.format(**{'thought':thought,'action_name':action_name,'action_input':json.dumps(action_input,indent=2)})
        observation_prompt=self.observation_prompt.format(**{'observation':observation,'iteration':self.iteration,'max_iteration':self.max_iteration})
        messages=[AIMessage(action_prompt),HumanMessage(observation_prompt)]
        return {**state,'messages':messages}

    async def answer(self,state:State):
        state['messages'].pop()
        if self.max_iteration>self.iteration:
            agent_data=state.get('agent_data')
            thought=agent_data.get('Thought')
            action_name=agent_data.get('Action Name')
            action_input=agent_data.get('Action Input')
            action_result=await self.registry.async_execute(action_name,action_input)
            final_answer=action_result.content
        else:
            thought='Looks like I have reached the maximum iteration limit reached.',
            action_name='Done Tool'
            action_input='{"answer":"Maximum Iteration reached."}'
            final_answer='Maximum Iteration reached.'
        answer_prompt=self.answer_prompt.format(**{
            'thought':thought,
            'final_answer':final_answer
        })
        messages=[AIMessage(answer_prompt)]
        if self.verbose:
            print(colored(f'Final Answer: {final_answer}',color='cyan',attrs=['bold']))
        return {**state,'output':final_answer,'messages':messages}

    def main_controller(self,state:State):
        if self.iteration<self.max_iteration:
            self.iteration+=1
            agent_data=state.get('agent_data')
            action_name=agent_data.get('Action Name')
            if action_name!='Done Tool':
                return 'action'
        return 'answer'

    def create_graph(self):
        workflow=StateGraph(State)

        workflow.add_node('reason',self.reason)
        workflow.add_node('action',self.action)
        workflow.add_node('answer',self.answer)

        workflow.add_edge(START,'reason')
        workflow.add_conditional_edges('reason',self.main_controller)
        workflow.add_edge('action','reason')
        workflow.add_edge('answer',END)

        return workflow.compile(debug=False)

    async def invoke(self,input:str=''):
        if self.verbose:
            print(f'Entering {self.name}')
        state={
            'input':input,
            'agent_data':{},
            'output':'',
            'messages':[]
        }
        response=await self.graph.ainvoke(state)
        if self.memory:
            self.memory.store(response.get('messages'))
        return response.get('output')

    def stream(self, input: str):
        if self.verbose:
            print(f'Entering {self.name}')
        state={
            'input':input,
            'agent_data':{},
            'output':'',
            'messages':[]
        }
        events=self.graph.stream(state)
        for event in events:
            for value in event.values():
                if value['output']:
                    yield value['output']
