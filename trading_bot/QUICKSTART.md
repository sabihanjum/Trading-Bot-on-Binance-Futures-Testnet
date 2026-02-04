# Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Dependencies
```powershell
cd trading_bot
pip install -r requirements.txt
```

### Step 2: Set API Credentials

**PowerShell:**
```powershell
$env:BINANCE_API_KEY = "your_testnet_api_key"
$env:BINANCE_API_SECRET = "your_testnet_api_secret"
```

**Command Prompt:**
```cmd
set BINANCE_API_KEY=your_testnet_api_key
set BINANCE_API_SECRET=your_testnet_api_secret
```

### Step 3: Test Connection
```powershell
python cli.py --test
```

Expected output:
```
🔍 Testing API connection...
✅ Connection successful!
✅ API credentials are valid
```

## Quick Examples

### Example 1: Market Buy Order
```powershell
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Example 2: Limit Sell Order
```powershell
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.0
```

### Example 3: Check Balance
```powershell
python cli.py --balance
```

## Verification

After running orders, check:
1. **Console Output** - Order confirmation with ID and status
2. **Log Files** - Detailed logs in `logs/` directory
3. **Binance Testnet** - Verify orders at https://testnet.binancefuture.com/

## Common Symbols

- BTCUSDT (Bitcoin)
- ETHUSDT (Ethereum)
- BNBUSDT (Binance Coin)
- ADAUSDT (Cardano)
- SOLUSDT (Solana)

## Help

```powershell
python cli.py --help
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API credentials not found" | Set environment variables |
| "Invalid API-key" | Check credentials from testnet |
| "Symbol not found" | Use valid symbols like BTCUSDT |
| "Invalid quantity" | Check minimum order size for symbol |
