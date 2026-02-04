@echo off
REM Windows batch script to set up the trading bot

echo ============================================================
echo Binance Futures Trading Bot - Setup Script
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/3] Python detected...
python --version
echo.

REM Install dependencies
echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/3] Setup complete!
echo.

REM Create logs directory
if not exist logs mkdir logs

echo ============================================================
echo Next Steps:
echo ============================================================
echo.
echo 1. Get API credentials from: https://testnet.binancefuture.com/
echo.
echo 2. Set your API credentials (in Command Prompt):
echo    set BINANCE_API_KEY=your_api_key_here
echo    set BINANCE_API_SECRET=your_api_secret_here
echo.
echo 3. Test the connection:
echo    python cli.py --test
echo.
echo 4. Place your first order:
echo    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
echo.
echo See README.md for full documentation
echo ============================================================
echo.

pause
