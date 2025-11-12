import http.client
import json

# ✅ کلید API خودت از پنل sms.ir
API_KEY = "zjtbNOwvnZ1iZ7egDMjDT7KcXIAvDu93Rrcx4chJlW5GYEOz"

# ✅ شماره خط اختصاصی (اگر هنوز خط نداری، 3000505 یا خط تستی sms.ir را قرار بده)
LINE_NUMBER = 3000505

# ✅ شماره موبایل مقصد (شماره واقعی خودت)
MOBILE = "09XXXXXXXXXX"

# ✅ متن پیامک
MESSAGE_TEXT = "سلام! تست وب‌سرویس sms.ir با http.client"

# --- ارسال درخواست ---
conn = http.client.HTTPSConnection("api.sms.ir")

payload = json.dumps({
    "lineNumber": LINE_NUMBER,
    "messageText": MESSAGE_TEXT,
    "mobiles": [MOBILE],
    "sendDateTime": None  # می‌تونی None بذاری تا همون لحظه ارسال شه
})

headers = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

conn.request("POST", "/v1/send/bulk", payload, headers)

res = conn.getresponse()
data = res.read()

print("Status:", res.status)
print("Response:", data.decode("utf-8"))
