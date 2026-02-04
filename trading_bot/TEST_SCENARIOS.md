# Test Scenarios for Trading Bot

## Prerequisites
Ensure you have set your API credentials:
```powershell
$env:BINANCE_API_KEY = "your_key"
$env:BINANCE_API_SECRET = "your_secret"
```

## Test 1: Connection Test
**Command:**
```powershell
python cli.py --test
```

**Expected Result:**
- Connection successful message
- API credentials validated

---

## Test 2: Account Balance Check
**Command:**
```powershell
python cli.py --balance
```

**Expected Result:**
- Display of wallet balance
- Available balance
- Unrealized profit/loss

---

## Test 3: Market Buy Order (BTCUSDT)
**Command:**
```powershell
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Expected Result:**
- Order placed successfully
- Order ID returned
- Status: FILLED
- Average price displayed

**Log File:** Check logs/ directory for detailed request/response

---

## Test 4: Limit Sell Order (ETHUSDT)
**Command:**
```powershell
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000.0
```

**Expected Result:**
- Order placed successfully
- Order ID returned
- Status: NEW (waiting for price)
- Limit price: 3000.0

**Log File:** Check logs/ directory for detailed request/response

---

## Test 5: Market Sell Order (BNBUSDT)
**Command:**
```powershell
python cli.py --symbol BNBUSDT --side SELL --type MARKET --quantity 0.1
```

**Expected Result:**
- Order executed at market price
- Status: FILLED
- Executed quantity: 0.1

---

## Test 6: Limit Buy Order (BTCUSDT)
**Command:**
```powershell
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 25000.0
```

**Expected Result:**
- Order placed at limit price
- Status: NEW
- Waiting for execution at 25000.0

---

## Test 7: Invalid Input - Missing Price for LIMIT
**Command:**
```powershell
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
```

**Expected Result:**
- ❌ Validation error
- Message: "Price is required for LIMIT orders"

---

## Test 8: Invalid Input - Invalid Side
**Command:**
```powershell
python cli.py --symbol BTCUSDT --side HOLD --type MARKET --quantity 0.001
```

**Expected Result:**
- ❌ Validation error
- Message: "Invalid side"

---

## Test 9: Invalid Input - Negative Quantity
**Command:**
```powershell
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity -0.001
```

**Expected Result:**
- ❌ Validation error
- Message: "Quantity must be positive"

---

## Log Verification

After each test, verify logs in `logs/` directory contain:
1. Request parameters
2. API response
3. Success/failure status
4. Error details (if any)

## Submission Files Required

For the application, include log files from:
1. ✅ One MARKET order (Test 3 or 5)
2. ✅ One LIMIT order (Test 4 or 6)
