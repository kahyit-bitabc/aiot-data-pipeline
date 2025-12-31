import requests
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbw1buTKxm-B-Xfp1XS-b70a7a2zE08cE6HmR7O6Mc8bN3iGiqpqT2k6DJbB1oFRZofe/exec"
TIMEOUT = 10


# ---------------------------
# SAFE FETCH HELPERS
# ---------------------------
def safe_float(val):
    try:
        return float(val)
    except:
        return None


def get_binance_oi_usd(symbol="AIOTUSDT"):
    try:
        oi = requests.get(
            "https://fapi.binance.com/fapi/v1/openInterest",
            params={"symbol": symbol},
            timeout=TIMEOUT
        ).json()["openInterest"]

        px = requests.get(
            "https://fapi.binance.com/fapi/v1/premiumIndex",
            params={"symbol": symbol},
            timeout=TIMEOUT
        ).json()["markPrice"]

        return float(oi) * float(px)
    except Exception as e:
        print("Binance error:", e)
        return None


def get_bingx_oi_usd(symbol="AIOT-USDT"):
    try:
        r = requests.get(
            "https://open-api.bingx.com/openApi/swap/v2/quote/openInterest",
            params={"symbol": symbol},
            timeout=TIMEOUT
        ).json()
        return float(r["data"]["openInterest"])
    except Exception as e:
        print("BingX error:", e)
        return None


def get_gateio_oi_usd(symbol="AIOT_USDT"):
    try:
        r = requests.get(
            "https://api.gateio.ws/api/v4/futures/usdt/contract_stats",
            params={"contract": symbol},
            timeout=TIMEOUT
        ).json()
        return float(r[-1]["open_interest_usd"])
    except Exception as e:
        print("Gate.io error:", e)
        return None


def get_mexc_oi_usd(symbol="AIOT_USDT"):
    try:
        r = requests.get(
            "https://contract.mexc.com/api/v1/contract/ticker",
            params={"symbol": symbol},
            timeout=TIMEOUT
        ).json()
        return float(r["data"]["holdVol"])
    except Exception as e:
        print("MEXC error:", e)
        return None


def get_kucoin_oi_usd(symbol="AIOTUSDTM"):
    try:
        r = requests.get(
            f"https://api-futures.kucoin.com/api/v1/contracts/{symbol}",
            timeout=TIMEOUT
        ).json()
        return float(r["data"]["openInterest"])
    except Exception as e:
        print("KuCoin error:", e)
        return None


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

    print("Sending payload:")
    print(payload)

    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    print("Status:", r.status_code)
    print("Response:", r.text)


if __name__ == "__main__":
    main()
