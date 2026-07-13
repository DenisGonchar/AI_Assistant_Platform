from abc import ABC, abstractmethod

class BaseSearch(ABC):
    @abstractmethod
    def search(self, query: str) -> list[dict]:
        '''
        Выполняет поиск и возвращает список результатов
        '''
        pass
    