# Create a Parent Class
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print("Some generic animal sound")

# Create a Child Class (Dog)
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # Call parent constructor
        self.breed = breed     # New property

    def make_sound(self):      # Override method
        print("Woof!")

    def fetch(self):           # New method
        print(f"{self.name} is fetching the ball!")

# Create a Child Class (Cat)
class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def make_sound(self):
        print("Meow!")

    def scratch(self):
        print(f"{self.name} is scratching the sofa!")

# Create a Child Class (Bird)
class Bird(Animal):
    def __init__(self, name, can_fly=True):
        super().__init__(name)
        self.can_fly = can_fly

    def make_sound(self):
        print("Tweet!")

    def fly(self):
        if self.can_fly:
            print(f"{self.name} is flying!")
        else:
            print(f"{self.name} cannot fly.")

# Test the classes
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Misty", "Gray")
bird = Bird("Kiwi", can_fly=True)   # در اینجا می خواهیم مقدار را به True تغییر بدیم تا ببینیم چه اتفاقی می افتد

# Inherited property
print(dog.name, dog.breed)
print(cat.name, cat.color)
print(bird.name, bird.can_fly)

# Overridden methods
dog.make_sound()
cat.make_sound()
bird.make_sound()

# Child-specific methods
dog.fetch()
cat.scratch()
bird.fly()


   # دیدیم که نتیجه کد عوض شد و به جای
   # Kiwi is not flying!
   # برای ما چاپ شد
   # Kiwi is flying!