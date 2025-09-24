from abc import abstractmethod


class Tools:
    @abstractmethod
    def beavior_of_tools(ABC):
        pass

class Broom(Tools):                     # جارو
    def beavior_of_tools(self):         # رفتار ابزارها
        return "Cleanes Spaces."        # مکانها را تمیز میکند

class Sandpaper(Tools):                 # سمباده
    def beavior_of_tools(self):
        return "Smooth surfaces."       # سطوح را نرم میکند

class Hammer(Tools):                         # چکش
    def beavior_of_tools(self):
        return "Strikes objects together."   # اشیاء را به هم میکوبد

class Screwdriver(Tools):
    def beavior_of_tools(self):
        return "Opens and closes screws."

class Sicssors(Tools):
    def beavior_of_tools(self):
        return "Cats materials."

class Brush(Tools):
    def beavior_of_tools(self):
        return "Cleanes surfaces and dishes."

class Teapot(Tools):
    def beavior_of_tools(self):
        return "Brews tea."

class Refrigerator(Tools):
    def beavior_of_tools(self):
        return "Preserves food freshness."

class Heater(Tools):
    def beavior_of_tools(self):
        return "Warms up spaces."

class Washing_machine(Tools):
    def beavior_of_tools(self):
        return "Cleans clothes."

Tools = [Broom(), Sandpaper(), Hammer(), Screwdriver(), Sicssors(), Brush(), Teapot(), Refrigerator(), Heater(), Washing_machine()]
for tool in Tools:
    print(tool.beavior_of_tools())