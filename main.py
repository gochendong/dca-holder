import threading

from binance import init_binance_trade
from bitget import init_bitget_trade
from dca import dca_task


def main():
    threads = []

    binance_trades = init_binance_trade()
    bitget_trades = init_bitget_trade()

    for trade in binance_trades + bitget_trades:
        thread = threading.Thread(target=dca_task, args=(trade,))
        threads.append(thread)
        thread.start()


if __name__ == "__main__":
    main()