from typing import Iterator, Generic, TypeVar

import pygame

from ui.core.type import _UnitRect
from ui.core.basecomponent import UIComponent


T = TypeVar('T', bound=UIComponent)
class UIContainer(UIComponent, Generic[T]):
    def __init__(self, name: str, rect: _UnitRect | pygame.Rect, *elements: T, **kwargs):
        self.elements: dict[str, T] = {}
        super().__init__(name, rect, **kwargs)
        
        for element in elements:
            self.add(element)
            element.parent = self

    @property
    def hidden(self) -> bool:
        return self._hidden
    
    
    @hidden.setter
    def hidden(self, value: bool) -> None:
        self._hidden = value
        for element in self:
            element.hidden = value

            
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
        for element in self:
            element.update(dt)


    def render(self, surface: pygame.surface.Surface) -> None:
        """ Render all component elements in the container. 
            The components are rendered in the same order they were added. 
            
            Args:
                 surface: pygame `Surface` object on which to render
        """
        super().render(surface)

        for element in self:
            element.render(surface)
        
        
    def _winpos_recompute(self) -> None:
        super()._winpos_recompute()
        
        for element in self:
            element._winpos_recompute()
            
            
    def _on_window_resize(self) -> None:
        super()._on_window_resize()
        
        for element in self:
            element._on_window_resize()
            
        
    def __getattr__(self, attr: str) -> T:
        if not "elements" in dir(self):
            raise KeyError(f"Container '{self.name}' is missing 'self.elements'")
        
        element = self.elements.get(attr) 
        if element is None:
            raise AttributeError(f"container '{self.name}' does not contain element with name '{attr}'")
        
        return element
    
    
    def __len__(self) -> int:
        return len(self.elements)
        
        
    def __iter__(self) -> Iterator[T]:
        return iter(self.elements.values())
    
    
    def __getitem__(self, index: int) -> T:
        return list(self.elements.values())[index]
    