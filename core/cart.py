from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Item:
    item_id: int = None
    item_type: str = None
    price: float = None
    count: int = None

    @staticmethod
    def make_item(item: dict):
        """
        implement the transformation from string to Item instance
        :return:
        """
        pass


class ShoppingCart:
    def __init__(self, user_id):
        self.user_id: np.unit64 = user_id
        self.items: List[Item]

    @staticmethod
    def add_item(item: Item):
        pass

    @staticmethod
    def remove_item(item: Item):
        pass

    def remove_all(self):
        self.items = None

    @property
    def show_cart(self):
        return self.items
