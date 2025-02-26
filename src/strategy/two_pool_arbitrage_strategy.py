from decimal import Decimal
from typing import Tuple, List
from ..analysis.price_impact import Pool
from .strategies import Strategy
import math
import logging

logger = logging.getLogger(__name__)

class TwoPoolArbitrageStrategy(Strategy):
    """
    两池子套利策略，通过求导计算最优输入金额
    基于 Uniswap V2 的 x * y = k 公式
    """
    
    def __init__(self,profit_threshold:Decimal=Decimal('0')):
        self.profit_threshold = profit_threshold 
        
    async def find_arbitrage_opportunity(self, path_list: List[List[Pool]]):
        """分析两个池子之间的套利机会"""
        for path in path_list:  
            if len(path) != 2:  # 只处理两池子路径
                continue
                
            pool1, pool2 = path[0], path[1]
            if pool1.dex.dex_type != "v2" or pool2.dex.dex_type != "v2":
                continue
            
            optimal_amount = self._calculate_optimal_amount(pool1, pool2)
            
            if optimal_amount > 0:
                profit = self._calculate_profit(pool1, pool2, optimal_amount)
                if profit > self.profit_threshold:
                    return {
                        "path": path,
                        "input_amount": optimal_amount,
                        "expected_profit": profit,
                        "profit_token": pool2.token_out
                    }
        return None
        
    def _calculate_optimal_amount(self, pool1: Pool, pool2: Pool) -> Decimal:
        """
        计算最优输入金额，考虑手续费
        通过求导 d(profit)/d(x) = 0 来获得最大利润点
        """
        try:
            x1, y1 = pool1.amount0, pool1.amount1
            x2, y2 = pool2.amount0, pool2.amount1
            
            # 考虑手续费的系数
            fee1 = Decimal('1') - pool1.fee
            fee2 = Decimal('1') - pool2.fee
            
            # 修正后的最优输入量公式
            # dx = sqrt((x1 * x2 * y1 * fee1 * fee2) / y2) - x1
            numerator = Decimal(x1 * x2 * y1 * fee1 * fee2)
            denominator = Decimal(y2)
            
            optimal_amount = Decimal(math.sqrt(numerator / denominator)) - Decimal(x1)
            return max(optimal_amount, Decimal('0'))
            
        except Exception as e:
            logger.error(f"计算最优输入金额时发生错误: {e}")
            return Decimal('0')
            
    def _calculate_profit(self, pool1: Pool, pool2: Pool, amount_in: Decimal) -> Decimal:
        """计算给定输入金额的预期利润"""
        try:
            # 第一个池子的输出
            amount_out1 = pool1.dex.get_amount_out(amount_in,pool1.token_in,pool1.token_out)
            
            # 第二个池子的输出
            final_amount = pool2.dex.get_amount_out(amount_out1,pool2.token_in,pool2.token_out)
            
            # 计算利润
            return final_amount - amount_in
            
        except Exception as e:
            logger.error(f"计算利润时发生错误: {e}")
            return Decimal('0') 