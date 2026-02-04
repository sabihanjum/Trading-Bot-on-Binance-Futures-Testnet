"""
Order placement logic and utilities
"""
from .client import BinanceFuturesClient
from .validators import validate_order_params, ValidationError
from .logging_config import get_logger
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = get_logger()


class OrderManager:
    """
    Manages order placement and execution
    """
    
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """
        Initialize OrderManager with Binance client
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet (default: True)
        """
        logger.info("Initializing OrderManager...")
        self.client = BinanceFuturesClient(api_key, api_secret, testnet)
        logger.info("OrderManager initialized successfully")
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY/SELL)
            quantity: Order quantity
            
        Returns:
            dict: Order response with details
        """
        logger.info(f"=== Placing MARKET Order ===")
        
        try:
            # Validate parameters
            params = validate_order_params(
                symbol=symbol,
                side=side,
                order_type='MARKET',
                quantity=quantity,
                price=None
            )
            
            # Print order summary
            self._print_order_summary(params)
            
            # Place the order
            response = self.client.place_order(
                symbol=params['symbol'],
                side=params['side'],
                order_type=params['order_type'],
                quantity=params['quantity']
            )
            
            # Print order response
            self._print_order_response(response)
            
            return response
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n❌ Order validation failed: {e}")
            raise
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            print(f"\n❌ Order failed: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Failed to place market order: {e}")
            print(f"\n❌ Order failed: {e}")
            raise
    
    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY/SELL)
            quantity: Order quantity
            price: Limit price
            
        Returns:
            dict: Order response with details
        """
        logger.info(f"=== Placing LIMIT Order ===")
        
        try:
            # Validate parameters
            params = validate_order_params(
                symbol=symbol,
                side=side,
                order_type='LIMIT',
                quantity=quantity,
                price=price
            )
            
            # Print order summary
            self._print_order_summary(params)
            
            # Place the order
            response = self.client.place_order(
                symbol=params['symbol'],
                side=params['side'],
                order_type=params['order_type'],
                quantity=params['quantity'],
                price=params['price'],
                timeInForce='GTC'  # Good Till Cancel
            )
            
            # Print order response
            self._print_order_response(response)
            
            return response
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n❌ Order validation failed: {e}")
            raise
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            print(f"\n❌ Order failed: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Failed to place limit order: {e}")
            print(f"\n❌ Order failed: {e}")
            raise
    
    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place an order (routes to appropriate method based on type)
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            dict: Order response
        """
        order_type = order_type.upper()
        
        if order_type == 'MARKET':
            return self.place_market_order(symbol, side, quantity)
        elif order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            return self.place_limit_order(symbol, side, quantity, price)
        else:
            raise ValueError(f"Unsupported order type: {order_type}")
    
    def _print_order_summary(self, params):
        """Print order request summary"""
        print("\n" + "="*50)
        print("ORDER REQUEST SUMMARY")
        print("="*50)
        print(f"Symbol:       {params['symbol']}")
        print(f"Side:         {params['side']}")
        print(f"Type:         {params['order_type']}")
        print(f"Quantity:     {params['quantity']}")
        if params.get('price'):
            print(f"Price:        {params['price']}")
        print("="*50)
        
        logger.info(f"Order summary: {params}")
    
    def _print_order_response(self, response):
        """Print order response details"""
        print("\n" + "="*50)
        print("ORDER RESPONSE")
        print("="*50)
        print(f"Order ID:     {response.get('orderId', 'N/A')}")
        print(f"Symbol:       {response.get('symbol', 'N/A')}")
        print(f"Side:         {response.get('side', 'N/A')}")
        print(f"Type:         {response.get('type', 'N/A')}")
        print(f"Status:       {response.get('status', 'N/A')}")
        print(f"Quantity:     {response.get('origQty', 'N/A')}")
        
        # Show executed quantity if available
        executed_qty = response.get('executedQty', '0')
        if executed_qty and float(executed_qty) > 0:
            print(f"Executed Qty: {executed_qty}")
        
        # Show average price if available
        avg_price = response.get('avgPrice')
        if avg_price and float(avg_price) > 0:
            print(f"Avg Price:    {avg_price}")
        
        # Show limit price for limit orders
        if response.get('price'):
            print(f"Limit Price:  {response.get('price')}")
        
        print("="*50)
        
        # Success message
        status = response.get('status', 'UNKNOWN')
        if status in ['NEW', 'FILLED', 'PARTIALLY_FILLED']:
            print(f"\n✅ Order placed successfully!")
        else:
            print(f"\n⚠️  Order status: {status}")
        
        print()
        logger.info(f"Order response printed: Order ID {response.get('orderId')}")
    
    def test_connection(self):
        """Test connection to Binance API"""
        return self.client.test_connection()
    
    def get_account_info(self):
        """Get account balance information"""
        return self.client.get_account_balance()
