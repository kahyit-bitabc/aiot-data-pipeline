import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbw1buTKxm-B-Xfp1XS-b70a7a2zE08cE6HmR7O6Mc8bN3iGiqpqT2k6DJbB1oFRZofe/exec"

TIMEOUT = 10

# ---------------------------
# OPEN INTEREST FETCHERS
# ---------------------------

def get_binance_oi_usd(symbol="AIOTUSDT"):
    r = requests.get(
        "https://fapi.binance.com/fapi/v1/openInterest",
        params={"symbol": symbol},
        timeout=TIMEOUT
    ).json()
    px = float(requests.get(
        "https://fapi.binance.com/fapi/v1/premiumIndex",
        params={"symbol": symbol},
        timeout=TIMEOUT
    ).json()["markPrice"])
    return float(r["openInterest"]) * px


def get_bingx_oi_usd(symbol="AIOT-USDT"):
    r = requests.get(
        "https://open-api.bingx.com/openApi/swap/v2/quote/openInterest",
        params={"symbol": symbol},
        timeout=TIMEOUT
    ).json()
    return float(r["data"]["openInterest"])


def get_gateio_oi_usd(symbol="AIOT_USDT"):
    r = requests.get(
        "https://api.gateio.ws/api/v4/futures/usdt/contract_stats",
        params={"contract": symbol},
        timeout=TIMEOUT
    ).json()
    return float(r[-1]["open_interest_usd"])


def get_mexc_oi_usd(symbol="AIOT_USDT"):
    r = requests.get(
        "https://contract.mexc.com/api/v1/contract/ticker",
        params={"symbol": symbol},
        timeout=TIMEOUT
    ).json()
    return float(r["data"]["holdVol"])


def get_kucoin_oi_usd(symbol="AIOTUSDTM"):
    r = requests.get(
        f"https://api-futures.kucoin.com/api/v1/contracts/{symbol}",
        timeout=TIMEOUT
    ).json()
    return float(r["data"]["openInterest"])


# ---------------------------
# MAIN
# ---------------------------
def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    data = [
        {"exchange": "Binance", "value": get_binance_oi_usd()},
        {"exchange": "BingX", "value": get_bingx_oi_usd()},
        {"exchange": "Gate.io", "value": get_gateio_oi_usd()},
        {"exchange": "MEXC", "value": get_mexc_oi_usd()},
        {"exchange": "KuCoin", "value": get_kucoin_oi_usd()},
    ]

    payload = {
        "type": "oi",
        "timestamp": timestamp,
        "data": data
    }

    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    print("Status:", r.status_code)
    print("Response:", r.text)


if __name__ == "__main__":
    main()
