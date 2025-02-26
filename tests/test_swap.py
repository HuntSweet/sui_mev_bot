import asyncio
import pytest
from decimal import Decimal
from src.config import Config
from src.execution.transaction_executor import TransactionExecutor

class TestSwap:
    @pytest.fixture
    def config(self):
        return Config()
    
    @pytest.fixture
    def executor(self, config):
        return TransactionExecutor(config)
    
    @pytest.mark.asyncio
    async def test_sui_to_usdc_swap(self, executor):
        # 测试参数
        swap_params = {
            "token_in": {
                "address": "0x2::sui::SUI",  # SUI代币地址
                "amount": Decimal("1.0")  # 兑换1个SUI
            },
            "token_out": {
                "address": "0x5d4b302506645c37ff133b98c4b50a5ae14841659738d6d733d59d0d217a93bf::coin::USDC",  # USDC代币地址
                "min_amount_out": Decimal("0")  # 最小获得的USDC数量，这里设为0便于测试
            },
            "dex": {
                "name": "deepbook",  # 使用DeepBook DEX
                "pool": "0x...",  # 需要填入实际的交易对地址
            }
        }

        try:
            # 构建交易
            transaction = await executor._build_transaction({
                "type": "swap",
                "params": swap_params
            })
            
            # 估算gas
            estimated_gas = await executor._estimate_gas(transaction)
            print(f"预估gas费用: {estimated_gas}")
            
            # 执行交易
            tx_result = await executor._send_transaction(transaction)
            print(f"交易结果: {tx_result}")
            
            # 验证交易
            success = executor._verify_transaction(tx_result)
            assert success, "交易执行失败"
            
            # 验证交易结果
            if success:
                print(f"交易哈希: {tx_result.get('digest')}")
                print(f"获得的USDC数量: {tx_result.get('effects', {}).get('amount_out')}")
                
        except Exception as e:
            pytest.fail(f"测试失败: {str(e)}")

if __name__ == "__main__":
    # 直接运行测试
    asyncio.run(TestSwap().test_sui_to_usdc_swap(
        TestSwap().executor(TestSwap().config())
    )) 