import asyncio
import json
import logging
import websockets
from typing import Dict, List
from decimal import Decimal
from ..common.event_bus import EventBus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShioFeedMonitor:
    def __init__(self, event_bus: EventBus, proxy: str = None):
        self.ws_url = "wss://rpc.getshio.com/feed"
        self.ws = None
        self.is_running = False
        self.proxy = proxy
        self.event_bus = event_bus
        
    async def connect(self):
        """建立WebSocket连接"""
        try:
            websocket_options = {
                'max_size': None,
                'ssl': True,
                'ping_interval': 20,
                'ping_timeout': 20,
            }
            
            if self.proxy:
                proxy_host, proxy_port = self.proxy.split(':')
                websocket_options.update({
                    'proxy': f'http://{proxy_host}:{proxy_port}'
                })
            
            self.ws = await websockets.connect(
                self.ws_url,
                **websocket_options
            )
            
            logger.info("成功连接到Shio Feed")
            return True
            
        except Exception as e:
            logger.error(f"连接Shio Feed失败: {e}")
            return False
            
    async def monitor_transactions(self, message: str):
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            
            # 处理ping消息
            if data.get("type") == "ping":
                await self.send_pong()
                return
                
            # 处理拍卖事件
            if data.get("auctionStarted","") != "":
                transactions = self._parse_auction_event(data)
                if transactions:
                    self.event_bus.emit("receive_transactions", transactions)
                    
        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
            
    def _parse_auction_event(self, event: Dict) -> List[Dict]:
        """
        解析拍卖事件为标准交易格式
        返回格式:
        {
            "hash": str,
            "dex": str,
            "function": str,
            "token_in": str,
            "token_out": str,
            "amount_in": Decimal,
            "amount_out": Decimal,
            "timestamp": int
        }
        """
        try:
            auction_data = event.get("data", {})
            
            transaction = {
                "hash": auction_data.get("id", ""),
                "dex": "shio",
                "function": "auction",
                "token_in": auction_data.get("baseAsset", ""),
                "token_out": auction_data.get("quoteAsset", ""),
                "amount_in": Decimal(str(auction_data.get("baseAmount", "0"))),
                "amount_out": Decimal(str(auction_data.get("quoteAmount", "0"))),
                "timestamp": auction_data.get("timestamp", 0)
            }
            
            return [transaction]
            
        except Exception as e:
            logger.error(f"解析拍卖事件时发生错误: {e}")
            return []
            
    async def send_pong(self):
        """响应ping消息"""
        if self.ws:
            try:
                pong_message = {"type": "pong"}
                await self.ws.send(json.dumps(pong_message))
            except Exception as e:
                logger.error(f"发送pong消息失败: {e}")
                
    async def _start(self):
        """启动监控"""
        self.is_running = True
        
        while self.is_running:
            try:
                if not self.ws:
                    success = await self.connect()
                    if not success:
                        await asyncio.sleep(5)  # 连接失败后等待5秒重试
                        continue
                        
                async for message in self.ws:
                    await self.monitor_transactions(message)
                    
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket连接断开，尝试重连...")
                self.ws = None
            except Exception as e:
                logger.error(f"监控过程发生错误: {e}")
                await asyncio.sleep(1)
                
    async def stop(self):
        """停止监控"""
        self.is_running = False
        if self.ws:
            await self.ws.close()
            self.ws = None 
    
    def start(self):
        asyncio.create_task(self._start())
