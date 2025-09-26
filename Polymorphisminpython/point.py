class Point:
    def __init__(self):
        pass

    def disign(self):
        v = "**********"
        return v

class Subpoint(Point):
    def __init__(self):
        super().__init__()

    def disign(self):
        m = "***************"
        return(m)

c = Subpoint()

print(c.disign())
print(c.disign())

