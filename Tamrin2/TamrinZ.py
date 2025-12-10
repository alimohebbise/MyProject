import dis

def test():
    x = 10
    y = x + 5
    return y

dis.dis(test)
