from typing import Generic, TypeVar

import pygame

from ui.core.type import _TupleI4
from ui.core.basecomponent import UIComponent


T = TypeVar('T', bound=UIComponent)
class UIContainer(UIComponent, Generic[T]):
    def __init__(self, name: str, rect: _TupleI4 | pygame.Rect, *elements: T, **kwargs):
        self.elements: dict[str, T] = {} # this has to appear before super().__init__() for config() attr lookup
        super().__init__(name, rect, **kwargs)
        
        for element in elements:
            element.parent = self
            self.add(element)

            
    def add(self, element: T) -> None:
        """ Add new component to the container. 
        
            Args:
                element: the element to be added

            Raises:
                `AttributeError` when a object with the same name has already been added
        """
        if element.name in self.elements:
            raise AttributeError(f"component already contains object with name '{element.name}'")
        self.elements[element.name] = element


    def update(self, dt: int) -> None:
        """ Update all component elements in the container. 
            The components are updated in the same order they were added. 
            
            Args:
                dt: elapsed time since the last frame
        """
        for element in self.elements.values():
            element.update(dt)


    def render(self, surface: pygame.surface.Surface) -> None:
        """ Render all component elements in the container. 
            The components are rendered in the same order they were added. 
            
            Args:
                 surface: pygame `Surface` object on which to render
        """
        super().render(surface)

        for element in self.elements.values():
            element.render(surface)

        # surface.blit(self.surface, self.position)
        
        
    def _winpos_recompute(self) -> None:
        super()._winpos_recompute()
        
        for element in self.elements.values():
            element._winpos_recompute()
            
        
    def __getattr__(self, attr: str) -> T:
        # TODO: depthen lookup by iterating through containers
        element = self.elements.get(attr) 
        if element is None:
            raise AttributeError(f"container '{self.name} does not contain element with name '{attr}''")
        
        return element