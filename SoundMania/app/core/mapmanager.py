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
    song_path: str
    
    
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
        """ Extract a MapInfo object from a specified path to an existing map directory. """
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
        """ Validate and parse a map directory. 
            
            Returns:
                a new MapInfo object on successful parse, otherwise `None` 
        """
        if os.path.isdir(path) and path.endswith(cls.MAP_EXTENSION):
            info_file_path = os.path.join(path, cls.INFO_FILE_NAME)
            
            if not os.path.isfile(info_file_path):
                logger.warn(f"{path} map exists, but info file is missing")
                return None
            
            with open(info_file_path, 'r') as info_file:
                author = info_file.readline().strip() or "???"
                name = info_file.readline().strip() or "???"
                
                music_paths = [p for p in os.listdir(path) if p.endswith((".mp3", ".ogg"))]
                if not music_paths:
                    logger.warn(f"{path} map exists, but music file is missing")
                    return None
                
                if len(music_paths) > 1:
                    logger.warn(f"{path} map exists, but contains multiple music files, and the result is ambiguous")
                    return None
                
                song_path = os.path.join(path, music_paths[0])
            
            return MapInfo(path, author, name, song_path)
        
        return None
    
    
    @classmethod
    def _get_user_path(cls) -> str:
        config = configparser.ConfigParser() # TODO: probably extract config parsing to a distinct file manager
        config.read(cls.CONF_PATH)
        
        try:
            return config["COMMON"]["map_dir"]
        except KeyError:
            default = cls.CONF_DEFAULTS["map_dir"]
            logger.info(f"Could not obtain map directory from 'conf.ini'. Defaulting to '{default}'")
            return default
        