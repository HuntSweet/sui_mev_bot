import asyncio
import logging
from typing import Dict, Optional, List

from config import Config
from monitor.transaction_monitor import TransactionMonitor
from analysis.price_impact import PriceImpactAnalyzer
from strategy.arbitrage import ArbitrageStrategy
from execution.transaction_executor import TransactionExecutor
from common.event_bus import EventBus
from analysis.price_impact import TransactionFilters, PriceImpactFilter
from analysis.price_impact import Pool
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MEVBot:
    def __init__(self):
        self.config = Config()
        self.monitor = TransactionMonitor(self.config.SUI_RPC_URL)
        self.analyzer = PriceImpactAnalyzer()
        self.strategy = ArbitrageStrategy(self.config)
        self.executor = TransactionExecutor(self.config)
        
    async def process_transaction(self, transaction: Dict) -> Optional[bool]:
        """
        处理单个交易
        """
        try:
            # 分析价格影响
            price_impact, affected_pairs = await self.analyzer.analyze_price_impact(transaction)
            
            # 如果价格影响太小，直接跳过
            if abs(price_impact) < self.config.MIN_PROFIT_THRESHOLD:
                return None
                
            # 寻找套利机会
            opportunity = await self.strategy.find_arbitrage_opportunity(affected_pairs)
            if not opportunity:
                return None
                
            # 执行套利交易
            success = await self.executor.execute_arbitrage(opportunity)
            return success
            
        except Exception as e:
            logger.error(f"处理交易时发生错误: {e}")
            return None
            
    async def run(self):
        """
        运行MEV机器人
        """
        logger.info("MEV机器人启动...")
        
        
        while True:
            try:
                # 监控新交易
                transactions = await self.monitor.monitor_transactions()
                
                # 并行处理所有交易
                tasks = [self.process_transaction(tx) for tx in transactions]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 统计结果
                successful_trades = sum(1 for r in results if r is True)
                if successful_trades > 0:
                    logger.info(f"成功执行 {successful_trades} 笔套利交易")
                    
                # 等待下一个轮询间隔
                await asyncio.sleep(self.config.POLLING_INTERVAL)
                
            except Exception as e:
                logger.error(f"运行时发生错误: {e}")
                await asyncio.sleep(1)  # 发生错误时短暂暂停

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
    # bot = MEVBot()
    event_bus = EventBus(asyncio.get_event_loop())
    transaction_filters = TransactionFilters()
    transaction_filters.add_filter(PriceImpactFilter())
    affected_pairs_extractor = AffectedPairsExtractor()
    config = Config()
    strategy = ArbitrageStrategy(config,event_bus)
    path_generator = PathGenerator()
    executor = TransactionExecutor(config,event_bus)
    
    async def run_bot(transactions:List[Dict]):
        try:
            # 过滤交易
            filterd_transactions = await transaction_filters.filter_transactions(transactions)
            # 提取影响池
            affected_pairs = await affected_pairs_extractor.extract_affected_pairs(filterd_transactions)
            # 生成路径
            path_list = await path_generator.generate_path_list(affected_pairs)
            # 寻找套利机会
            await strategy.find_arbitrage_opportunity(path_list)
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