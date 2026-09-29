import numpy as np

class Ingredient:
    def __init__(self, name: str):
        self.__name = name

    @property
    def Name(self) -> str:
        return self.__name

    def __str__(self) -> str:
        return self.Name

class Menu:
    def __init__(self, name: str, price: np.int64, ingredients: dict[Ingredient, np.int64] = {}):
        self.__name = name
        self.__price = price
        self.__ingredients = ingredients

    @property
    def Name(self) -> str:
        return self.__name

    @property
    def Price(self) -> np.int64:
        return self.__price

    @property
    def Ingredients(self) -> dict[Ingredient, np.int64]:
        return self.__ingredients

    def __str__(self) -> str:
        return f"{self.Name} - ${self.Price // 100}.{self.Price % 100}"

    def __len__(self) -> int:
        return len(self.Name)

    def displayIngredients(self) -> str:
        res = f"{self}\nRequires"
        for i in self.Ingredients:
            res += f"\n {i}"
        return res