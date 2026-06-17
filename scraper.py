import requests

TOPIC = "akshit-moneycontrol-stocks"

print("Sending test notification...")

r = requests.post(
    f"https://ntfy.sh/{TOPIC}",
    data="Hello from GitHub Actions!".encode("utf-8")
)

print("Status code:", r.status_code)
print("Response:", r.text)

print("Done")
