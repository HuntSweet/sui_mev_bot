from typing import List, Dict, Set, Optional
from decimal import Decimal
import logging
from dataclasses import dataclass
from ..analysis.price_impact import Pool
from ..db.db import DB
logger = logging.getLogger(__name__)

@dataclass
class PathConfig:
    max_path_length: int = 3  # 最大路径长度
    min_liquidity: Decimal = Decimal('1000')  # 最小流动性要求
    custom_paths: List[List[str]] = None  # 自定义路径 [["USDC","SUI","USDT"]]
    start_tokens: List[str] = None  # 指定起始代币
    blacklist_tokens: Set[str] = None  # 黑名单代币
    blacklist_dexes: Set[str] = None  # 黑名单DEX

class PathFinder:
    def __init__(self, config: PathConfig, db: DB):
        self.config = config
        self.pool_graph: Dict[str, Dict[str, List[Pool]]] = {}  # token_from -> token_to -> [pools]
        self.db = db
        # 初始化时从数据库加载所有池子并构建图
        self._build_graph()
        
    def _build_graph(self):
        """从数据库加载所有池子并构建图"""
        self.pool_graph.clear()
        all_pools = self.db.get_all_pools()
        for pool in all_pools:
            self.add_pool(pool)
            
    def add_pool(self, pool: Pool):
        """添加池子到图中"""
        
        # 添加正向边
        if pool.token0 not in self.pool_graph:
            self.pool_graph[pool.token0] = {}
        if pool.token1 not in self.pool_graph[pool.token0]:
            self.pool_graph[pool.token0][pool.token1] = []
        self.pool_graph[pool.token0][pool.token1].append(pool)
        
        # 添加反向边
        if pool.token1 not in self.pool_graph:
            self.pool_graph[pool.token1] = {}
        if pool.token0 not in self.pool_graph[pool.token1]:
            self.pool_graph[pool.token1][pool.token0] = []
        self.pool_graph[pool.token1][pool.token0].append(pool)
        
    def find_paths(self, affected_pools: List[Pool]) -> List[List[Pool]]:
        """
        根据受影响的池子寻找可能的套利路径
        从数据库中的所有池子中搜索与受影响池子相关的套利路径
        """
        paths = []
        affected_tokens = set()
        
        # 收集受影响池子中的所有代币
        for pool in affected_pools:
            affected_tokens.add(pool.token0)
            affected_tokens.add(pool.token1)
            
        # 如果有自定义路径，检查是否与受影响代币相关
        if self.config.custom_paths:
            for token_path in self.config.custom_paths:
                # 检查路径是否包含受影响的代币
                if any(token in affected_tokens for token in token_path):
                    path = self._build_path_from_tokens(token_path)
                    if path:
                        paths.append(path)
            if paths:  # 如果找到了相关的自定义路径，直接返回
                return paths
            
        # 从受影响的代币开始搜索路径
        for start_token in affected_tokens:
            if self._is_blacklisted_token(start_token):
                continue
            
            # 从每个受影响的代币开始搜索
            self._find_cycles(
                start_token=start_token,
                current_token=start_token,
                current_path=[],
                visited=set(),
                paths=paths,
                affected_pools=set(affected_pools)  # 转换为set以提高查找效率
            )
            
        return paths
        
    def _find_cycles(self, start_token: str, current_token: str, 
                     current_path: List[Pool], visited: Set[str], 
                     paths: List[List[Pool]], affected_pools: Set[Pool]):
        """使用DFS寻找套利环路，优先考虑受影响的池子"""
        
        # 如果路径长度达到上限，只检查是否可以回到起点
        if len(current_path) >= self.config.max_path_length:
            if start_token in self.pool_graph.get(current_token, {}):
                # 找到一条回到起点的边
                for pool in self.pool_graph[current_token][start_token]:
                    if not self._is_blacklisted_pool(pool):
                        # 确保路径中至少包含一个受影响的池子
                        if any(p in affected_pools for p in current_path) or pool in affected_pools:
                            paths.append(current_path + [pool])
            return
            
        # 继续搜索
        for next_token in self.pool_graph.get(current_token, {}):
            if self._is_blacklisted_token(next_token):
                continue
                
            # 对于非最后一步，避免访问已访问的节点
            if next_token != start_token and next_token in visited:
                continue
                
            # 优先考虑受影响的池子
            pools = self.pool_graph[current_token][next_token]
            # 将受影响的池子排在前面
            sorted_pools = sorted(pools, 
                                key=lambda p: p in affected_pools, 
                                reverse=True)
            
            for pool in sorted_pools:
                if self._is_blacklisted_pool(pool):
                    continue
                    
                if not self._check_pool_liquidity(pool):
                    continue
                    
                # 继续搜索
                visited.add(next_token)
                current_path.append(pool)
                
                self._find_cycles(
                    start_token=start_token,
                    current_token=next_token,
                    current_path=current_path,
                    visited=visited,
                    paths=paths,
                    affected_pools=affected_pools
                )
                
                current_path.pop()
                visited.remove(next_token)
                
    def _build_path_from_tokens(self, token_path: List[str]) -> Optional[List[Pool]]:
        """根据代币序列构建池子路径"""
        path = []
        for i in range(len(token_path) - 1):
            token_from = token_path[i]
            token_to = token_path[i + 1]
            
            # 检查是否存在连接这两个代币的池子
            if token_from not in self.pool_graph or token_to not in self.pool_graph[token_from]:
                logger.warning(f"找不到连接 {token_from} 和 {token_to} 的池子")
                return None
                
            # 选择流动性最大的池子
            best_pool = max(
                self.pool_graph[token_from][token_to],
                key=lambda p: p.amount0 + p.amount1
            )
            path.append(best_pool)
            
        return path
        
    def _is_blacklisted_token(self, token: str) -> bool:
        """检查代币是否在黑名单中"""
        return (self.config.blacklist_tokens and 
                token in self.config.blacklist_tokens)
                
    def _is_blacklisted_pool(self, pool: Pool) -> bool:
        """检查池子是否在黑名单DEX中"""
        return (self.config.blacklist_dexes and 
                pool.dex.name in self.config.blacklist_dexes)
                
    def _check_pool_liquidity(self, pool: Pool) -> bool:
        """检查池子是否满足最小流动性要求"""
        total_liquidity = pool.amount0 + pool.amount1
        return total_liquidity >= self.config.min_liquidity 
