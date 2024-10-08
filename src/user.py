"""Import modules"""
import dataclasses
from os import environ
from dotenv import load_dotenv

@dataclasses.dataclass
class EnvVariables:
    """Variables dataclass"""
    ROOT: str
    HOST: str
    USER: str
    PASSWORD: str

class User:
    """User Configuration interface"""
    
    def __init__(self): 
        """Load instance variables"""
        load_dotenv()

        self.creds = EnvVariables(
            ROOT=environ["DB_ROOT"],
            HOST=environ["DB_HOST"],
            USER=environ["DB_USER"],
            PASSWORD=environ["DB_PASSWORD"]
        )