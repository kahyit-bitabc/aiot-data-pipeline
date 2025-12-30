import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxIHxL4rpqorfx_QFf1YjqPpkBJErbhW3CiZc4JfgHb5nJZM34iT_1nXRbyKHoGnabN/exec"

SYMBOL = "AIOTUSDT"
SYMBOL_BINGX = "AIOT-USDT"
SYMBOL_MEXC = "AIOT_USDT"
SYMBOL_KUCOIN = "AIOTUSDTM"


def get_binance_funding():
    return float(requests.get(
        "https://fapi.binance.com/fapi/v1/premiumIndex",
        params={"symbol": SYMBOL},
        timeout=10
    ).json()["lastFundingRate"])


def get_bingx_funding():
    return float(requests.get(
        "https://open-api.bingx.com/openApi/swap/v2/quote/premiumIndex",
        params={"symbol": SYMBOL_BINGX},
        timeout=10
    ).json()["data"]["lastFundingRate"])


def get_mexc_funding():
    return float(requests.get(
        "https://contract.mexc.com/api/v1/contract/ticker",
        params={"symbol": SYMBOL_MEXC},
        timeout=10
    ).json()["data"]["fundingRate"])


def get_gateio_funding():
    return float(requests.get(
        f"https://api.gateio.ws/api/v4/futures/usdt/contracts/{SYMBOL_MEXC}",
        timeout=10
    ).json()["funding_rate"])


def get_kucoin_funding():
    return float(requests.get(
        f"https://api-futures.kucoin.com/api/v1/contracts/{SYMBOL_KUCOIN}",
        timeout=10
    ).json()["data"]["fundingFeeRate"])


def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    funding = {
        "Binance": get_binance_funding(),
        "BingX": get_bingx_funding(),
        "MEXC": get_mexc_funding(),
        "Gate.io": get_gateio_funding(),
        "KuCoin": get_kucoin_funding()
    }

    payload = {
        "timestamp": timestamp,
        "funding": funding
    }

    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    print("Status:", r.status_code)
    print("Response:", r.text)
    print(payload)


if __name__ == "__main__":
    main()
