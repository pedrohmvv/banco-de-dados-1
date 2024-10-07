"""Import modules"""
import dataclasses
from yaml import load
from yaml.loader import SafeLoader
from os.path import join, dirname, abspath

@dataclasses.dataclass
class ItemsVariables:
    """Variables dataclass"""
    products_by_category: dict

class Items:
    """User Configuration interface"""
    
    def __init__(self): 
        """Load instance variables"""
        data = {}
        with open(
            join(dirname(abspath(__file__)), "items.yaml"), encoding="utf-8"
        ) as file:
            data = load(file, Loader=SafeLoader)
        self.item = ItemsVariables(
            products_by_category=data.get('products_by_category'),
        )
