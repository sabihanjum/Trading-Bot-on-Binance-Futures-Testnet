"""
Binance Futures client wrapper
"""
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .logging_config import get_logger

logger = get_logger()


class BinanceFuturesClient:
    """
    Wrapper for Binance Futures API client
    """
    
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """
        Initialize Binance Futures client
        
        Args:
            api_key: Binance API key (if None, reads from environment)
            api_secret: Binance API secret (if None, reads from environment)
            testnet: Use testnet (default: True)
        """
        # Get credentials from environment if not provided
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "API credentials not found. "
                "Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables "
                "or pass them as arguments."
            )
        
        try:
            # Initialize Binance client
            self.client = Client(self.api_key, self.api_secret, testnet=testnet)
            
            # Set testnet URL for futures
            if testnet:
                self.client.API_URL = 'https://testnet.binancefuture.com'
                logger.info("Binance Futures client initialized (TESTNET)")
            else:
                logger.info("Binance Futures client initialized (PRODUCTION)")
                
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    def test_connection(self):
        """
        Test API connection and credentials
        
        Returns:
            bool: True if connection successful
        """
        try:
            logger.info("Testing API connection...")
            # Test connectivity
            server_time = self.client.futures_time()
            logger.info(f"Server time: {server_time}")
            
            # Test authentication
            account_info = self.client.futures_account()
            logger.info("API authentication successful")
            logger.debug(f"Account balance: {account_info.get('totalWalletBalance', 'N/A')} USDT")
            
            return True
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            return False
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {e}")
            return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_symbol_info(self, symbol):
        """
        Get trading rules and information for a symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            dict: Symbol information or None if not found
        """
        try:
            logger.debug(f"Fetching symbol info for {symbol}")
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.debug(f"Symbol {symbol} found: {s['status']}")
                    return s
            
            logger.warning(f"Symbol {symbol} not found in exchange info")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get symbol info: {e}")
            return None
    
    def get_account_balance(self):
        """
        Get account balance information
        
        Returns:
            dict: Account balance details
        """
        try:
            logger.debug("Fetching account balance")
            account = self.client.futures_account()
            
            balance_info = {
                'total_wallet_balance': account.get('totalWalletBalance', '0'),
                'total_unrealized_profit': account.get('totalUnrealizedProfit', '0'),
                'available_balance': account.get('availableBalance', '0')
            }
            
            logger.debug(f"Account balance: {balance_info}")
            return balance_info
            
        except Exception as e:
            logger.error(f"Failed to get account balance: {e}")
            return {}
    
    def place_order(self, symbol, side, order_type, quantity, price=None, **kwargs):
        """
        Place an order on Binance Futures
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            **kwargs: Additional order parameters
            
        Returns:
            dict: Order response
            
        Raises:
            BinanceAPIException: If API request fails
        """
        try:
            logger.info(f"Placing {order_type} {side} order for {symbol}")
            logger.debug(f"Order params: quantity={quantity}, price={price}")
            
            # Prepare order parameters
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }
            
            # Add price for LIMIT orders
            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders")
                params['price'] = price
                params['timeInForce'] = kwargs.get('timeInForce', 'GTC')  # Good Till Cancel
            
            # Add any additional parameters
            params.update(kwargs)
            
            logger.debug(f"Final order parameters: {params}")
            
            # Place the order
            response = self.client.futures_create_order(**params)
            
            logger.info(f"Order placed successfully: Order ID {response.get('orderId')}")
            logger.debug(f"Order response: {response}")
            
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            logger.error(f"Failed order params: {params}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            raise
    
    def get_order_status(self, symbol, order_id):
        """
        Get status of an order
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            dict: Order status information
        """
        try:
            logger.debug(f"Fetching order status: {order_id}")
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logger.debug(f"Order status: {order}")
            return order
            
        except Exception as e:
            logger.error(f"Failed to get order status: {e}")
            raise
