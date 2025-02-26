from typing import List, Dict, Set
import asyncio
from sui_python_sdk import SuiClient, SuiConfig
from ..config import Config
from abc import ABC, abstractmethod


class Monitor(ABC):
    #数据源
    @abstractmethod
    async def monitor_transactions(self) -> List[Dict]:
        pass


class TransactionMonitor(Monitor):
    def __init__(self, rpc_url: str):
        self.client = SuiClient(SuiConfig.from_rpc_url(rpc_url))
        # DEX合约地址映射
        self.dex_contracts = {
            "turbos": {
                "pool": "0x...",  # Turbos池合约地址
                "router": "0x..."  # Turbos路由合约地址
            },
            "cetus": {
                "pool": "0x...",
                "router": "0x..."
            },
            "deepbook": {
                "pool": "0x...",
                "router": "0x..."
            }
        }
        # 已知的DEX函数签名
        self.dex_functions = {
            "swap_exact_input": "0x...",
            "swap_exact_output": "0x...",
            "add_liquidity": "0x...",
            "remove_liquidity": "0x..."
        }
        
    async def monitor_transactions(self) -> List[Dict]:
        """
        监控链上交易，识别潜在的套利机会
        """
        try:
            # 获取最新区块
            latest_block = await self.client.get_latest_checkpoint_sequence_number()
            
            # 获取区块中的交易
            transactions = await self.client.get_checkpoint(latest_block)
            
            # 过滤出DEX相关交易
            dex_transactions = self._filter_dex_transactions(transactions)
            
            return dex_transactions
            
        except Exception as e:
            print(f"监控交易时发生错误: {e}")
            return []
            
    def _filter_dex_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """
        过滤出DEX相关的交易
        """
        filtered_txs = []
        for tx in transactions:
            if self._is_dex_transaction(tx):
                # 解析交易详情
                parsed_tx = self._parse_dex_transaction(tx)
                if parsed_tx:
                    filtered_txs.append(parsed_tx)
        return filtered_txs
        
    def _is_dex_transaction(self, transaction: Dict) -> bool:
        """
        判断是否为DEX交易
        """
        try:
            # 检查交易目标地址是否是已知的DEX合约
            target_addresses = self._extract_target_addresses(transaction)
            for dex in self.dex_contracts.values():
                if dex["pool"] in target_addresses or dex["router"] in target_addresses:
                    return True
                    
            # 检查交易调用的函数是否是DEX相关函数
            function_signature = self._extract_function_signature(transaction)
            return function_signature in self.dex_functions.values()
            
        except Exception as e:
            print(f"检查DEX交易时发生错误: {e}")
            return False
            
    def _parse_dex_transaction(self, transaction: Dict) -> Dict:
        """
        解析DEX交易详情
        """
        try:
            # 基础交易信息
            parsed_tx = {
                "tx_hash": transaction.get("digest"),
                "timestamp": transaction.get("timestamp_ms"),
                "sender": transaction.get("sender"),
                "dex_info": self._get_dex_info(transaction),
                "function_info": self._get_function_info(transaction),
                "token_info": self._get_token_info(transaction)
            }
            
            return parsed_tx
            
        except Exception as e:
            print(f"解析DEX交易时发生错误: {e}")
            return None
            
    def _extract_target_addresses(self, transaction: Dict) -> Set[str]:
        """
        提取交易的目标地址
        """
        addresses = set()
        try:
            # 从交易数据中提取所有目标地址
            if "target" in transaction:
                addresses.add(transaction["target"])
            if "calls" in transaction:
                for call in transaction["calls"]:
                    if "target" in call:
                        addresses.add(call["target"])
        except Exception as e:
            print(f"提取目标地址时发生错误: {e}")
        return addresses
        
    def _extract_function_signature(self, transaction: Dict) -> str:
        """
        提取交易的函数签名
        """
        try:
            if "function" in transaction:
                return transaction["function"]
            return ""
        except Exception as e:
            print(f"提取函数签名时发生错误: {e}")
            return ""
            
    def _get_dex_info(self, transaction: Dict) -> Dict:
        """
        获取DEX相关信息
        """
        for dex_name, contracts in self.dex_contracts.items():
            addresses = self._extract_target_addresses(transaction)
            if contracts["pool"] in addresses or contracts["router"] in addresses:
                return {
                    "name": dex_name,
                    "contract": contracts["pool"] if contracts["pool"] in addresses else contracts["router"]
                }
        return {}
        
    def _get_function_info(self, transaction: Dict) -> Dict:
        """
        获取函数调用信息
        """
        function_sig = self._extract_function_signature(transaction)
        for fname, fsig in self.dex_functions.items():
            if fsig == function_sig:
                return {
                    "name": fname,
                    "signature": fsig
                }
        return {}
        
    def _get_token_info(self, transaction: Dict) -> Dict:
        """
        获取代币相关信息
        """
        try:
            # 从交易输入数据中解析代币信息
            return {
                "token_in": self._parse_token_input(transaction),
                "token_out": self._parse_token_output(transaction),
                "amount_in": self._parse_amount_in(transaction),
                "amount_out": self._parse_amount_out(transaction)
            }
        except Exception as e:
            print(f"获取代币信息时发生错误: {e}")
            return {}
            
    def _parse_token_input(self, transaction: Dict) -> str:
        """
        解析输入代币
        """
        # TODO: 实现输入代币解析逻辑
        return ""
        
    def _parse_token_output(self, transaction: Dict) -> str:
        """
        解析输出代币
        """
        # TODO: 实现输出代币解析逻辑
        return ""
        
    def _parse_amount_in(self, transaction: Dict) -> int:
        """
        解析输入金额
        """
        # TODO: 实现输入金额解析逻辑
        return 0
        
    def _parse_amount_out(self, transaction: Dict) -> int:
        """
        解析输出金额
        """
        # TODO: 实现输出金额解析逻辑
        return 0 