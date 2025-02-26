from typing import Dict, List, Optional
from decimal import Decimal
from ..config import Config
from abc import ABC, abstractmethod
from ..analysis.price_impact import Pool
from ..common.event_bus import EventBus

class Strategy(ABC):
    @abstractmethod
    async def find_arbitrage_opportunity(self, path_list: List[List[Pool]]):
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
            if opportunities:
                # 将机会发送给tx_executor去执行交易
                self.event_bus.emit("arbitrage_opportunity",opportunities)



class ArbitrageStrategy(Strategy):
    def __init__(self, config: Config,event_bus:EventBus):
        self.config = config
        self.event_bus = event_bus
        
    async def find_arbitrage_opportunity(self, path_list: List[List[Pool]]):
        """
        基于价格影响寻找套利机会
        
        返回:
            套利路径和预期收益
        """
        try:
            # 计算最优套利路径
            for path in path_list:
                if self._validate_arbitrage(path):
                    self.event_bus.emit("arbitrage_opportunity", path)
            
        except Exception as e:
            print(f"寻找套利机会时发生错误: {e}")
            return None
            
    async def _calculate_best_path(self, price_impacts: Dict) -> Dict:
        """
        计算最优套利路径
        """
        # TODO: 实现套利路径计算逻辑
        return {}
        
    def _validate_arbitrage(self, path: Dict) -> bool:
        """
        验证套利是否满足条件
        """
        if not path:
            return False
            
        # 检查最小利润阈值
        if path.get("expected_profit", 0) < self.config.MIN_PROFIT_THRESHOLD:
            return False
            
        # 检查滑点限制
        if path.get("estimated_slippage", 1) > self.config.MAX_SLIPPAGE:
            return False
            
        return True 