import os
import time
import ccxt

from common import (
    BaseClient,
    TradeParams,
    Trade,
    round_floor,
    logger,
    Asset,
    DEFAULT_TYPE,
)


EX = "OKX"


def init_okx_trade():
    trades = []
    uids, api_keys, secret_keys, passwords = (
        os.getenv(f"{EX}_UID"),
        os.getenv(f"{EX}_API_KEY"),
        os.getenv(f"{EX}_SECRET_KEY"),
        os.getenv(f"{EX}_PASSWORD"),
    )
    if uids and api_keys and secret_keys and passwords:
        uids, api_keys, secret_keys, passwords = (
            uids.split(","),
            api_keys.split(","),
            secret_keys.split(","),
            passwords.split(","),
        )
        if (
            len(uids) != len(api_keys)
            or len(api_keys) != len(secret_keys)
            or len(secret_keys) != len(passwords)
        ):
            logger.error(
                "UID, API_KEY, and SECRET_KEY and PASSWORD must have the same length"
            )
            return
        for idx, uid in enumerate(uids):
            client = OKXClient(api_keys[idx], secret_keys[idx], passwords[idx])
            trade_params = TradeParams(EX)
            trade = Trade(
                user_id=uid,
                exchange=EX,
                client=client,
                shares=trade_params.shares,
                min_amount=trade_params.min_amount,
                max_amount=trade_params.max_amount,
                min_profit_percent=trade_params.min_profit_percent,
                add_position_ratio=trade_params.add_position_ratio,
                increase_position_ratio=trade_params.increase_position_ratio,
            )
            trades.append(trade)
    return trades


class OKXClient(BaseClient):
    def __init__(self, api_key, secret_key, password):
        super().__init__(api_key, secret_key, password)
        self.spot = self.connect_exchange(api_key, secret_key, password)

    def connect_exchange(self, apiKey, secretKey, password):
        return ccxt.okx(
            {
                "verify": False,
                "enableRateLimit": True,
                "options": {
                    "defaultType": DEFAULT_TYPE,
                },
                "apiKey": apiKey,
                "secret": secretKey,
                "password": password,
            }
        )

    def fetch_earn_balance(self, token):
        if token == Asset:
            return 0
        poss = self.spot.private_get_finance_savings_balance()["data"]
        for pos in poss:
            if pos["ccy"] == token:
                return float(pos["amt"])
        return 0

    def subscribe(self, token, amount):
        if token == Asset:
            return
        amount = round_floor(amount)
        logger.info(f"subscribe {amount} {token}")
        try:
            self.transfer_to_funding(token, amount)
            self.spot.private_post_finance_savings_purchase_redempt(
                {
                    "ccy": token,
                    "amt": float(amount),
                    "side": "purchase",
                    "rate": 0.01,
                }
            )
        except Exception as e:
            logger.error(e)

    def redeem(self, token, amount):
        if token == Asset:
            return
        if amount < 1:
            amount = 1
        amount = round_floor(amount)
        logger.info(f"redeem {amount} {token}")
        self.spot.private_post_finance_savings_purchase_redempt(
            {
                "ccy": token,
                "amt": float(amount),
                "side": "redempt",
                "rate": 0.01,
            }
        )
        self.transfer_to_spot(token, amount)

    def trading(self, symbol, side, amount, value):
        return super().place_market_order(symbol, side, amount, value, False)

    # 6：资金账户
    # 18：交易账户
    def transfer_to_spot(self, token, amount):
        try:
            self.spot.transfer(token, amount, "6", "18")
        except Exception as e:
            logger.error(e)

    def transfer_to_funding(self, token, amount):
        if token == Asset:
            amount = round_floor(amount)
            logger.info(f"reserve: {amount:.8f} {token}")
        try:
            self.spot.transfer(token, amount, "18", "6")
        except Exception as e:
            logger.error(e)
