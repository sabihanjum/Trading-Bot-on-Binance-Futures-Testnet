#!/usr/bin/env python3
"""
Binance Futures Trading Bot - CLI Interface

Command-line interface for placing orders on Binance Futures Testnet
"""
import argparse
import sys
import os
from bot.logging_config import setup_logging
from bot.orders import OrderManager
from bot.validators import ValidationError
from binance.exceptions import BinanceAPIException


def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description='Trading Bot for Binance Futures Testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Place a market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Place a limit sell order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.0

  # Test connection
  python cli.py --test
        '''
    )
    
    parser.add_argument(
        '--symbol',
        type=str,
        help='Trading pair symbol (e.g., BTCUSDT, ETHUSDT)'
    )
    
    parser.add_argument(
        '--side',
        type=str,
        choices=['BUY', 'SELL', 'buy', 'sell'],
        help='Order side (BUY or SELL)'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        dest='order_type',
        choices=['MARKET', 'LIMIT', 'market', 'limit'],
        help='Order type (MARKET or LIMIT)'
    )
    
    parser.add_argument(
        '--quantity',
        type=float,
        help='Order quantity'
    )
    
    parser.add_argument(
        '--price',
        type=float,
        help='Order price (required for LIMIT orders)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test API connection and credentials'
    )
    
    parser.add_argument(
        '--balance',
        action='store_true',
        help='Show account balance'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='Binance API key (or set BINANCE_API_KEY env variable)'
    )
    
    parser.add_argument(
        '--api-secret',
        type=str,
        help='Binance API secret (or set BINANCE_API_SECRET env variable)'
    )
    
    return parser


def validate_order_args(args):
    """Validate that required arguments are provided for placing orders"""
    if not args.symbol:
        raise ValueError("--symbol is required")
    if not args.side:
        raise ValueError("--side is required")
    if not args.order_type:
        raise ValueError("--type is required")
    if not args.quantity:
        raise ValueError("--quantity is required")
    
    if args.order_type.upper() == 'LIMIT' and not args.price:
        raise ValueError("--price is required for LIMIT orders")


def main():
    """Main CLI entry point"""
    # Setup logging
    logger = setup_logging()
    
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Print header
    print("\n" + "="*60)
    print("BINANCE FUTURES TRADING BOT (TESTNET)")
    print("="*60)
    
    try:
        # Initialize OrderManager
        logger.info("Initializing trading bot...")
        order_manager = OrderManager(
            api_key=args.api_key,
            api_secret=args.api_secret,
            testnet=True
        )
        
        # Handle test connection
        if args.test:
            print("\n🔍 Testing API connection...")
            if order_manager.test_connection():
                print("✅ Connection successful!")
                print("✅ API credentials are valid")
                return 0
            else:
                print("❌ Connection test failed")
                print("Please check your API credentials and network connection")
                return 1
        
        # Handle balance query
        if args.balance:
            print("\n💰 Fetching account balance...")
            balance = order_manager.get_account_info()
            print("\nAccount Balance:")
            print(f"  Total Wallet Balance: {balance.get('total_wallet_balance', 'N/A')} USDT")
            print(f"  Available Balance:    {balance.get('available_balance', 'N/A')} USDT")
            print(f"  Unrealized Profit:    {balance.get('total_unrealized_profit', 'N/A')} USDT")
            return 0
        
        # Validate order arguments
        if not args.test and not args.balance:
            validate_order_args(args)
            
            # Place order
            logger.info(f"Placing {args.order_type} {args.side} order...")
            response = order_manager.place_order(
                symbol=args.symbol,
                side=args.side,
                order_type=args.order_type,
                quantity=args.quantity,
                price=args.price
            )
            
            return 0
    
    except ValueError as e:
        logger.error(f"Invalid arguments: {e}")
        print(f"\n❌ Error: {e}")
        print("\nUse --help to see usage information")
        return 1
    
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n❌ Validation error: {e}")
        return 1
    
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e.status_code} - {e.message}")
        print(f"\n❌ Binance API Error: {e.message}")
        if e.status_code == 401:
            print("Please check your API credentials")
        return 1
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
