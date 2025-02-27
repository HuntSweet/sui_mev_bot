import asyncio
import json
import logging
import websockets
from typing import Callable, Optional,List,Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShioFeedMonitor:
    def __init__(self,  proxy: Optional[str] = None):
        self.ws_url = "wss://rpc.getshio.com/feed"
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.is_running = False
        self.proxy = proxy
        
    async def connect(self):
        """建立WebSocket连接"""
        try:
            # 设置连接选项
            websocket_options = {
                'max_size': None,
                'ssl': True,
                'ping_interval': 20,
                'ping_timeout': 20,
            }
            
            # 如果设置了代理
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
    
    def convert_message(self,message:str) -> List[Dict]:
        """将消息转换为交易信息"""
        pass
    
    async def monitor_transactions(self, message: str):
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            
            logger.debug(f"收到消息: {data}")
                
            # 处理ping消息
            if data.get("type") == "ping":
                await self.send_pong()
                return
            
            # 处理auction事件
            if data.get("auctionStarted","") != "":
                logger.info(f"收到拍卖事件: {data}")
                transactions = self.convert_message(data)

                self.event_bus.emit("receive_transactions", transactions)

                    
        except json.JSONDecodeError:
            logger.error(f"解析消息失败: {message}")
        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
            
    async def send_pong(self):
        """响应ping消息"""
        if self.ws:
            try:
                pong_message = {"type": "pong"}
                await self.ws.send(json.dumps(pong_message))
            except Exception as e:
                logger.error(f"发送pong消息失败: {e}")
                
    async def start(self):
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

