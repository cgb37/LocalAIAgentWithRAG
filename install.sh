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

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        if [ "$1" = "ollama" ]; then
            echo -e "${RED}Error: ollama is not installed${NC}"
            echo -e "${YELLOW}Please install ollama first:${NC}"
            echo -e "1. Visit ${GREEN}https://ollama.com${NC}"
            echo -e "2. Download and install the Mac version"
            echo -e "3. Run this script again after installation"
            exit 1
        else
            echo -e "${RED}Error: $1 is not installed${NC}"
            echo "Please install $1 and try again"
            exit 1
        fi
    fi
}
# Check prerequisites
echo "Checking prerequisites..."
check_command "python3"
check_command "pip3"
check_command "ollama"

# Create and activate virtual environment
echo -e "\n${GREEN}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "\n${GREEN}Installing Python packages...${NC}"
pip3 install -r requirements.txt

# Download required AI models
echo -e "\n${GREEN}Downloading AI models...${NC}"
ollama pull llama3.2
ollama pull mxbai-embed-large

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "To start using the project:"
echo -e "1. Activate the virtual environment: ${GREEN}source venv/bin/activate${NC}"
echo -e "2. Run the application: ${GREEN}python3 main.py${NC}"