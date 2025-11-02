#!/usr/bin/env bash
# ROS MCP Client Setup Script
# Sets up the environment for the Gemini Live client

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_DIR="$SCRIPT_DIR"

echo "🔧 ROS MCP Client Setup"
echo "======================="
echo "📁 Client directory: $CLIENT_DIR"

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3-dev python3-venv

# Change to project root for dependency installation
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Install Python dependencies using uv
echo "🐍 Installing Python dependencies..."
if command -v uv &> /dev/null; then
    echo "Using uv for dependency management..."
    uv sync
else
    echo "uv not found, using pip..."
    pip install -e .
fi

# Create .env file in the client directory
ENV_FILE="$CLIENT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "📝 Creating .env template in $CLIENT_DIR..."
    cat > "$ENV_FILE" << EOF
# Google API Key for Gemini
# Get your API key from: https://aistudio.google.com/
GOOGLE_API_KEY=your_google_api_key_here
EOF
    echo "⚠️  Please edit $ENV_FILE and add your Google API key"
else
    echo "✅ .env file already exists in $CLIENT_DIR"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your Google API key to $ENV_FILE"
echo "2. Verify mcp_config.json points to your ros-mcp-server"
echo "3. Run: cd $CLIENT_DIR && uv run gemini_client.py"
echo ""
if [ "$IS_WSL" = true ]; then
    echo "💡 WSL Notes:"
    echo "- This client runs in text-only mode (no audio/video)"
    echo "- Use WSL paths in mcp_config.json (e.g., /mnt/c/Users/...)"
fi