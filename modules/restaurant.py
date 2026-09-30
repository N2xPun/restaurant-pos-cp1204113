import numpy as np

class Ingredient:
    def __init__(self, name: str):
        self.__name = name

    @property
    def Name(self) -> str:
        return self.__name

    def __hash__(self) -> int:
        return hash(self.__name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ingredient):
            return other.__name == self.__name
        elif isinstance(other, str):
            return other == self.__name
        return False

    def __lt__(self, other: Ingredient | str) -> bool:
        if isinstance(other, Ingredient):
            return self.__name < other.__name
        else:
            return self.__name < other

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
        return f"{self.__name} - ${self.__price // 100}.{self.__price % 100}"

    def __hash__(self) -> int:
        return hash(self.__name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Menu):
            return other.__name == self.__name
        elif isinstance(other, str):
            return other == self.__name
        return False

    def __lt__(self, other: Menu | str) -> bool:
        if isinstance(other, Menu):
            return self.__name < other.__name
        else:
            return self.__name < other

    def displayIngredients(self) -> str:
        res = f"{self}\nRequires"
        for i in self.__ingredients:
            res += f"\n {i}"
        return res