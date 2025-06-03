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

**Prompt** Install Fetch-MCP

```plaintext
Enter a task: install fetch-mcp                                                                                                                         
Entering MCP Agent
Thought: The user wants to install the 'fetch-mcp' server. According to the installation guidelines, the first step is to download the server. I will use the Download Tool for this purpose.
Action Name: Download Tool
Action Input: {"server_name": "fetch-mcp"}
Observation: Downloaded fetch-mcp from https://github.com/zcaceres/fetch-mcp.git and saved to D:\Personal Projects\MCP Agent\mcp_servers\fetch-mcp.
Thought: I have downloaded the 'fetch-mcp' server. The next step according to the installation guidelines is to read and understand the installation and configuration from the README.md file. I will use the Read Tool to do this.
Action Name: Read Tool
Action Input: {"server_name": "fetch-mcp"}
Observation: # Fetch MCP Server ![fetch mcp logo](logo.jpg) This MCP server provides functionality to fetch web content in various formats, including HTML, JSON, plain text, and Markdown. <a href="https://glama.ai/mcp/servers/nu09wf23ao"> <img width="380" height="200" src="https://glama.ai/mcp/servers/nu09wf23ao/badge" alt="Fetch Server MCP server" /> </a> ## Components ### Tools - **fetch_html** - Fetch a website and return the content as HTML - Input: - `url` (string, required): URL of the website to [...]
Thought: I have read the README.md and the next steps are to install dependencies and build the server using npm commands. I will use the Shell Tool to execute `npm install` in the server's directory.
Action Name: Shell Tool
Action Input: {"server_name": "fetch-mcp", "command": "npm install"}
Observation: > fetch@1.0.0 prepare > npm run build > fetch@1.0.0 build > tsc && shx chmod +x dist/*.js added 439 packages, and audited 440 packages in 21s 61 packages are looking for funding run `npm fund` for details found 0 vulnerabilities
Thought: I have installed the dependencies and the build step was also executed as part of the `prepare` script during `npm install`. The next step according to the installation guidelines is to install the server by updating the config.json. I will use the Install Tool for this.
Action Name: Install Tool
Action Input: {"server_name": "fetch-mcp", "command": "node", "args": ["./dist/index.js"], "env": {}}
Observation: Installed fetch-mcp successfully.
Thought: I have successfully downloaded, read the instructions, installed dependencies, built the server, and installed it using the Install Tool. The task of installing fetch-mcp is now complete. I will use the Done Tool to indicate the completion and provide the final answer.
Final Answer: The fetch-mcp server has been successfully installed.
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
