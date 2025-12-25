def MyOstadCode():
       for i in range(3,100):
           print(i-1)

def MyOstadCode2():
    for i in range(3, 100):
        print(i - 2)

for i in range(1,100):
    if i == 1:
        print(1)
    elif i == 2:
        i = 1
        print(i)
    else:
        i -= 1     # مقدار قبلی
        i += i + 1 # جمع مقدار قبلی با مقدار فعلی

        print(i)



