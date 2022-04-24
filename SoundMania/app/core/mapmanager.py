import configparser

class MapManager:
    CONF_PATH = "SoundMania/locals/conf.ini"
    
    def __init__(self): 
        self.local_path = self._get_user_path()
    
    
    @classmethod
    def load_map_index(cls) -> list[None]:
        return []
    
    
    @classmethod
    def _get_user_path(cls) -> str:
        config = configparser.ConfigParser()
        config.read(cls.CONF_PATH)
        return config["COMMON"]["map_dir"]