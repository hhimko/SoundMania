from __future__ import annotations
from typing import Callable
from math import ceil

import logging
logger = logging.getLogger("MapIndex")

import pygame

from ui.core import UIComponent, UIContainer
from ui.core.type import _UnitRect
from ui.core.units import pw, ph
from ui.button import Button
import soundmania


class MapIndex(UIContainer):
    BUTTON_OFFEST = 50
    BUTTON_HEIGHT = 150
    
    def __init__(self, root: soundmania.SoundMania, name: str, rect: _UnitRect | pygame.Rect, **kwargs):
        super().__init__(name, rect, **kwargs)
        self.root = root
        self._selected_index = 0
        
        self._visible_count = self._calculate_visible_count() 
        self._map_paths = self.root.map_manager.load_available_maps()
        logger.info(f"Successfully loaded {len(self._map_paths)} maps")
        
    
    def get_prefab(self) -> UIContainer:
        """ Return a new GUI map object based on a prefab. """
        # container elements need to be instantiated separately to avoid shallow copying
        return UIContainer("map_prefab", (0, 0, self._width, self.BUTTON_HEIGHT),
                        Button("button_overlay", (0, 0, pw(100), self.BUTTON_HEIGHT), hidden=True),
                        UIComponent("section_title", (0, 0, pw(100), ph(60)), text="???", color=(200,200,200)),
                        UIComponent("section_author", (0, ph(60), pw(100), ph(40)), text="???", color=(200,200,200)),
                        parent=self, centered=True, color=(200,200,200)
                     )
    
        
    def select_previous(self, wrap: bool = True) -> None:
        """ Decrement the currenty selected map index.
            
            Args:
                wrap: tells whether to wrap the index around or clamp to the last item 
        """
        if len(self) == 0:
            return
        
        idx = self._selected_index - 1
        self._selected_index = idx % len(self) if wrap else max(idx, 0)
        
        self._update_visible()
        
    
    def select_enter(self) -> None:
        """ Select and play current map. """
        if len(self) == 0:
            return
        
        selected = self._get_component_relative(0)
        selected.button_overlay.on_mouse_click()
    
    
    def select_next(self, wrap: bool = True) -> None:
        """ Increment the currenty selected map index.
            
            Args:
                wrap: tells whether to wrap the index around or clamp to the last item 
        """
        if len(self) == 0:
            return
        
        idx = self._selected_index + 1
        self._selected_index = idx % len(self) if wrap else min(idx, len(self)-1)
        
        self._update_visible()
        
        
    def _calculate_visible_count(self) -> int:
        return ceil((self.height / (self.BUTTON_HEIGHT + self.BUTTON_OFFEST) - 1) / 2) * 2 + 1 # should always return an odd number
    
    
    def _spawn_visible(self) -> None:
        self.elements.clear()
        
        for i in range(-self._visible_count//2 + 1, self._visible_count//2 + 1):
            component = self.get_prefab()
            component.name = f"map_component_{i}"
            self.add(component)
            
        self._update_visible()
            
            
    def _update_visible(self) -> None:
        for i in range(-self._visible_count//2 + 1, self._visible_count//2 + 1):
            component = self._get_component_relative(i)
            component.is_dirty = True
            
            map_index = self._selected_index + i
            if  not 0 <= map_index < len(self._map_paths):
                component.hidden = True
                component.text = "???"
                del component.button_overlay.on_mouse_click
            else:
                component.hidden = False
                component.y = i *(self.BUTTON_HEIGHT + self.BUTTON_OFFEST) + self.y
                component.width = self.width - abs(i) * 20
                
                map_path = self._map_paths[map_index]
                map_info = self.root.map_manager.get_map_info(map_path)
                
                component.section_title.text = map_info.song_title
                component.section_author.text = map_info.song_author
                
                component.button_overlay.on_mouse_click = self._get_button_callback(map_info.song_path)
                
            component._on_window_resize()
            
            
    def _get_button_callback(self, song_path: str) -> Callable:
        return lambda _: print(song_path)
            
    
    def _on_window_resize(self) -> None:
        super()._on_window_resize()
        self._visible_count = self._calculate_visible_count() 
        self._spawn_visible()
        
        
    def _get_component_relative(self, index: int) -> UIContainer:
        center = self._visible_count // 2
        return super().__getitem__(center+index)
        
        
    def __len__(self) -> int:
        return len(self._map_paths)
    
    
    