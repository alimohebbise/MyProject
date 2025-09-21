class Person:
  def __init__(self, name, age):
      self.name = name
      self.age = age

  def funcperson(self):
    print("My name is " + self.name)

p1 = Person("Ali", 23)
p1.funcperson()