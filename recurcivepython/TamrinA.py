def calk_factorial(x):
    if x == 1:
        return 1
    else:
        return (x * calk_factorial(x - 1))
num = 6
print("The factorial of", num, "is", calk_factorial(num))

"""
def rooroo(x):
    if x == 0:
        return 0
    else:
        return (x * rooroo(x - 1))
dilili = 9
print("dilili: ", dilili, "rooroo: ", rooroo(dilili))
"""