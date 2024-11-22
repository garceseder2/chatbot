import json
from typing import Any, Dict
from pydantic import BaseModel

class Config(BaseModel):
    app_name: str
    version: str
    api_integration_llm: str
    vectorial_database: Dict[str, Any]
    llm: Dict[str, Any]

# Variable global para almacenar la configuración
_config: Config = None

def load_config(file_path: str = "config.json") -> Config:
    global _config
    if _config is None:  # Si aún no se ha cargado, hacerlo
        with open(file_path, "r") as file:
            data = json.load(file)
            _config = Config(**data)
    return _config

# Función para acceder a la configuración desde cualquier lugar
def get_config() -> Config:
    return _config if _config else load_config()
