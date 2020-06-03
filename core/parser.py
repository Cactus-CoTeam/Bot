from typing import Optional, List

from core.cart import Item


class InterfaceResult:
    def get_result(self, search_result: Optional[List[dict]]):
        """

        :param search_result:
        :return: List [Item]

        something like

        """
        converted_result = List[Item]

        for item in search_result:
            converted_item = Item.make_item(item)
            converted_result.append(converted_item)

        return converted_result


class Parser:
    def __init__(self):
        self.result: Optional[list] = None

    @staticmethod
    def parse(self, search_item: str):
        """This function should take the search item from query

        parameters
        - search_item

        result: Optional[list] = search_result

        """

        raise NotImplementedError()

    def get_result(self):
        return InterfaceResult().get_result(search_result=self.result)
