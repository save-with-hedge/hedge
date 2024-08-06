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

    def to_dict(self):
        return {
            "book": self.book,
            "time_placed": self.time_placed,
            "time_closed": self.time_closed,
            "odds": self.odds,
            "wager": self.wager,
            "result": self.result.value,
            "earnings": self.earnings,
            "selection": self.selection,
            "sport": self.sport,
            "bet_type": self.bet_type,
            "parlay_details": self.parlay_details,
        }
