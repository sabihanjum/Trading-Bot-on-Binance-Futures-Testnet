# PowerShell setup script for the trading bot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Binance Futures Trading Bot - Setup Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/3] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Install dependencies
Write-Host "[2/3] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "Created logs directory" -ForegroundColor Green
}

Write-Host "[3/3] Setup complete!" -ForegroundColor Green
Write-Host ""

# Display next steps
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Get API credentials from: " -NoNewline
Write-Host "https://testnet.binancefuture.com/" -ForegroundColor Blue
Write-Host ""
Write-Host "2. Set your API credentials (PowerShell):" -ForegroundColor White
Write-Host '   $env:BINANCE_API_KEY = "your_api_key_here"' -ForegroundColor Gray
Write-Host '   $env:BINANCE_API_SECRET = "your_api_secret_here"' -ForegroundColor Gray
Write-Host ""
Write-Host "3. Test the connection:" -ForegroundColor White
Write-Host "   python cli.py --test" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Place your first order:" -ForegroundColor White
Write-Host "   python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001" -ForegroundColor Gray
Write-Host ""
Write-Host "See README.md for full documentation" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
