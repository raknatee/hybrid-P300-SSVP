
from dataclasses import dataclass
from typing import Union

@dataclass(init=True)
class FP:
    freq:float
    phare:float

    def __init__(self,freq:float,phare:float) -> None:
        self.freq = freq 
        self.phare = phare

wave_data:list[Union[FP,None]] = [
    FP(12.4, 0),
    FP(12.6, .35),
    FP(12.8, .7),
    FP(13, 1.05),
    FP(13.2, 1.4),
    FP(13.4, 1.75),
    FP(13.6, .1),
    FP(13.8, .45),
    None, None,
    FP(14, .8),
    FP(14.2, 1.15),
]