#!/bin/bash

# Script Name: install
# Description: TODO: Add description
# Author: charlesbrownroberts
# Date Created: 4/14/25
# Last Modified: 4/14/25

# Main code starts here
echo "Hello, this is a script template!"

# Add your script's logic here

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Whitelist of required commands and models
REQUIRED_COMMANDS=("python3" "pip3" "ollama")
REQUIRED_OLLAMA_MODELS=("llama3.2" "mxbai-embed-large")
REQUIRED_PYTHON="/opt/homebrew/bin/python3"
REQUIRED_PYTHON_VERSION="3.12"

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        exit 1
    fi
}

# Function to check if an Ollama model exists locally
check_ollama_model() {
    if ! ollama list | grep -q "$1"; then
        echo -e "${YELLOW}Ollama model '$1' not found. Pulling now...${NC}"
        ollama pull "$1"
    else
        echo -e "${GREEN}Ollama model '$1' is already available.${NC}"
    fi
}

# Check all required commands
echo "Checking prerequisites..."
for cmd in "${REQUIRED_COMMANDS[@]}"; do
    check_command "$cmd"
done

# Check Python version and path (only before venv is created)
if [ ! -d "venv" ]; then
    PYTHON_VERSION=$($REQUIRED_PYTHON --version 2>&1 | awk '{print $2}')
    PYTHON_PATH=$(which python3)
    if [[ "$PYTHON_PATH" != "$REQUIRED_PYTHON" ]]; then
        echo -e "${RED}Error: python3 is not Homebrew Python at $REQUIRED_PYTHON${NC}"
        echo -e "${YELLOW}Current python3 path: $PYTHON_PATH${NC}"
        echo -e "${YELLOW}Please run: brew install python${NC}"
        exit 1
    fi
    if [[ "$PYTHON_VERSION" != $REQUIRED_PYTHON_VERSION* ]]; then
        echo -e "${RED}Error: Python $REQUIRED_PYTHON_VERSION.x is required. Found $PYTHON_VERSION${NC}"
        exit 1
    fi
    echo -e "${GREEN}Using Homebrew Python: $PYTHON_PATH ($PYTHON_VERSION)${NC}"
else
    echo -e "${GREEN}Virtual environment already exists. Skipping Homebrew Python path check.${NC}"
fi

# Create and activate virtual environment
echo -e "\n${GREEN}Creating Python virtual environment...${NC}"
$REQUIRED_PYTHON -m venv venv
source venv/bin/activate

# Upgrade pip in the virtual environment
echo -e "\n${GREEN}Upgrading pip...${NC}"
python3 -m pip install --upgrade pip

# Install Python dependencies
echo -e "\n${GREEN}Installing Python packages...${NC}"
pip3 install -r requirements.txt

# Check and download required Ollama models
echo -e "\n${GREEN}Checking and downloading required AI models...${NC}"
for model in "${REQUIRED_OLLAMA_MODELS[@]}"; do
    check_ollama_model "$model"
done

# Output summary of software and versions BEFORE running the app
echo -e "\n${GREEN}Environment summary:${NC}"
PYTHON_VERSION_ACTUAL=$(python3 --version 2>&1)
PIP_VERSION_ACTUAL=$(pip3 --version 2>&1)
OLLAMA_VERSION_ACTUAL=$(ollama --version 2>&1)
# List Ollama models
OLLAMA_MODELS=$(ollama list | grep -E "llama3.2|mxbai-embed-large" | awk '{print $1 " (" $2 ")"}')
echo -e "  Python:   $PYTHON_VERSION_ACTUAL"
echo -e "  Pip:      $PIP_VERSION_ACTUAL"
echo -e "  Ollama:   $OLLAMA_VERSION_ACTUAL"
echo -e "  Models:   $OLLAMA_MODELS"

echo -e "\n${GREEN}Activating the virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}Running the multi-project application...${NC}"
python3 main.py

# Only show installation complete if not running the app interactively
if [ "$1" != "run" ]; then
  echo -e "\n${GREEN}Installation complete!${NC}"
fi
