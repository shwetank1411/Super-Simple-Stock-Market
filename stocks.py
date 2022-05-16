import decimal
from enum import Enum, auto
from dataclasses import dataclass


class StockType(Enum):
    Common = auto()
    Preferred = auto()


@dataclass(frozen=True)
class Stock:
    stock_symbol: str
    stock_type: StockType
    last_dividend: int
    par_value: int
    fixed_dividend: decimal = 0
