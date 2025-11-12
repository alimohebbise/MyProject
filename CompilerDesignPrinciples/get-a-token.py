def get_a_token(input_str):
    state = 0  # حالت اولیه DFA
    token = ""

    for ch in input_str:
        if state == 0:
            if ch.isdigit():
                state = 1
                token += ch
            elif ch.isalpha():
                state = 2
                token += ch
            else:
                return f"خطا: نویسه غیرمجاز {ch}"

        elif state == 1:  # عدد
            if ch.isdigit():
                token += ch
            else:
                return f"عدد: {token}"

        elif state == 2:  # شناسه (identifier)
            if ch.isalnum():
                token += ch
            else:
                return f"شناسه: {token}"

    # اگر ورودی تمام شد
    if state == 1:
        return f"عدد: {token}"
    elif state == 2:
        return f"شناسه: {token}"
    else:
        return "توکن شناسایی نشد"


# تابع اصلی
if __name__ == "__main__":
    input_str = input("رشته ورودی را وارد کنید: ")
    result = get_a_token(input_str)
    print(result)
