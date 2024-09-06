from dataclasses import dataclass
from enum import Enum


class Result(Enum):
    win = "win"
    loss = "loss"
    push = "push"


@dataclass
class HedgeBetslip:
    book: str
    time_placed: str
    time_closed: str
    odds: str
    wager: float
    result: Result
    earnings: float

    # single betslips only
    selection: str
    sport: str
    bet_type: str

    # parlay betslips only
    parlay_details: str

    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
