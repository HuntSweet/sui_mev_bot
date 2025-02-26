from typing import Dict, Tuple
from decimal import Decimal
from abc import ABC, abstractmethod
from typing import TypedDict, List


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

class TransactionFilter(ABC):
    @abstractmethod
    def filter(self, transaction: Dict) -> List[Dict]:
        pass

class TransactionFilters:
    def __init__(self, filters:List[TransactionFilter]):
        self.filters = filters
        
    def add_filter(self, filter:TransactionFilter):
        self.filters.append(filter)
        
    def filter_transactions(self, transactions: List[Dict]) -> List[Dict]:
        for filter in self.filters:
            transactions = filter.filter(transactions)
        return transactions
    
    
class PriceImpactFilter:
    @abstractmethod
    def analyze_price_impact(self, transaction: Dict) -> Tuple[Decimal, Dict]:
        pass

class PriceImpactAnalyzer:
    def __init__(self):
        self.price_cache = {}  # 缓存价格数据
        
    async def analyze_price_impact(self, transaction: Dict) -> Tuple[Decimal, Dict]:
        """
        分析交易对价格的影响
        
        返回:
            - price_impact: 价格影响百分比
            - affected_pairs: 受影响的交易对信息
        """
        try:
            # 解析交易数据
            token_in, token_out, amount = self._parse_transaction(transaction)
            
            # 获取交易前价格
            price_before = await self._get_price(token_in, token_out)
            
            # 计算价格影响
            price_after = self._calculate_new_price(price_before, amount)
            price_impact = (price_after - price_before) / price_before
            
            affected_pairs = {
                "token_in": token_in,
                "token_out": token_out,
                "price_before": price_before,
                "price_after": price_after
            }
            
            return price_impact, affected_pairs
            
        except Exception as e:
            print(f"分析价格影响时发生错误: {e}")
            return Decimal(0), {}
            
    def _parse_transaction(self, transaction: Dict) -> Tuple[str, str, Decimal]:
        """
        解析交易数据
        """
        # TODO: 实现交易数据解析逻辑
        return "", "", Decimal(0)
        
    async def _get_price(self, token_in: str, token_out: str) -> Decimal:
        """
        获取当前价格
        """
        # TODO: 实现价格获取逻辑
        return Decimal(0) 