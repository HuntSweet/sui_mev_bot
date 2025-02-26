import asyncio
import logging
from typing import Dict, Optional, List
from config import Config
from monitor.transaction_monitor import TransactionMonitor
from analysis.price_impact import PriceImpactAnalyzer
from strategy.strategies import Strategies
from strategy.gradient_search_strategy import GradientSearchStrategy
from strategy.two_pool_arbitrage import TwoPoolArbitrageStrategy

from execution.transaction_executor import TransactionExecutor
from common.event_bus import EventBus
from analysis.price_impact import TransactionFilters, PriceImpactFilter
from analysis.price_impact import Pool
from token_price.token_price import TokenPriceProvider
from monitor.shio_feed import ShioFeedMonitor
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

class PathGenerator:
    def __init__(self):
        self.event_bus = EventBus(asyncio.get_event_loop())
        
    async def generate_path_list(self, affected_pairs: List[Pool]) -> List[List[Pool]]:
        pass
    
async def main():
    config = Config()
    
    transaction_monitor = TransactionMonitor()
    shio_feed_monitor = ShioFeedMonitor()
    transaction_monitor.start()
    shio_feed_monitor.start()
    
    event_bus = EventBus(asyncio.get_event_loop())
    transaction_filters = TransactionFilters()
    transaction_filters.add_filter(PriceImpactFilter())
    affected_pairs_extractor = AffectedPairsExtractor()
    strategies = Strategies(event_bus)
    strategies.add_strategy(TwoPoolArbitrageStrategy())
    strategies.add_strategy(GradientSearchStrategy())
    path_generator = PathGenerator()
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
            path_list = await path_generator.generate_path_list(affected_pairs)
            # 寻找套利机会
            await strategies.find_arbitrage_opportunities(path_list)
        except Exception as e:
            logger.error(f"运行时发生错误: {e}")
    
    event_bus.add_event("receive_transactions", run_bot)
    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {e}") 