"""
Input validators for trading bot
"""
import re
from decimal import Decimal, InvalidOperation
from .logging_config import get_logger

logger = get_logger()


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_symbol(symbol):
    """
    Validate trading symbol format
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Returns:
        str: Uppercase symbol
        
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.upper().strip()
    
    # Basic validation - alphanumeric only
    if not re.match(r'^[A-Z0-9]+$', symbol):
        raise ValidationError(f"Invalid symbol format: {symbol}")
    
    # Most Binance Futures symbols end with USDT or BUSD
    if not (symbol.endswith('USDT') or symbol.endswith('BUSD')):
        logger.warning(f"Symbol {symbol} doesn't end with USDT or BUSD - may be invalid")
    
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side):
    """
    Validate order side
    
    Args:
        side: Order side (BUY or SELL)
        
    Returns:
        str: Uppercase side
        
    Raises:
        ValidationError: If side is invalid
    """
    if not side:
        raise ValidationError("Side cannot be empty")
    
    side = side.upper().strip()
    
    if side not in ['BUY', 'SELL']:
        raise ValidationError(f"Invalid side: {side}. Must be BUY or SELL")
    
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type):
    """
    Validate order type
    
    Args:
        order_type: Order type (MARKET or LIMIT)
        
    Returns:
        str: Uppercase order type
        
    Raises:
        ValidationError: If order type is invalid
    """
    if not order_type:
        raise ValidationError("Order type cannot be empty")
    
    order_type = order_type.upper().strip()
    
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError(f"Invalid order type: {order_type}. Must be MARKET or LIMIT")
    
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity):
    """
    Validate order quantity
    
    Args:
        quantity: Order quantity as string or number
        
    Returns:
        float: Validated quantity
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity: {quantity}. Must be a number")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be positive: {qty}")
    
    logger.debug(f"Quantity validated: {qty}")
    return qty


def validate_price(price, order_type):
    """
    Validate order price
    
    Args:
        price: Order price as string or number
        order_type: Order type (MARKET or LIMIT)
        
    Returns:
        float or None: Validated price (None for MARKET orders)
        
    Raises:
        ValidationError: If price is invalid
    """
    if order_type == 'MARKET':
        if price is not None and price != '':
            logger.warning("Price provided for MARKET order - will be ignored")
        return None
    
    if order_type == 'LIMIT':
        if price is None or price == '':
            raise ValidationError("Price is required for LIMIT orders")
        
        try:
            prc = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid price: {price}. Must be a number")
        
        if prc <= 0:
            raise ValidationError(f"Price must be positive: {prc}")
        
        logger.debug(f"Price validated: {prc}")
        return prc
    
    return None


def validate_order_params(symbol, side, order_type, quantity, price=None):
    """
    Validate all order parameters together
    
    Args:
        symbol: Trading pair symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT)
        quantity: Order quantity
        price: Order price (required for LIMIT)
        
    Returns:
        dict: Validated parameters
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    logger.info("Validating order parameters...")
    
    try:
        validated = {
            'symbol': validate_symbol(symbol),
            'side': validate_side(side),
            'order_type': validate_order_type(order_type),
            'quantity': validate_quantity(quantity),
            'price': validate_price(price, order_type)
        }
        
        logger.info("All parameters validated successfully")
        return validated
        
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise
