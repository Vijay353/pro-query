#!/bin/bash
# Quick Start Script for AI Portfolio Backend
# Run this after copying all files to set everything up

set -e  # Exit on error

echo "======================================"
echo "AI Portfolio Backend - Quick Setup"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --quiet --upgrade pip
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --quiet -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Create .env from example
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠ .env file already exists (not overwriting)${NC}"
    echo ""
fi

# Check if Ollama is running
echo "Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
    
    # Check if llama3.2:3b is pulled
    if curl -s http://localhost:11434/api/tags | grep -q "llama3.2"; then
        echo -e "${GREEN}✓ llama3.2 model is available${NC}"
    else
        echo -e "${YELLOW}⚠ llama3.2 model not found${NC}"
        echo "  Pull it with: ollama pull llama3.2:3b"
    fi
else
    echo -e "${YELLOW}⚠ Ollama is not running${NC}"
    echo ""
    echo "To install Ollama:"
    echo "  Mac/Windows: https://ollama.ai/download"
    echo "  Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo ""
    echo "After installing, run:"
    echo "  ollama serve          # In one terminal"
    echo "  ollama pull llama3.2:3b   # In another terminal"
fi
echo ""

# Summary
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Make sure Ollama is running:"
echo "   ${GREEN}ollama serve${NC}"
echo ""
echo "2. Pull the model (if not already done):"
echo "   ${GREEN}ollama pull llama3.2:3b${NC}"
echo ""
echo "3. Start the backend:"
echo "   ${GREEN}source .venv/bin/activate${NC}  # If not already active"
echo "   ${GREEN}uvicorn main:app --reload --port 8000${NC}"
echo ""
echo "4. In your frontend folder, create .env:"
echo "   ${GREEN}echo 'VITE_API_BASE=http://localhost:8000' > .env${NC}"
echo ""
echo "5. Start your frontend:"
echo "   ${GREEN}npm run dev${NC}"
echo ""
echo "======================================"
echo ""
echo "Test the backend:"
echo "  ${GREEN}http://localhost:8000${NC}          - API info"
echo "  ${GREEN}http://localhost:8000/docs${NC}     - Interactive docs"
echo "  ${GREEN}http://localhost:8000/api/health${NC} - Health check"
echo ""
echo "======================================"