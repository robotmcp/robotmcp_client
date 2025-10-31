#!/usr/bin/env bash
# Minimal cross-OS setup for ROS-MCP Client (custom MCP client service)
set -e

echo "ROS-MCP Client Setup"
echo "===================="

# Detect OS
OS="$(uname -s)"
case "$OS" in
  Linux*)   PLATFORM=linux ;;
  Darwin*)  PLATFORM=mac   ;;
  CYGWIN*|MINGW*) PLATFORM=windows ;;
  *) echo "Unsupported OS: $OS" ; exit 1 ;;
esac

echo "Detected OS: $PLATFORM"

# Ensure Python 3.10+
ensure_python() {
  case "$PLATFORM" in
    mac)
      if ! command -v python3 >/dev/null 2>&1; then
        if command -v brew >/dev/null 2>&1; then
          echo "Installing Python via Homebrew..."
          brew install python@3.11 || brew install python@3.12
        else
          echo "Install Python 3.10+ from https://www.python.org/downloads/"
        fi
      fi
      ;;
    linux)
      if ! command -v python3 >/dev/null 2>&1; then
        if command -v apt-get >/dev/null 2>&1; then
          sudo apt-get update -qq
          sudo apt-get install -y -qq python3 python3-venv python3-dev
        elif command -v yum >/dev/null 2>&1; then
          sudo yum install -y python3 python3-devel
        elif command -v pacman >/dev/null 2>&1; then
          sudo pacman -S --noconfirm python python-virtualenv
        else
          echo "Install Python 3.10+ using your package manager"
        fi
      fi
      ;;
    windows)
      if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
        echo "Install Python 3.10+ from https://www.python.org/downloads/ and add to PATH"
      fi
      ;;
  esac
}

# Ensure uv
ensure_uv() {
  if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv (pipx or pip)..."
    if command -v pipx >/dev/null 2>&1; then
      pipx install uv || true
    elif command -v python3 >/dev/null 2>&1; then
      python3 -m pip install --user uv || true
    else
      echo "pip/pipx not found. Install Python first."
    fi
  fi
}

ensure_python
ensure_uv

# Create project virtual environment with uv (no global installs)
if [ ! -d ".venv" ]; then
  echo "Creating project virtual environment (.venv) with uv..."
  uv venv .venv
else
  echo "Virtual environment .venv already exists."
fi

# Create .env if missing
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" << 'EOF'
# Required: Absolute path to ros-mcp-server folder (no quotes)
ROS_MCP_SERVER_PATH=
# Example: /Users/you/ROS-MCP/ros-mcp-server

# LLM provider selection (pick one):
# - gemini (google_genai:gemini-2.5-flash-lite)
# - openai (openai:gpt-4.1)
# - claude (anthropic:claude-sonnet-4-5)
# - llama (Cerebras: llama-3.3-70b)
# - qwen  (Cerebras: qwen-3-32b)
# - gpt-oss (Cerebras: gpt-oss-120b)
LLM_PROVIDER=gpt-oss

# API keys (provide only the key matching your chosen LLM_PROVIDER)
CEREBRAS_API_KEY=
# Get from: https://inference.cerebras.ai/
OPENAI_API_KEY=
# Get from: https://platform.openai.com/api-keys
ANTHROPIC_API_KEY=
# Get from: https://console.anthropic.com/account/keys
GOOGLE_API_KEY=
# Get from: https://aistudio.google.com/ (only for LLM_PROVIDER=gemini)
EOF
  echo ".env created. Fill in ROS_MCP_SERVER_PATH and API keys as needed."
else
  echo ".env already exists. Skipping creation."
fi

# Final notes (OS-specific)
echo
echo "Setup complete."
echo "- Edit .env and set ROS_MCP_SERVER_PATH to your absolute ros-mcp-server path."
echo "- Optionally set LLM_PROVIDER and corresponding API key."

case "$PLATFORM" in
  mac|linux)
    cat << EOF
Activate the virtual environment, then install deps and run:

  source .venv/bin/activate
  uv sync
  uv run clients/baseclient.py
EOF
    ;;
  windows)
    cat << EOF
Activate the virtual environment, then install deps and run (PowerShell):

  .\.venv\Scripts\Activate.ps1
  uv sync
  uv run clients\baseclient.py

Alternative for cmd.exe:
  .\.venv\Scripts\activate.bat
  uv sync
  uv run clients\baseclient.py
EOF
    ;;
esac
