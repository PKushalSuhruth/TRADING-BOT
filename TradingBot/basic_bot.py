from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging

# Configure logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        # Set base URL for Binance Futures Testnet
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }

            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Limit orders require a price.")
                order_params['price'] = price
                order_params['timeInForce'] = 'GTC'

            # Place the order
            order = self.client.futures_create_order(**order_params)
            logging.info(f"Order placed: {order}")
            print(f"✅ Order Successful: {order}")

        except BinanceAPIException as e:
            logging.error(f"Binance API error: {e}")
            print(f"❌ API Exception: {e}")

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Enter API Key and Secret safely
    api_key = input("🔑 Enter your Binance API Key: ")
    api_secret = input("🔑 Enter your Binance Secret Key: ")

    bot = BasicBot(api_key, api_secret)

    # Get order details from the user
    symbol = input("Enter trading pair symbol (e.g., BTCUSDT): ")
    side = input("Enter order side (BUY/SELL): ").upper()
    order_type = input("Enter order type (MARKET/LIMIT): ").upper()
    quantity = float(input("Enter quantity: "))

    price = None
    if order_type == 'LIMIT':
        price = float(input("Enter limit price: "))

    # Place the order
    bot.place_order(symbol, side, order_type, quantity, price)
