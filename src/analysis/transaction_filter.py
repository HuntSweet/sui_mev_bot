from abc import ABC, abstractmethod
from typing import Dict, List

class TransactionFilter(ABC):
    @abstractmethod
    def filter(self, transactions: List[Dict]) -> List[Dict]:
        pass

class TransactionFilters:
    def __init__(self, filters:List[TransactionFilter]):
        self.filters = filters
        
    def add_filter(self, filter:TransactionFilter):
        self.filters.append(filter)
        
    def filter_transactions(self, transactions: List[Dict]) -> List[Dict]:
        for filter in self.filters:
            transactions = filter.filter(transactions)
        return transactions