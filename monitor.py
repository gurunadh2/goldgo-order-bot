import requests
import time

# ===== API =====
url = "https://client.goldgo.cc/v1/job/sell_list"

headers = {
    "device-id": "17736400115626711840",
    "user-id": "142045",
    "user-agent": "Mozilla/5.0",
    "content-type": "application/json"
}

# ===== TELEGRAM =====
BOT_TOKEN = "8643412865:AAFjAZbxdhT7AC9J0yhyGNflJQ-J06MzHNw"
CHAT_ID = "6622226383"

# ===== SETTINGS =====
THRESHOLD = 20000
CHECK_INTERVAL = 0.8   # less than 1 second

alerted_ranges = set()


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


print("🚀 GoldGo Order Monitor Started")

while True:

    try:

        response = requests.post(url, headers=headers)

        data = response.json()

        orders = data.get("data", [])

        for order in orders:

            min_amt = int(order.get("min", 0))
            max_amt = int(order.get("max", 0))
            rate = order.get("rate")
            count = int(order.get("count", 0))

            key = f"{min_amt}-{max_amt}"

            if count > 0 and min_amt >= THRESHOLD and key not in alerted_ranges:

                msg = f"""
🚨 NEW ORDER AVAILABLE

💰 Range: {min_amt} - {max_amt}
🎁 Reward: {rate}
📦 Orders Available: {count}

⚡ Status: BUY AVAILABLE
"""

                print(msg)

                send_telegram(msg)

                alerted_ranges.add(key)

        print("Checking orders...")

    except Exception as e:

        print("Error:", e)

    time.sleep(CHECK_INTERVAL)