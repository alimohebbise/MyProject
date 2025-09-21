class Pizzarecipe:
    def __init__(menu, name, price):
        menu.name = name
        menu.price = price

    def microwave(microwavecooking):
        print("The name of the pizza we cooked using the microwave is " + microwavecooking.name)

cooking = Pizzarecipe("Pepperoni", 100)
cooking.microwave()