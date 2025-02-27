import asyncio
import logging
from typing import Dict, Optional, List
from config import Config
from monitor.transaction_monitor import TransactionMonitor
from analysis.price_impact import PriceImpactAnalyzer
from strategy.strategies import Strategies
from strategy.gradient_search_strategy import GradientSearchStrategy
from strategy.two_pool_arbitrage_strategy import TwoPoolArbitrageStrategy

from execution.transaction_executor import TransactionExecutor
from db.db import DB
from common.event_bus import EventBus
from analysis.price_impact import TransactionFilters, PriceImpactFilter
from analysis.price_impact import Pool
from token_price.token_price import TokenPriceProvider
from monitor.shio_feed_monitor import ShioFeedMonitor
from path.path_finder import PathFinder, PathConfig
from decimal import Decimal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AffectedPairsExtractor:
    def __init__(self):
        self.event_bus = EventBus(asyncio.get_event_loop())
        
    async def extract_affected_pairs(self, transactions: List[Dict]) -> List[Pool]:
        pass


    
async def main():
    config = Config()
    
    # 数据库
    db = DB()
    
    # 创建交易监控器
    transaction_monitor = TransactionMonitor(config.SUI_RPC_URL,db)
    shio_feed_monitor = ShioFeedMonitor()
    transaction_monitor.start()
    shio_feed_monitor.start()
    
    event_bus = EventBus(asyncio.get_event_loop())
    
    # 交易过滤器
    transaction_filters = TransactionFilters()
    transaction_filters.add_filter(PriceImpactFilter())
    affected_pairs_extractor = AffectedPairsExtractor()
    
    # 策略
    strategies = Strategies(event_bus)
    strategies.add_strategy(TwoPoolArbitrageStrategy())
    strategies.add_strategy(GradientSearchStrategy())
    
    # 创建路径查找器
    path_config = PathConfig(
        max_path_length=3,
        min_liquidity=Decimal('1000'),
        custom_paths=[
        ],
        blacklist_tokens={"SAFEMOON"},
        blacklist_dexes={""}
    )
    
    path_finder = PathFinder(path_config,db)

    token_price_provider = TokenPriceProvider()
    # 用于接收盈利的机会并执行交易
    executor = TransactionExecutor(config,event_bus,token_price_provider)
    
    async def run_bot(transactions:List[Dict]):
        try:
            # 过滤交易
            filterd_transactions = await transaction_filters.filter_transactions(transactions)
            # 提取影响池
            affected_pairs = await affected_pairs_extractor.extract_affected_pairs(filterd_transactions)
            # 生成路径
            path_list = await path_finder.find_paths(affected_pairs)
            # 寻找套利机会
            await strategies.find_arbitrage_opportunities(path_list)
        except Exception as e:
            logger.error(f"运行时发生错误: {e}")
    
    event_bus.add_event("receive_transactions", run_bot)
    while True:
        await token_price_provider.update_token_price()
        await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {e}") 