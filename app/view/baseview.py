from abc import ABC, abstractmethod
from pygame.surface import Surface


class View(ABC):
    """ Abstract View class defining a common interface for creating scenes. """
    def __init__(self, root):
        self.root = root
        
        
    @abstractmethod    
    def handle_input(self) -> None:
        pass
    
    
    @abstractmethod    
    def update(self, dt: int) -> None:
        pass
    
    
    @abstractmethod    
    def render(self, surface: Surface) -> None:
        pass