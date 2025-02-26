from typing import TypedDict
from decimal import Decimal

class Dex(TypedDict):
    name: str
    router: str
    dex_type: str
    def get_amount_in(self, amount_out: Decimal,token_in:str,token_out:str) -> Decimal:
        pass
    
    def get_amount_out(self, amount_in: Decimal,token_in:str,token_out:str) -> Decimal:
        pass
    
class Pool(TypedDict):
    address: str
    token0: str
    token1: str
    dex: Dex
    amount0: Decimal
    amount1: Decimal
    fee: Decimal
    token_in: str
    token_out: str