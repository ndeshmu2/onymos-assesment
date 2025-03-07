import threading
import random
import time

MAX_TICKERS = 1024 

BUY = "BUY"
SELL = "SELL"

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type 
        self.ticker = ticker        
        self.quantity = quantity
        self.price = price
        self.processed = False     

class OrderBook:
    def __init__(self):
        self.orders = [[] for _ in range(MAX_TICKERS)]

    def add_order(self, order_type, ticker, quantity, price):
        new_order = Order(order_type, ticker, quantity, price)
        self.orders[ticker].append(new_order)
    
    def match_order(self, ticker):

        order_list = self.orders[ticker]

        for buy_order in order_list:
            if buy_order.order_type == BUY and not buy_order.processed:
                best_sell = None
                for sell_order in order_list:
                    if (sell_order.order_type == SELL and not sell_order.processed and
                        sell_order.price <= buy_order.price):
                        if best_sell is None or sell_order.price < best_sell.price:
                            best_sell = sell_order
                
                if best_sell is not None:
                    trade_qty = min(buy_order.quantity, best_sell.quantity)
                    buy_order.quantity -= trade_qty
                    best_sell.quantity -= trade_qty

                    if buy_order.quantity == 0:
                        buy_order.processed = True
                    if best_sell.quantity == 0:
                        best_sell.processed = True

                    print(f"Ticker {ticker}: Matched {trade_qty} shares at price {best_sell.price}")

def simulate_orders(order_book, num_orders=1000):

    for _ in range(num_orders):
        ticker = random.randint(0, MAX_TICKERS - 1)
        quantity = random.randint(1, 100)
        price = round(random.uniform(10.0, 100.0), 2)
        order_type = random.choice([BUY, SELL])
        
        order_book.add_order(order_type, ticker, quantity, price)

        time.sleep(0.001)

def main():
    order_book = OrderBook()

    simulator_thread = threading.Thread(target=simulate_orders, args=(order_book,))
    simulator_thread.start()
    simulator_thread.join()

    for ticker in range(MAX_TICKERS):
        order_book.match_order(ticker)

if __name__ == "__main__":
    main()
