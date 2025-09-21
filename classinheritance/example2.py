Class Animal:
  def __init__(self, name):
    self.name = name

  def make_sound(self):
      print("Some generic animal sound")

Create Dog(Animal)
   def __init__(self, name, breed):
    super().__init__(name)