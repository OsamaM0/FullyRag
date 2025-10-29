#!/bin/bash

# PolyRAG Setup Script
# This script helps set up both backend and frontend projects

set -e

echo "🚀 PolyRAG Separated Architecture Setup"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for required tools
check_requirements() {
    echo "📋 Checking requirements..."

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}⚠️  Docker is not installed (optional for development)${NC}"
    fi

    echo -e "${GREEN}✓ Requirements check passed${NC}"
    echo ""
}

# Setup backend
setup_backend() {
    echo "🔧 Setting up Backend..."
    cd backend

    # Copy environment file
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Created .env file. Please configure it with your API keys${NC}"
    fi

    # Install dependencies
    if command -v uv &> /dev/null; then
        echo "Installing dependencies with uv..."
        uv sync --frozen
    else
        echo "Installing uv..."
        pip install uv
        uv sync --frozen
    fi

    echo -e "${GREEN}✓ Backend setup complete${NC}"
    cd ..
    echo ""
}

# Setup frontend
setup_frontend() {
    echo "🎨 Setting up Frontend..."
    cd frontend

    # Copy environment file
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Created .env file. Please configure it${NC}"
    fi

    # Install dependencies
    if command -v uv &> /dev/null; then
        echo "Installing dependencies with uv..."
        uv sync --frozen
    else
        echo "Installing uv..."
        pip install uv
        uv sync --frozen
    fi

    echo -e "${GREEN}✓ Frontend setup complete${NC}"
    cd ..
    echo ""
}

# Setup with Docker
setup_docker() {
    echo "🐳 Setting up with Docker..."

    # Backend
    cd backend
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Created backend/.env file. Please configure it${NC}"
    fi
    echo "Starting backend services..."
    docker-compose up -d
    cd ..

    # Frontend
    cd frontend
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Created frontend/.env file. Please configure it${NC}"
    fi
    echo "Starting frontend services..."
    docker-compose up -d
    cd ..

    echo -e "${GREEN}✓ Docker setup complete${NC}"
    echo ""
}

# Main menu
main_menu() {
    echo "Please choose setup method:"
    echo "1) Local Development (Python)"
    echo "2) Docker Compose"
    echo "3) Both (install Python deps + Docker)"
    echo "4) Exit"
    echo ""
    read -p "Enter choice [1-4]: " choice

    case $choice in
        1)
            check_requirements
            setup_backend
            setup_frontend
            echo -e "${GREEN}✨ Setup complete!${NC}"
            echo ""
            echo "To start the backend:"
            echo "  cd backend && source .venv/bin/activate && python src/run_service.py"
            echo ""
            echo "To start the frontend:"
            echo "  cd frontend && source .venv/bin/activate && streamlit run src/streamlit-app.py"
            ;;
        2)
            setup_docker
            echo -e "${GREEN}✨ Setup complete!${NC}"
            echo ""
            echo "Services are running:"
            echo "  Backend:  http://localhost:8080"
            echo "  Frontend: http://localhost:8501"
            echo "  API Docs: http://localhost:8080/docs"
            ;;
        3)
            check_requirements
            setup_backend
            setup_frontend
            setup_docker
            echo -e "${GREEN}✨ Setup complete!${NC}"
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac
}

# Run main menu
main_menu
