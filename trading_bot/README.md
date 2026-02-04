# Binance Futures Trading Bot (Testnet)

A Python application for placing orders on Binance Futures Testnet (USDT-M) with clean architecture, comprehensive logging, and robust error handling.

## Features

- ✅ Place **MARKET** and **LIMIT** orders on Binance Futures Testnet
- ✅ Support for **BUY** and **SELL** orders
- ✅ CLI interface with argument validation
- ✅ Structured, modular codebase
- ✅ Comprehensive logging to file
- ✅ Robust error handling for API and network failures
- ✅ Input validation with clear error messages
- ✅ Test connection and check account balance

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Binance Futures API client wrapper
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # Input validation functions
│   └── logging_config.py    # Logging configuration
├── cli.py                   # CLI entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── README.md                # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account
- API credentials from Binance Futures Testnet

### 2. Get API Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Create an account or log in
3. Generate API Key and Secret Key
4. Save your credentials securely

### 3. Install Dependencies

```bash
# Navigate to the project directory
cd trading_bot

# Install required packages
pip install -r requirements.txt
```

### 4. Configure API Credentials

**Option 1: Environment Variables (Recommended)**

On Windows (PowerShell):
```powershell
$env:BINANCE_API_KEY = "your_api_key_here"
$env:BINANCE_API_SECRET = "your_api_secret_here"
```

On Windows (Command Prompt):
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

On Linux/Mac:
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

**Option 2: Create .env file**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials
# BINANCE_API_KEY=your_api_key_here
# BINANCE_API_SECRET=your_api_secret_here
```

**Option 3: Pass as CLI arguments**

```bash
python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET --test
```

## Usage

### Test Connection

Before placing orders, verify your API credentials:

```bash
python cli.py --test
```

### Check Account Balance

```bash
python cli.py --balance
```

### Place a Market Order

**Market Buy Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Market Sell Order:**
```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

### Place a Limit Order

**Limit Buy Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 30000.0
```

**Limit Sell Order:**
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.0
```

## CLI Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--symbol` | Yes* | Trading pair symbol (e.g., BTCUSDT, ETHUSDT) |
| `--side` | Yes* | Order side: BUY or SELL |
| `--type` | Yes* | Order type: MARKET or LIMIT |
| `--quantity` | Yes* | Order quantity (must be positive) |
| `--price` | Yes** | Order price (required for LIMIT orders) |
| `--test` | No | Test API connection and credentials |
| `--balance` | No | Show account balance |
| `--api-key` | No | Binance API key (overrides env variable) |
| `--api-secret` | No | Binance API secret (overrides env variable) |

\* Required for placing orders  
\** Required only for LIMIT orders

## Examples

### Example 1: Market Buy Order (BTCUSDT)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Expected Output:**
```
============================================================
BINANCE FUTURES TRADING BOT (TESTNET)
============================================================

==================================================
ORDER REQUEST SUMMARY
==================================================
Symbol:       BTCUSDT
Side:         BUY
Type:         MARKET
Quantity:     0.001
==================================================

==================================================
ORDER RESPONSE
==================================================
Order ID:     123456789
Symbol:       BTCUSDT
Side:         BUY
Type:         MARKET
Status:       FILLED
Quantity:     0.001
Executed Qty: 0.001
Avg Price:    42350.5
==================================================

✅ Order placed successfully!
```

### Example 2: Limit Sell Order (ETHUSDT)

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.0
```

**Expected Output:**
```
============================================================
BINANCE FUTURES TRADING BOT (TESTNET)
============================================================

==================================================
ORDER REQUEST SUMMARY
==================================================
Symbol:       ETHUSDT
Side:         SELL
Type:         LIMIT
Quantity:     0.01
Price:        2500.0
==================================================

==================================================
ORDER RESPONSE
==================================================
Order ID:     987654321
Symbol:       ETHUSDT
Side:         SELL
Type:         LIMIT
Status:       NEW
Quantity:     0.01
Limit Price:  2500.0
==================================================

✅ Order placed successfully!
```

## Logging

All operations are logged to files in the `logs/` directory:

- **Log file format:** `trading_bot_YYYYMMDD_HHMMSS.log`
- **Location:** `logs/` directory (created automatically)
- **Content:** API requests, responses, errors, and debug information

Example log entries:
```
2026-02-04 10:30:15 - trading_bot - INFO - Logging initialized. Log file: logs/trading_bot_20260204_103015.log
2026-02-04 10:30:15 - trading_bot - INFO - Initializing OrderManager...
2026-02-04 10:30:16 - trading_bot - INFO - Binance Futures client initialized (TESTNET)
2026-02-04 10:30:16 - trading_bot - INFO - === Placing MARKET Order ===
2026-02-04 10:30:16 - trading_bot - INFO - Validating order parameters...
2026-02-04 10:30:16 - trading_bot - INFO - All parameters validated successfully
2026-02-04 10:30:17 - trading_bot - INFO - Order placed successfully: Order ID 123456789
```

## Error Handling

The bot handles various error scenarios:

### Invalid Input
```bash
python cli.py --symbol BTCUSDT --side INVALID --type MARKET --quantity 0.001

❌ Validation error: Invalid side: INVALID. Must be BUY or SELL
```

### Missing Required Parameter
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001

❌ Validation error: Price is required for LIMIT orders
```

### API Errors
```bash
# Invalid API credentials
❌ Binance API Error: Invalid API-key, IP, or permissions for action.
Please check your API credentials
```

### Network Errors
```bash
# Network connection issues
❌ Unexpected error: Connection timeout
```

## Code Structure

### client.py
- `BinanceFuturesClient`: Wrapper for Binance Futures API
- Connection testing, order placement, and account queries
- API error handling and logging

### orders.py
- `OrderManager`: High-level order management
- `place_market_order()`: Place market orders
- `place_limit_order()`: Place limit orders
- Order summary and response formatting

### validators.py
- Input validation functions
- `validate_symbol()`: Validate trading symbols
- `validate_side()`: Validate order side (BUY/SELL)
- `validate_order_type()`: Validate order type (MARKET/LIMIT)
- `validate_quantity()`: Validate order quantity
- `validate_price()`: Validate order price

### logging_config.py
- Logging setup with file and console handlers
- Timestamped log files
- Different log levels for file and console

## Testing

### Test Connection
```bash
python cli.py --test
```

### Test with Different Symbols
```bash
# Bitcoin
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Ethereum
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.01

# Binance Coin
python cli.py --symbol BNBUSDT --side BUY --type MARKET --quantity 0.1
```

## Assumptions

1. **Testnet Environment**: All orders are placed on Binance Futures Testnet
2. **USDT-M Futures**: Using USDT-margined futures contracts
3. **Time In Force**: LIMIT orders use GTC (Good Till Cancel) by default
4. **Quantity Precision**: User is responsible for providing valid quantity based on symbol rules
5. **Price Precision**: User is responsible for providing valid price based on symbol rules

## Troubleshooting

### Issue: "API credentials not found"
**Solution:** Set environment variables or pass credentials as CLI arguments

### Issue: "Symbol not found"
**Solution:** Ensure the symbol is valid and available on Binance Futures (e.g., BTCUSDT, ETHUSDT)

### Issue: "Invalid quantity"
**Solution:** Check minimum order quantity for the symbol (varies by trading pair)

### Issue: "Connection timeout"
**Solution:** Check your internet connection and firewall settings

### Issue: "Invalid API-key"
**Solution:** Verify your API credentials are correct and have Futures trading permissions

## Important Notes

⚠️ **This is for TESTNET only** - No real funds are involved  
⚠️ **Never share your API credentials** - Keep them secure  
⚠️ **Check order parameters** - Validate symbol, quantity, and price before placing orders  
⚠️ **Monitor logs** - Check log files for detailed execution information

## Support

For issues or questions:
- Check the log files in the `logs/` directory
- Review Binance Futures Testnet API documentation
- Ensure your API credentials have proper permissions

## License

This project is created for application purposes and educational use.

---

**Developed by:** Sabiha Anjum  
**Date:** February 4, 2026  
**Purpose:** Application Task - Python Developer (Trading Bot)
