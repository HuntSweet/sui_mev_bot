from decimal import Decimal
from typing import List, Tuple
from ..analysis.price_impact import Pool
from .arbitrage import Strategy
import math
from scipy.optimize import minimize

class ThreeV2PoolArbitrageStrategy(Strategy):
    """
    三池子套利策略
    基于数值优化方法求解最优输入金额
    """
    
    def __init__(self):
        self.gas_cost = Decimal('0.001')
        
    async def find_arbitrage_opportunity(self, path_list: List[List[Pool]]):
        """分析三个池子之间的套利机会"""
        for path in path_list:
            if len(path) != 3:  # 只处理三池子路径
                continue
                
            pool1, pool2, pool3 = path[0], path[1], path[2]
            if not all(p.dex.dex_type == "v2" for p in [pool1, pool2, pool3]):
                continue
            
            optimal_amounts = self._calculate_optimal_amounts(pool1, pool2, pool3)
            if optimal_amounts:
                profit = self._calculate_profit(pool1, pool2, pool3, optimal_amounts)
                if profit > self.gas_cost:
                    return {
                        "path": path,
                        "input_amounts": optimal_amounts,
                        "expected_profit": profit
                    }
        return None
        
    def _calculate_optimal_amounts(self, pool1: Pool, pool2: Pool, pool3: Pool) -> List[Decimal]:
        """
        计算三个池子的最优输入金额
        使用数值优化方法求解
        """
        try:
            def objective(amounts):
                # 转换为Decimal以保持精度
                x1, x2 = map(Decimal, amounts)
                
                # 计算每个池子的输出量（考虑手续费）
                fee1 = Decimal('1') - pool1.fee
                fee2 = Decimal('1') - pool2.fee
                fee3 = Decimal('1') - pool3.fee
                
                # 第一个池子的输出
                y1 = (pool1.amount1 * x1 * fee1) / (pool1.amount0 + x1)
                
                # 第二个池子的输出
                y2 = (pool2.amount1 * y1 * fee2) / (pool2.amount0 + y1)
                
                # 第三个池子的输出
                y3 = (pool3.amount1 * y2 * fee3) / (pool3.amount0 + y2)
                
                # 返回负的利润（因为minimize寻找最小值）
                return float(-(y3 - x1))
                
            # 初始猜测值
            initial_guess = [1.0, 1.0]
            
            # 约束条件：输入金额必须为正
            bounds = [(0, None), (0, None)]
            
            # 使用scipy的optimize.minimize进行优化
            result = minimize(objective, initial_guess, bounds=bounds)
            
            if result.success:
                return [Decimal(str(x)) for x in result.x]
            return None
            
        except Exception as e:
            print(f"计算最优输入金额时发生错误: {e}")
            return None
            
    def _calculate_profit(self, pool1: Pool, pool2: Pool, pool3: Pool, amounts: List[Decimal]) -> Decimal:
        """计算三池子套利的预期利润"""
        try:
            amount_in = amounts[0]
            
            # 第一个池子的输出
            amount_out1 = pool1.dex.get_amount_out(amount_in)
            
            # 第二个池子的输出
            amount_out2 = pool2.dex.get_amount_out(amount_out1)
            
            # 第三个池子的输出
            final_amount = pool3.dex.get_amount_out(amount_out2)
            
            return final_amount - amount_in
            
        except Exception as e:
            print(f"计算利润时发生错误: {e}")
            return Decimal('0') 