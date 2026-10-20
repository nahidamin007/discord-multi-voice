#!/bin/bash

# Colors
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== SMART LAUNCHER V2 (RedHat Optimized) ===${NC}"

# 1. Determine the directory
cd "$(dirname "$0")"

# 2. Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[Error] Python3 is not installed!${NC}"
    exit 1
fi

# Print version for debug
python3 --version

# 3. Setup Venv
VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}[!] Initializing a new venv...${NC}"
    
    # Try standard venv creation with Pip
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[Error] Unable to create venv. Please check your Python installation.${NC}"
        # Fallback suggestion for RedHat/CentOS/Fedora
        echo -e "${YELLOW}Suggestion: sudo dnf install python3-pip python3-devel${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[v] Venv created successfully.${NC}"
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}[*] Installing dependencies...${NC}"
        ./$VENV_DIR/bin/pip install --upgrade pip
        ./$VENV_DIR/bin/pip install -r requirements.txt
        
        if [ $? -ne 0 ]; then
             echo -e "${RED}[!] Dependency installation failed.${NC}"
             exit 1
        fi
        echo -e "${GREEN}[v] Installation completed!${NC}"
    else
        echo -e "${RED}[!] requirements.txt not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}[v] Using existing venv.${NC}"
fi

# 4. Run Dashboard
echo -e "${GREEN}[*] Starting Bot...${NC}"
echo "------------------------------------------------"

./$VENV_DIR/bin/python3 dashboard.py

EXIT_CODE=$?

echo "------------------------------------------------"
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}[!] Bot stopped with an error (Code: $EXIT_CODE).${NC}"
else
    echo -e "${GREEN}[!] Bot stopped.${NC}"
fi