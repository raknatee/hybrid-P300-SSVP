from __future__ import annotations
from typing import Any, Optional, Union


class DataBufferManager:
    buffer:Buffer

    @classmethod
    def get_instance(cls)->Buffer:
        if(not hasattr(cls,'buffer')):
            cls.buffer = Buffer()
        return cls.buffer

class Buffer(list):

    def __init__(self):
        list.__init__(self)
    def add(self,data:dict[str,Any]):
        super().append(data)

    def get_and_clear(self)->list[dict[str,Any]]:

        copy_of_myself = [*self]
        self.clear()
        return copy_of_myself