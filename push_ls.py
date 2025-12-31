import requests
from datetime import datetime

TIMEOUT = 10
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbw1buTKxm-B-Xfp1XS-b70a7a2zE08cE6HmR7O6Mc8bN3iGiqpqT2k6DJbB1oFRZofe/exec"

# ---------------------------
# BINANCE LONG / SHORT
# ---------------------------
def get_binance_ls_ratio(symbol="AIOTUSDT", period="1h"):
    url = "https://fapi.binance.com/futures/data/topLongShortAccountRatio"
    params = {
        "symbol": symbol,
        "period": period,
        "limit": 1
    }

    try:
        resp = requests.get(url, params=params, timeout=10)

        # HTTP error (403 / 429 / 5xx)
        if resp.status_code != 200:
            print(f"[WARN] Binance HTTP {resp.status_code}")
            return {
                "ratio": None,
                "long": None,
                "short": None
            }

        data = resp.json()

        # Binance sometimes returns empty list
        if not isinstance(data, list) or len(data) == 0:
            print("[WARN] Binance returned empty data")
            return {
                "ratio": None,
                "long": None,
                "short": None
            }

        row = data[-1]

        # Validate required keys
        if not all(k in row for k in ("longShortRatio", "longAccount", "shortAccount")):
            print("[WARN] Missing expected fields in Binance response")
            return {
                "ratio": None,
                "long": None,
                "short": None
            }

        return {
            "ratio": round(float(row["longShortRatio"]), 2),
            "long": round(float(row["longAccount"]) * 100, 2),
            "short": round(float(row["shortAccount"]) * 100, 2)
        }

    except Exception as e:
        print(f"[ERROR] Binance LS fetch failed: {e}")
        return {
            "ratio": None,
            "long": None,
            "short": None
        }


# ---------------------------
# BUILD DATA STRUCTURE
# ---------------------------
def build_ls_payload(symbol="AIOTUSDT"):
    timeframes = {
        "5m": "5m",
        "30m": "30m",
        "1h": "1h",
        "4h": "4h",
        "1d": "1d"
    }

    rows = []

    for label, tf in timeframes.items():
        try:
            r = get_binance_ls_ratio(symbol, tf)
            rows.append({
                "timeframe": label,
                "ratio": r["ratio"],
                "long": r["long"],
                "short": r["short"]
            })
        except Exception as e:
            rows.append({
                "timeframe": label,
                "ratio": None,
                "long": None,
                "short": None
            })
            print(f"[WARN] {label}: {e}")

    return {
        "type": "ls",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "data": rows
    }


# ---------------------------
# SEND TO GOOGLE SHEETS
# ---------------------------
def push_to_google_sheet(payload):
    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    print("Status:", r.status_code)
    print("Response:", r.text)


# ---------------------------
# MAIN
# ---------------------------
def main():
    payload = build_ls_payload("AIOTUSDT")
    print("Payload Preview:\n", payload)
    push_to_google_sheet(payload)


if __name__ == "__main__":
    main()
