def switch(case):
    if case == 1:
        return "This is case one."
    elif case == 2:
        return "This is case two."
    else:
        return "This is the default case."
print(switch(1))  # Output: This is case one.
print(switch(3))  # Output: This is the default case.