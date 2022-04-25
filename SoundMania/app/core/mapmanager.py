from dataclasses import dataclass
import configparser
import os

import logging
logger = logging.getLogger("MapManager")


@dataclass
class MapInfo:
    map_path: str
    song_author: str
    song_title: str
    song_duration: int=0
    
    
class MapManager:
    MAP_EXTENSION = ".smm"
    INFO_FILE_NAME = "info"
    
    CONF_PATH = "SoundMania\\locals\\conf.ini"
    CONF_DEFAULTS = {
        "map_dir": "SoundMania\\locals\\maps",
    }
    
    
    def __init__(self): 
        self.local_path = self._get_user_path()
        self._map_info_cache: dict[str, MapInfo] = {}
        
        
    def get_map_info(self, path: str) -> MapInfo:
        map_info = self._map_info_cache.get(path)
        
        if not map_info:
            full_path = os.path.join(self.local_path, path)
            if self._register_map(full_path):
                map_info = self._map_info_cache[path]
            else:
                raise KeyError(f"map could not be located at '{path}'")
    
        return map_info
    
    
    def load_available_maps(self) -> list[str]:
        """ Load to the managers cache and return all avaiable map paths. """
        available = [] 
        
        for path in os.listdir(self.local_path):
            full_path = os.path.join(self.local_path, path)
            
            if self._register_map(full_path):
                available.append(full_path)
                
        return available
    
    
    def _register_map(self, path: str) -> bool:
        map_info = self._parse_map_info(path)
        if not map_info:
            return False
        
        self._map_info_cache[path] = map_info
        return True
    
    
    @classmethod
    def _parse_map_info(cls, path: str) -> MapInfo | None:
        if os.path.isdir(path) and path.endswith(cls.MAP_EXTENSION):
            info_file_path = os.path.join(path, cls.INFO_FILE_NAME)
            
            if not os.path.isfile(info_file_path):
                logger.warn(f"{path} map exists, but info file is missing")
                return None
            
            with open(info_file_path, 'r') as info_file:
                author = info_file.readline().strip() or "???"
                name = info_file.readline().strip() or "???"
                try:
                    duration = int(info_file.readline().strip())
                except ValueError:
                    logger.warn(f"{path} map exists, but info file is corrupted")
                    return None 
            
            return MapInfo(path, author, name, duration)
        
        return None
    
    
    @classmethod
    def _get_user_path(cls) -> str:
        config = configparser.ConfigParser()
        config.read(cls.CONF_PATH)
        
        try:
            return config["COMMON"]["map_dir"]
        except KeyError:
            default = cls.CONF_DEFAULTS["map_dir"]
            logger.info(f"Could not obtain map directory from 'conf.ini'. Defaulting to '{default}'")
            return default
        