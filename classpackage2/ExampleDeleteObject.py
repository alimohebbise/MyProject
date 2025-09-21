class Pizzarecipe:
  def __init__(menu, name, price):
    menu.name = name
    menu.price = price

  def microwave(menu):
      print("The name of the pizza we cooked using the microwave is " + menu.name)

cooking = Pizzarecipe("Pepperoni", 100)

