# ROS MCP Client 🧠⇄🤖

![Static Badge](https://img.shields.io/badge/ROS-Available-green)
![Static Badge](https://img.shields.io/badge/ROS2-Available-green)
![Static Badge](https://img.shields.io/badge/License-Apache%202.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

<p align="center">
  <img src="https://github.com/robotmcp/ros-mcp-server/blob/main/docs/images/framework.png"/>
</p>

The **ROS MCP Client** is a reference implementation of a Model Context Protocol (MCP) client, designed to connect directly with [ros-mcp-server](https://github.com/robotmcp/ros-mcp-server/).

Instead of using a Desktop LLM client, it acts as a bridge that integrates an LLM, enabling natural-language interaction with any ROS or ROS2 robot.

## 🧠 What It Does

`ros-mcp-client` implements the LLM-side of the MCP protocol.

It can:
- Connect to a `ros-mcp-server` over MCP (stdio or HTTP).
- Send natural language queries or structured requests to the robot without the need to integrate it with a Desktop LLM client
- Stream back feedback, sensor data, or responses from the server.
- Integrate with a local LLM (Gemini, Ollama, Nvidia NeMo).

In short, it lets you run an MCP-compatible client that speaks to robots via the MCP interface — useful for testing, local reasoning, or autonomous AI controllers.

---

## ⚙️ Key Features of the ROS MCP Client

- Implements MCP client specification — plug-and-play with the ROS MCP server.

- ROS-aware LLM interface — specialized prompts and handlers for robotics tasks.

- Supports bidirectional streaming — send commands, receive real-time topic feedback.

- LLM integration ready — use Gemini, Anthropic, or Ollama APIs as reasoning engines.

- Offline-capable — works entirely within local or LAN environments.

---

## 

## 🛠 Getting Started  

The MCP client is version-agnostic (ROS1 or ROS2).  

<p align="center">
  <img src="https://github.com/robotmcp/ros-mcp-server/blob/main/docs/images/MCP_topology.png"/>
</p>  

### Prerequisites

- ROS or ROS2 running with `rosbridge`
- Active [`ros-mcp-server`](https://github.com/robotmcp/ros-mcp-server) instance

### Installation  

1. Clone the repository  
```bash
git clone https://github.com/robotmcp/ros-mcp-client.git
cd ros-mcp-client
```

2. Install dependencies
```bash
uv sync  # or pip install -e .
```

3. Minimal setup for custom MCP client
```bash
./setup.sh
# Then edit .env and set:
# - ROS_MCP_SERVER_PATH=/absolute/path/to/ros-mcp-server
# - LLM_PROVIDER=gpt-oss|openai|anthropic|ollama
```

4. Run the base client
```bash
uv run clients/baseclient.py
```

5. Follow the setup guide for the Gemini Live client:
   - **[Gemini Live Client](clients/gemini_live/README.md)** - Google Gemini integration

4. Start `rosbridge` on the target robot
```bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```  

---

## 📁 Project Structure

```
ros-mcp-client/
├── clients/
│   ├── gemini_live/          # Full-featured Gemini client
│   │   ├── gemini_client.py  # Main client script
│   │   ├── mcp.json          # MCP server configuration
│   │   ├── setup_gemini_client.sh  # Automated setup
│   │   └── README.md         # Detailed setup guide
├── config/                   # Shared configuration
├── scripts/                  # Utility scripts
├── pyproject.toml           # Python dependencies
└── README.md               # This file
```

---

## 📚 Available Clients  

The project includes a comprehensive LLM client implementation:

### 🤖 **Gemini Live Client** (`clients/gemini_live/`)
- **Full-featured** Google Gemini integration
- **Text-only mode** optimized for WSL
- **Real-time interaction** with ROS robots
- **Automated setup** with `setup_gemini_client.sh`

### 🚀 **Quick Start**
```bash
# Try the Gemini Live client
cd clients/gemini_live
./setup_gemini_client.sh
uv run gemini_client.py
```

We welcome community PRs with new client implementations and integrations!  

---

## 🤝 Contributing  

We love contributions of all kinds:  
- Bug fixes and documentation updates  
- New features (e.g., Action support, permissions)  
- Additional examples and tutorials  

Check out the [contributing guidelines](docs/contributing.md) and see issues tagged **good first issue** to get started.  

---

## 📜 License  


This project is licensed under the [Apache License 2.0](LICENSE).  
