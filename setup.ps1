# PolyRAG Setup Script for Windows
# This script helps set up both backend and frontend projects

Write-Host "🚀 PolyRAG Separated Architecture Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check for required tools
function Check-Requirements {
    Write-Host "📋 Checking requirements..." -ForegroundColor Yellow

    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Python 3 is not installed" -ForegroundColor Red
        exit 1
    }

    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "⚠️  Docker is not installed (optional for development)" -ForegroundColor Yellow
    }

    Write-Host "✓ Requirements check passed" -ForegroundColor Green
    Write-Host ""
}

# Setup backend
function Setup-Backend {
    Write-Host "🔧 Setting up Backend..." -ForegroundColor Yellow
    Set-Location backend

    # Copy environment file
    if (-not (Test-Path .env)) {
        Copy-Item .env.example .env
        Write-Host "⚠️  Created .env file. Please configure it with your API keys" -ForegroundColor Yellow
    }

    # Install dependencies
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        Write-Host "Installing dependencies with uv..."
        uv sync --frozen
    } else {
        Write-Host "Installing uv..."
        pip install uv
        uv sync --frozen
    }

    Write-Host "✓ Backend setup complete" -ForegroundColor Green
    Set-Location ..
    Write-Host ""
}

# Setup frontend
function Setup-Frontend {
    Write-Host "🎨 Setting up Frontend..." -ForegroundColor Yellow
    Set-Location frontend

    # Copy environment file
    if (-not (Test-Path .env)) {
        Copy-Item .env.example .env
        Write-Host "⚠️  Created .env file. Please configure it" -ForegroundColor Yellow
    }

    # Install dependencies
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        Write-Host "Installing dependencies with uv..."
        uv sync --frozen
    } else {
        Write-Host "Installing uv..."
        pip install uv
        uv sync --frozen
    }

    Write-Host "✓ Frontend setup complete" -ForegroundColor Green
    Set-Location ..
    Write-Host ""
}

# Setup with Docker
function Setup-Docker {
    Write-Host "🐳 Setting up with Docker..." -ForegroundColor Yellow

    # Backend
    Set-Location backend
    if (-not (Test-Path .env)) {
        Copy-Item .env.example .env
        Write-Host "⚠️  Created backend/.env file. Please configure it" -ForegroundColor Yellow
    }
    Write-Host "Starting backend services..."
    docker-compose up -d
    Set-Location ..

    # Frontend
    Set-Location frontend
    if (-not (Test-Path .env)) {
        Copy-Item .env.example .env
        Write-Host "⚠️  Created frontend/.env file. Please configure it" -ForegroundColor Yellow
    }
    Write-Host "Starting frontend services..."
    docker-compose up -d
    Set-Location ..

    Write-Host "✓ Docker setup complete" -ForegroundColor Green
    Write-Host ""
}

# Main menu
function Show-Menu {
    Write-Host "Please choose setup method:" -ForegroundColor Cyan
    Write-Host "1) Local Development (Python)"
    Write-Host "2) Docker Compose"
    Write-Host "3) Both (install Python deps + Docker)"
    Write-Host "4) Exit"
    Write-Host ""

    $choice = Read-Host "Enter choice [1-4]"

    switch ($choice) {
        "1" {
            Check-Requirements
            Setup-Backend
            Setup-Frontend
            Write-Host "✨ Setup complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "To start the backend:" -ForegroundColor Cyan
            Write-Host "  cd backend; .venv\Scripts\activate; python src\run_service.py"
            Write-Host ""
            Write-Host "To start the frontend:" -ForegroundColor Cyan
            Write-Host "  cd frontend; .venv\Scripts\activate; streamlit run src\streamlit-app.py"
        }
        "2" {
            Setup-Docker
            Write-Host "✨ Setup complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Services are running:" -ForegroundColor Cyan
            Write-Host "  Backend:  http://localhost:8080"
            Write-Host "  Frontend: http://localhost:8501"
            Write-Host "  API Docs: http://localhost:8080/docs"
        }
        "3" {
            Check-Requirements
            Setup-Backend
            Setup-Frontend
            Setup-Docker
            Write-Host "✨ Setup complete!" -ForegroundColor Green
        }
        "4" {
            Write-Host "Exiting..." -ForegroundColor Yellow
            exit 0
        }
        default {
            Write-Host "❌ Invalid choice" -ForegroundColor Red
            exit 1
        }
    }
}

# Run main menu
Show-Menu
