def rooroo(x):
    if x == 1:
        return 1
    else:
        return (x * rooroo(x - 1))
dilili = 9
print("dilili: ", dilili, "rooroo: ", rooroo(dilili))