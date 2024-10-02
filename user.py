"""Import modules"""
import dataclasses
from yaml import load
from yaml.loader import SafeLoader
from os.path import join, dirname, abspath

@dataclasses.dataclass
class EnvVariables:
    """Variables dataclass"""
    root: str
    host: str
    user: str
    password: str

class User:
    """User Configuration interface"""
    
    def __init__(self): 
        """Load instance variables"""
        data = {}
        with open(
            join(dirname(abspath(__file__)), "creds.yaml"), encoding="utf-8"
        ) as file:
            data = load(file, Loader=SafeLoader)
        self.vars = EnvVariables(
            root=data.get("root"),
            host=data.get("host"),
            user=data.get("user"),
            password=data.get("password")
        )
