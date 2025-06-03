<div align="center">

  <h1>🎮 MCP Agent</h1>

  <a href="https://github.com/Jeomon/MCP-Agent/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Cross%20Platform-blue" alt="Platform">
  <img src="https://img.shields.io/github/last-commit/Jeomon/MCP-Agent" alt="Last Commit">
  <br>
  <a href="https://x.com/CursorTouch">
    <img src="https://img.shields.io/badge/follow-%40CursorTouch-1DA1F2?logo=twitter&style=flat" alt="Follow on Twitter">
  </a>
  <a href="https://discord.com/invite/Aue9Yj2VzS">
    <img src="https://img.shields.io/badge/Join%20on-Discord-5865F2?logo=discord&logoColor=white&style=flat" alt="Join us on Discord">
  </a>

</div>

<br>

**MCP Agent** is a dynamic AI integration tool that can **discover, download, and connect** to any Model Context Protocol (MCP) server. Once connected, the agent can inspect all available tools, prompts, and resources, execute them autonomously, and seamlessly switch between multiple MCP servers.

## ✨ Key Capabilities

- **Autonomous MCP Server Discovery & Connection**  
  The agent can identify MCP servers listed on GitHub, clone them locally, and install necessary dependencies.

- **Self-Directed Interaction with MCP Tools**  
  Reads and executes any available tools and resources provided by the connected MCP server, without requiring manual intervention.

- **Multi-Server Navigation**  
  Connects and disconnects from multiple MCP servers on-demand, giving agent the ability to utilize various capabilities across different environments.

## 📃 Example

**Prompt** Install EXA-MCP

```plaintext
Enter a task: install exa-mcp
Entering MCP Agent
Thought: The user wants to install the 'exa-mcp' server. According to the installation guidelines, the first step is to download the server. I will use the Download Tool for this purpose.
Action Name: Download Tool
Action Input: {"server_name": "exa-mcp"}
Observation: Downloaded exa-mcp from https://github.com/exa-labs/exa-mcp-server.git and saved to D:\Personal Projects\MCP Agent\mcp_servers\exa-mcp.
Thought: I have downloaded the 'exa-mcp' server. The next step according to the installation guidelines is to read and understand the installation and configuration from the README.md file. I will use the Read Tool for this.
Action Name: Read Tool
Action Input: {"server_name": "exa-mcp"}
Observation: # Exa MCP Server 🔍 [![npm version](https://badge.fury.io/js/exa-mcp-server.svg)](https://www.npmjs.com/package/exa-mcp-server) [![smithery badge](https://smithery.ai/badge/exa)](https://smithery.ai/server/exa) A Model Context Protocol (MCP) server lets AI assistants like Claude use the Exa AI Search API for web searches. This setup allows AI models to get real-time web information in a safe and controlled way. ## Remote Exa MCP 🌐 Connect directly to Exa's hosted MCP server (instead of [...]
Thought: None
Action Name: Shell Tool
Action Input: {"server_name": "exa-mcp", "command": "npm install -g exa-mcp-server"}
Observation: changed 116 packages in 5s 22 packages are looking for funding run `npm fund` for details
Thought: I have downloaded and read the installation instructions for 'exa-mcp'. I have also executed the `npm install -g exa-mcp-server` command as suggested in the README. The next step is to install the server by updating the `config.json` file. The README provides a JSON configuration snippet for Claude Desktop. I need to adapt this for the MCP Agent's `Install Tool`. The `Install Tool` requires `server_name`, `command`, `args`, and `env`. Based on the README, the command is `npx`, the args are `["-y", "exa-mcp-server"]`, and the env should include the `EXA_API_KEY`. I will use a placeholder for the API key as I don't have the user's actual key. The user will need to replace this placeholder with their key after the installation is complete. I will also include the `--tools` argument to enable all tools as shown in the README example, as this seems like a reasonable default.
Action Name: Install Tool
Action Input: {"server_name": "exa-mcp", "command": "npx", "args": ["-y", "exa-mcp-server", "--tools=web_search_exa,research_paper_search,company_research,crawling,competitor_finder,linkedin_search,wikipedia_search_exa,github_search"], "env": {"EXA_API_KEY": "YOUR_EXA_API_KEY_HERE"}}
Observation: Installed exa-mcp successfully.
Thought: I have successfully downloaded, read the instructions, executed the necessary shell command, and installed the 'exa-mcp' server using the `Install Tool`. The installation process is complete according to the guidelines. I should now inform the user that the task is finished and provide the necessary information regarding the API key.
Final Answer: The 'exa-mcp' server has been successfully installed. 

Please note that you need to replace `YOUR_EXA_API_KEY_HERE` with your actual Exa API key in the `config.json` file for the server to function correctly. You can obtain your API key from [dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys).
```

>**NOTE:** API Key for EXA MCP to be provided manually on the `config.json`

**Prompt** Todays top AI updates (using EXA-MCP for web search)

```plaintext
Enter a task: Todays top AI updates
Entering MCP Agent
Thought: The user wants to get the top AI updates. I need to find a server that can provide this information. The first step is to list the available MCP servers to see which ones are available.
Action Name: Service Tool
Action Input: {}
Observation: exa-mcp
Thought: I attempted to explore the 'exa-mcp' server but received a message that it is not connected. According to the guidelines, I must connect to a server before exploring its tools. Therefore, I need to connect to the 'exa-mcp' server first.
Action Name: Connect Tool
Action Input: {"server_name": "exa-mcp"}
Observation: Server exa-mcp now connected.
Thought: I have successfully connected to the 'exa-mcp' server. Now that I am connected, I can explore the tools available on this server to find one that can provide the top AI updates as requested by the user.
Action Name: Explore Tool
Action Input: {"server_name": "exa-mcp"}
Observation: Tools available in exa-mcp: - Tool Name: web_search_exa - Tool Description: Search the web using Exa AI - performs real-time web searches and can scrape content from specific URLs. Supports configurable result counts and returns the content from the most relevant websites. - Tool Parameters: { "type": "object", "properties": { "query": { "type": "string", "description": "Search query" }, "numResults": { "type": "number", "description": "Number of search results to return (default: 5)" } }, [...]
Thought: The 'web_search_exa' tool is suitable for finding the top AI updates. I will use this tool with a query related to today's AI news. I will set the number of results to a reasonable number to get a good overview.
Action Name: Execute Tool
Action Input: {"server_name": "exa-mcp", "tool_name": "web_search_exa", "params": {"query": "today's top AI updates", "numResults": 5}}
Observation: { "requestId": "fdf1af53f21ccd1b98a79223f3bebf32", "autopromptString": "today's top AI updates", "autoDate": "2025-06-01T00:00:00.000Z", "resolvedSearchType": "neural", "results": [ { "id": "https://www.linkedin.com/news/story/google-debuts-new-ai-app-7381506/", "title": "Google debuts new AI app", "url": "https://www.linkedin.com/news/story/google-debuts-new-ai-app-7381506/", "publishedDate": "2025-06-02T14:05:14.000Z", "author": "Megan McDonough", "score": 0.41140973567962646, "text": [...]
Thought: None
Action Name: Disconnect Tool
Action Input: {"server_name": "exa-mcp"}
Error while closing the session: Attempted to exit cancel scope in a different task than it was entered in
Disconnected from the MCP server
Observation: Server exa-mcp now disconnected.
Thought: I have successfully retrieved the top AI updates using the 'web_search_exa' tool and disconnected from the server as requested. I can now provide the summarized information to the user and mark the task as complete.
Final Answer: Here are some of today's top AI updates:

*   **Google Debuts New AI App (AI Edge Gallery):** Google has released an experimental Android app that allows users to run open-source AI models directly on their smartphones without an internet connection. This app, powered by the phone's built-in processor, aims to provide developers with more AI capabilities while keeping data private. It supports various tasks like image analysis, text generation, and coding assistance, running models like Gemma 3 locally.

*   **OpenAI's Plans for ChatGPT:** OpenAI reportedly aims to transform ChatGPT into a "super assistant" that deeply understands users and acts as their interface to the internet. Documents suggest plans for ChatGPT to handle a wide range of tasks, from answering questions and managing schedules to assisting with complex research queries. This aligns with potential future hardware projects from OpenAI.

*   **Elon Musk's xAI Reportedly Seeks Funding:** Elon Musk's AI startup, xAI, is reportedly looking to raise $300 million in a tender offer, which would value the company at $113 billion. This follows xAI's acquisition of X and is expected to precede a larger investment round.
```

---

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Jeomon/MCP-Agent.git
cd MCP-Agent
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MCP Config

Create a `./mcp_servers/config.json` file in the project root:

```json
{
  "mcp_servers": {
    // server config
  }
}
```

### 4. Run the Agent

```bash
python app.py
```

---

## 🪪 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions, ideas, and pull requests are welcome! Check out the [CONTRIBUTING](CONTRIBUTING.md) guide for more info.
