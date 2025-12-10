def GetNextId(text):
    i = 0
    n = len(text)

    # حالت 0: باید با حرف شروع شود
    if i >= n or not text[i].isalpha():
        return -1, i   # شناسه نامعتبر
    i += 1

    # حالت 1: ادامه شناسه (حرف یا عدد)
    while i < n and text[i].isalnum():
        i += 1

    # اگر یک کاراکتر جلوتر رفتیم، آن را پس می‌دهیم
    return 0, i        # شناسه معتبر، i محل توقف خواندن است


# مثال استفاده
result, pos = GetNextId("abc123+5")
print(result, pos)   # خروجی: 0, 6  یعنی abc123 شناسه بوده
