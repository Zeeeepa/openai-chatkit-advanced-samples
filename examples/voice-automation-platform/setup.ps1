# Voice Automation Platform - Setup Script for Windows
# PowerShell installation script

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Voice Automation Platform Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js version..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Backend Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Backend setup
Set-Location backend

Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv
Write-Host "✓ Virtual environment created" -ForegroundColor Green

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ Python dependencies installed" -ForegroundColor Green

# Create .env file
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠ Please edit backend\.env and add your OPENAI_API_KEY" -ForegroundColor Yellow
}

Set-Location ..

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Frontend Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Frontend setup
Set-Location frontend

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
Write-Host "✓ Node.js dependencies installed" -ForegroundColor Green

# Create .env.local file
if (-not (Test-Path .env.local)) {
    Write-Host "Creating .env.local file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env.local
    Write-Host "✓ .env.local created" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Edit backend\.env and add your OPENAI_API_KEY"
Write-Host ""
Write-Host "2. Start the backend server:"
Write-Host "   cd backend"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   uvicorn app.main:app --reload"
Write-Host ""
Write-Host "3. In a new terminal, start the frontend:"
Write-Host "   cd frontend"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "4. Open http://localhost:3000 in your browser"
Write-Host ""
Write-Host "Tip: Use '.\dev-start.ps1' to start both servers at once!" -ForegroundColor Yellow
Write-Host ""

