class Pizzarecipe:
  def __init__(menu, name, price):
      menu.name = name
      menu.price = price

  def microwave(microwavecooking):
      print("The name of the pizza we cooked using the microwave is " + microwavecooking.price)

cooking = Pizzarecipe("Cooking", 100)

cooking.price = 200

print(cooking.price)