from abc import ABC, abstractmethod
class Monitor(ABC):
    #数据源
    @abstractmethod
    async def monitor_transactions(self):
        pass
