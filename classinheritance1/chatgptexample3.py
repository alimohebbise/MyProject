
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print("Some generic animal sound")


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def make_sound(self):
        print("woof!")

    def fetch(self):
        print(f"{self.name} is fetching the ball!")


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def make_sound(self):
        print("Meow!")

    def scratch(self):
        print(f"{self.name} is scratching the sofa!")


class Bird(Animal):
    def __init__(self, name, can_fly=False):
        super().__init__(name)
        self.can_fly = can_fly

    def make_sound(self):
        print("Tweet!")

    def fly(self):
        if self.can_fly:
            print(f"{self.name} can flying!")
        else:
            print(f"{self.name} cannot fly.")


dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Misty", "Gray")
bird = Bird("Kiwi", can_fly=False)  # چرا ما اینجا مقدار دهیش کردیم؟


print(dog.name, dog.breed)
print(cat.name, cat.color)
print(bird.name, bird.can_fly)      # مفسر میاد و میبینه از روی این باید شی را پیدا بکنه و سوال پیش میائ که ما چرا مقدارشا تو print نذاشتیم


dog.make_sound()
cat.make_sound()
bird.make_sound()

dog.fetch()
cat.scratch()
bird.fly()




