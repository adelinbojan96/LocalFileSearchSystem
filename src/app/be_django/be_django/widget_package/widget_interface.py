from abc import ABC, abstractmethod

class Widget(ABC):
    @abstractmethod
    def should_activate(self, context: dict) -> bool:
        pass

    @abstractmethod
    def render_payload(self, context: dict) -> dict:
        pass