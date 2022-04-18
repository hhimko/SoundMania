import pygame

from ui.core.basecomponent import UIComponent


_ElementNameMissing = object()

class UIContainer(UIComponent):
    def __init__(self, name: str, rect: pygame.rect.Rect, elements: list[UIComponent] | None=None, **kwargs):
        super().__init__(name, rect, **kwargs)
        self.elements: dict[str, UIComponent] = {}
        
        if elements:
            for element in elements:
                self.add(element)

            
    def add(self, element: UIComponent) -> None:
        """ Add new component to the container. 
        
            Args:
                element: the element to be added

            Raises:
                `AttributeError` when a object with the same name has already been added
        """
        if element.name in self.elements:
            raise AttributeError(f"component already contains object with name '{element.name}'")
        self.elements[element.name] = element
        
        
    def __getattr__(self, attr: str):
        # TODO: depthen lookup by iterating through containers
        element = self.elements.get(attr, _ElementNameMissing) 
        if element is _ElementNameMissing:
            raise AttributeError(f"container '{self.name} does not contain element with name '{attr}''")
        return element