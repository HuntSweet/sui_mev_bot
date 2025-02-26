from decimal import Decimal
from typing import List, Optional, Tuple, Dict
from ..analysis.price_impact import Pool
from .strategies import Strategy
import numpy as np
import logging

logger = logging.getLogger(__name__)

class GradientSearchStrategy(Strategy):
    """
    使用梯度下降搜索最优输入金额的策略
    """
    def __init__(self, learning_rate: float = 0.01, max_iterations: int = 1000, 
                 profit_threshold: Decimal = Decimal('0.1'), 
                 min_gradient: float = 1e-6):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.profit_threshold = profit_threshold  # 达到此利润即可停止
        self.min_gradient = min_gradient  # 最小梯度阈值
        
    async def find_arbitrage_opportunity(self, path_list: List[List[Pool]]) -> List[Dict]:
        """分析所有可能的套利机会"""
        opportunities = []
        
        for path in path_list:
            if len(path) < 2:  # 至少需要两个池子
                continue
                
            amount, profit = self._find_optimal_amount(path)
            if profit > 0:  # 只要有利润就记录
                opportunities.append({
                    "path": path,
                    "input_amount": amount,
                    "expected_profit": profit,
                    "profit_token": path[-1].token_out
                })
                
        return opportunities
        
    def get_initial_amount(self, path: List[Pool]) -> Decimal:
        """获取初始输入金额"""
        pass
        
    async def _find_optimal_amount(self, path: List[Pool]) -> Tuple[Decimal, Decimal]:
        """
        使用梯度下降寻找最优输入金额
        返回: (最优金额, 预期利润)
        """
        # 获取初始输入金额
        current_amount = self.get_initial_amount(path)
        best_amount = current_amount
        best_profit = await self._calculate_profit(path, current_amount)
        
        for i in range(self.max_iterations):
            # 计算当前利润
            current_profit = await self._calculate_profit(path, current_amount)
            
            # 如果找到更好的解，更新最优解
            if current_profit > best_profit:
                best_profit = current_profit
                best_amount = current_amount
                
            # 如果达到利润门槛，提前停止
            if current_profit >= self.profit_threshold:
                break
                
            # 计算梯度
            gradient = await self._calculate_gradient(path, current_amount)
            
            # 如果梯度太小，停止搜索
            if abs(gradient) < self.min_gradient:
                break
                
            # 更新输入金额
            current_amount = max(
                Decimal('0'),
                current_amount + Decimal(str(self.learning_rate * gradient))
            )
            
        return best_amount, best_profit
        
    async def _calculate_gradient(self, path: List[Pool], amount: Decimal, delta: float = 1e-6) -> float:
        """
        计算梯度（数值微分）
        """
        profit_plus = await self._calculate_profit(path, amount + Decimal(str(delta)))
        profit_minus = await self._calculate_profit(path, amount - Decimal(str(delta)))
        
        return float(profit_plus - profit_minus) / (2 * delta)
        
    async def _calculate_profit(self, path: List[Pool], amount_in: Decimal) -> Decimal:
        """计算给定路径和输入金额的预期利润"""
        try:
            current_amount = amount_in
            
            # 沿着路径计算最终输出金额
            for i in range(len(path)):
                pool = path[i]
                current_amount = pool.dex.get_amount_out(
                    current_amount,
                    pool.token_in,
                    pool.token_out
                )
                
            # 计算利润
            return current_amount - amount_in
            
        except Exception as e:
            logger.error(f"计算利润时发生错误: {e}")
            return Decimal('0')
            