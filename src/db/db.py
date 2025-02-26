from typing import Dict,List
from common.model import Pool
class DB:
    def __init__(self):
        self.db = {}
    
    #更新池子   
    async def update_pool(self, transaction: Dict):
        pass
    
    #获取池子
    async def get_pool(self, pool_id: str) -> Dict:
        pass
    
    #获取池子
    async def get_pool_by_token_address(self, token_address: str) -> Pool:
        pass
    
    #获取所有池子
    def get_all_pools(self) -> List[Pool]:
        pass
