from typing import Dict, List, TypedDict
from decimal import Decimal
from ..config import Config
from abc import ABC, abstractmethod
from ..analysis.price_impact import Pool
from ..common.event_bus import EventBus 

class Opportunity(TypedDict):
    path: List[Pool]
    input_amount: Decimal
    expected_profit: Decimal
    profit_token: str
    
class Strategy(ABC):
    @abstractmethod
    async def find_arbitrage_opportunity(self, path_list: List[List[Pool]]) -> List[Opportunity]:
        pass    


class Strategies:
    def __init__(self,config:Config,event_bus:EventBus):
        self.config = config
        self.event_bus = event_bus
        self.strategies = []
        
    def add_strategy(self,strategy:Strategy):
        self.strategies.append(strategy)
        
    async def find_arbitrage_opportunities(self,path_list:List[List[Pool]]):
        for strategy in self.strategies:
            opportunities = await strategy.find_arbitrage_opportunity(path_list)
            # 对每个找到的机会都发送事件
            for opportunity in opportunities:
                self.event_bus.emit("arbitrage_opportunity", opportunity)


    