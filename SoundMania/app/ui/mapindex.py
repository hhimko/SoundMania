from __future__ import annotations
from math import ceil

import logging
logger = logging.getLogger("MapIndex")

import pygame

from ui.menuitemlist import MenuItemList
from ui.core.type import _UnitRect
from ui.button import Button
import soundmania


class MapIndex(MenuItemList):
    BUTTON_OFFEST = 50
    BUTTON_HEIGHT = 150
    
    def __init__(self, root: soundmania.SoundMania, name: str, rect: _UnitRect | pygame.Rect, **kwargs):
        super().__init__(name, rect, **kwargs)
        self.root = root
        
        self._visible_count = self._calculate_visible_count() 
        self._map_paths = self.root.map_manager.load_available_maps()
        logger.info(f"Successfully loaded {len(self._map_paths)} maps")
        
        self._spawn_visible()
        
        
    @property 
    def prefab(self) -> Button:
        return Button("map_prefab", (self.x, 0, self._width, self.BUTTON_HEIGHT), 
                      centered=True, color=(200,200,200), text="???", text_size=75
                     )
        
        
    def select_previous(self, wrap: bool = True) -> None:
        super().select_previous(wrap)
        self._update_visible()
    
    
    def select_next(self, wrap: bool = True) -> None:
        super().select_next(wrap)
        self._update_visible()
        
        
    def _calculate_visible_count(self) -> int:
        return ceil((self.height / (self.BUTTON_HEIGHT + self.BUTTON_OFFEST) - 1) / 2) * 2 + 1 # should always return an odd number
    
    
    def _spawn_visible(self) -> None:
        self.elements.clear()
        
        for i in range(-self._visible_count//2 + 1, self._visible_count//2 + 1):
            button = self.prefab
            button.name = f"map_button_{i}"
            self.add(button)
            
        self._update_visible()
            
            
    def _update_visible(self) -> None:
        for i in range(-self._visible_count//2 + 1, self._visible_count//2 + 1):
            button = self._get_item_relative(i)
            button.is_dirty = True
            
            map_index = self._selected_index + i
            if  not 0 <= map_index < len(self._map_paths):
                button.hidden = True
                button.text = "???"
                continue
            
            button.hidden = False
            button.y = i *(self.BUTTON_HEIGHT + self.BUTTON_OFFEST) + self.y
            
            map_path = self._map_paths[map_index]
            button.text = map_path.split('\\')[-1]
            
    
    def _on_window_resize(self) -> None:
        super()._on_window_resize()
        self._visible_count = self._calculate_visible_count() 
        self._spawn_visible()
        
        
    def _get_item_relative(self, index: int) -> Button:
        center = self._visible_count // 2
        return super().__getitem__(center+index)
        
        
    def __len__(self) -> int:
        return len(self._map_paths)
    
    
    