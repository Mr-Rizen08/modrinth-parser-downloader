import json
from abc import ABC, abstractmethod
import pandas as pd


class SaverBase(ABC):
    key: str

    @abstractmethod
    def  saver(self, data: list | None , name):
        pass

    @classmethod
    def available (cls) -> list[str]:
        return [i.key for i in cls.__subclasses__()]

    @classmethod
    def create1(cls, key: str):
        for i in cls.__subclasses__():
            if i.key == key:
                return i
        raise ValueError(f"Такого формата {key} у нас нет ")

    @classmethod
    def create2(cls, key: str):
        savers = {sub.key: sub for sub in cls.__subclasses__()}
        if key  not in savers:
            raise ValueError(f"Такого формата {key} у нас нет" )
        return savers[key]() # <XlsxSaver object>: готовый объект, как построенный по чертежу дом

class JsonSaver(SaverBase):
    def saver(self, data: list | None, name):
        with open(f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Done")


class XlsxSaver(SaverBase):
    def saver(self, data: list | None, name):
        df = pd.DataFrame(data)
        df.to_excel(f"{name}.xlsx", index=False)
        print("Done")




class SaveToFile:
    def __init__(self, saver: SaverBase, data: list | None):
        self.saver = saver
        self.data = data

    def save(self, name: str):
        self.saver.saver(self.data, name)


