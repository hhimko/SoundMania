from functools import cached_property
import configparser

import logging
logger = logging.getLogger("MapManager")


class ConfigIO:
    """ Class responsible for managing user's local settings. """
    CONFIG_PATH = "SoundMania\\locals\\conf.ini"
    DEFAULTS = {
        "map_dir": "SoundMania\\locals\\maps"
    }
    
    def settings_get(self, name: str) -> str:
        """ Helper method for extracting user's local settings. """
        return self[name]
    
    
    def settings_set(self, **mapping: dict[str, str]) -> None:
        """ Helper method for overriding user's local settings. """
        pass
    
    
    def settings_apply(self) -> None:
        pass
    
    
    def settings_discard(self) -> None:
        pass
    
        
    @classmethod
    def get_user_map_directory(cls) -> str:
        config = configparser.ConfigParser()
        config.read(cls.CONFIG_PATH)
        
        try:
            return config["COMMON"]["map_dir"]
        except KeyError:
            default = cls.DEFAULTS["map_dir"]
            logger.info(f"Could not obtain map directory from 'conf.ini'. Defaulting to '{default}'")
            return default
        
    
    def __getitem__(self, name: str) -> str:
        return ''
    
    
    def __setitem__(self, name: str, value: str) -> None:
        return