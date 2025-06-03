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