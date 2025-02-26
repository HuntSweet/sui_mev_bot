import pytest
from decimal import Decimal
from typing import List, Set
from src.path.path_finder import PathFinder, PathConfig
from src.analysis.price_impact import Pool
from src.db.db import DB

class MockPool:
    def __init__(self, address: str, token0: str, token1: str, amount0: Decimal, amount1: Decimal):
        self.address = address
        self.token0 = token0
        self.token1 = token1
        self.amount0 = amount0
        self.amount1 = amount1
        self.dex = MockDex()

class MockDex:
    def __init__(self):
        self.name = "mock_dex"

class MockDB:
    def __init__(self, pools: List[Pool]):
        self.pools = pools
        
    def get_all_pools(self) -> List[Pool]:
        return self.pools

@pytest.fixture
def mock_pools():
    return [
        MockPool("0x1", "USDC", "ETH", Decimal("1000"), Decimal("1")),
        MockPool("0x2", "ETH", "USDT", Decimal("1"), Decimal("1000")),
        MockPool("0x3", "USDT", "USDC", Decimal("1000"), Decimal("1000")),
        MockPool("0x4", "BTC", "ETH", Decimal("1"), Decimal("10")),
    ]

@pytest.fixture
def path_finder(mock_pools):
    config = PathConfig(
        max_path_length=3,
        min_liquidity=Decimal("100"),
        custom_paths=[["USDC", "ETH", "USDT", "USDC"]],
        blacklist_tokens={"SAFEMOON"},
        blacklist_dexes=set()
    )
    db = MockDB(mock_pools)
    return PathFinder(config, db)

def test_find_paths_with_custom_path(path_finder):
    # 测试使用自定义路径
    affected_pools = [
        MockPool("0x1", "USDC", "ETH", Decimal("1000"), Decimal("1"))
    ]
    paths = path_finder.find_paths(affected_pools)
    
    assert len(paths) > 0
    assert len(paths[0]) == 3  # USDC->ETH->USDT->USDC
    assert paths[0][0].token0 == "USDC"
    assert paths[0][-1].token1 == "USDC"

def test_find_paths_with_affected_pools(path_finder):
    # 测试根据受影响的池子寻找路径
    affected_pools = [
        MockPool("0x1", "USDC", "ETH", Decimal("1000"), Decimal("1"))
    ]
    
    # 禁用自定义路径
    path_finder.config.custom_paths = None
    paths = path_finder.find_paths(affected_pools)
    
    assert len(paths) > 0
    for path in paths:
        # 验证每条路径都是闭环的
        assert path[0].token0 == path[-1].token1
        # 验证每条路径都包含至少一个受影响的池子
        affected_addresses = {p.address for p in affected_pools}
        path_addresses = {p.address for p in path}
        assert len(affected_addresses & path_addresses) > 0

def test_blacklist_tokens(path_finder):
    # 测试代币黑名单
    affected_pools = [
        MockPool("0x5", "SAFEMOON", "ETH", Decimal("1000"), Decimal("1"))
    ]
    
    path_finder.config.custom_paths = None
    paths = path_finder.find_paths(affected_pools)
    
    # 不应该包含黑名单代币的路径
    for path in paths:
        for pool in path:
            assert pool.token0 != "SAFEMOON"
            assert pool.token1 != "SAFEMOON"

def test_liquidity_filter(path_finder):
    # 测试流动性过滤
    affected_pools = [
        MockPool("0x6", "USDC", "ETH", Decimal("10"), Decimal("0.1"))  # 流动性太低
    ]
    
    path_finder.config.custom_paths = None
    paths = path_finder.find_paths(affected_pools)
    
    # 所有池子都应该满足最小流动性要求
    min_liquidity = path_finder.config.min_liquidity
    for path in paths:
        for pool in path:
            assert pool.amount0 + pool.amount1 >= min_liquidity

def test_max_path_length(path_finder):
    # 测试最大路径长度限制
    path_finder.config.custom_paths = None
    affected_pools = [
        MockPool("0x1", "USDC", "ETH", Decimal("1000"), Decimal("1"))
    ]
    
    paths = path_finder.find_paths(affected_pools)
    
    # 所有路径长度应该小于等于最大长度
    max_length = path_finder.config.max_path_length
    for path in paths:
        assert len(path) <= max_length 