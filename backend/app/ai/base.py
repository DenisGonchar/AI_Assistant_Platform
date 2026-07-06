from abc import ABC, abstractmethod

class BaseAI(ABC):
    @abstractmethod
    def generate(self, messages: list[dict]) -> str:
        pass