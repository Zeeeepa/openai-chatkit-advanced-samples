#!/bin/bash

# Voice Automation Platform - Setup Script
# Automated installation for Unix-like systems (Linux, macOS)

set -e  # Exit on error

echo "=================================="
echo "Voice Automation Platform Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Check Node.js version
echo -e "${YELLOW}Checking Node.js version...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18 or higher.${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo "Backend Setup"
echo "=================================="
echo ""

# Create Python virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
cd backend
python3 -m venv venv
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env and add your OPENAI_API_KEY${NC}"
fi

cd ..

echo ""
echo "=================================="
echo "Frontend Setup"
echo "=================================="
echo ""

# Install Node.js dependencies
echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
cd frontend
npm install
echo -e "${GREEN}✓ Node.js dependencies installed${NC}"

# Create .env.local file if it doesn't exist
if [ ! -f .env.local ]; then
    echo -e "${YELLOW}Creating .env.local file from template...${NC}"
    cp .env.example .env.local
    echo -e "${GREEN}✓ .env.local created${NC}"
fi

cd ..

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo ""
echo "1. Edit backend/.env and add your OPENAI_API_KEY"
echo ""
echo "2. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo -e "${YELLOW}Tip: Use './dev-start.sh' to start both servers at once!${NC}"
echo ""

