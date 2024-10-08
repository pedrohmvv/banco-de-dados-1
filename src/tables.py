from os.path import join, dirname, abspath
from yaml import load
from yaml.loader import SafeLoader
from dataclasses import dataclass

@dataclass
class TablesNames:
    """Tables names dataclass"""
    fornecedores: str
    categorias: str
    produtos: str
    clientes: str
    pedidos: str
    itensPedido: str

class Tables:
    """Tables class"""
    def __init__(self):
        data = {}
        with open(join(dirname(abspath(__file__)), 'tables.yaml'), encoding='utf-8') as file:
            data = load(file, Loader=SafeLoader)
        self.names = TablesNames(
            fornecedores=data.get('fornecedores'),
            categorias=data.get('categorias'),
            produtos=data.get('produtos'),
            clientes=data.get('clientes'),
            pedidos=data.get('pedidos'),
            itensPedido=data.get('itensPedido')
        )

        self.create_query = 'CREATE TABLE IF NOT EXISTS '
        
    def createTable(self, name: str, columns: str) -> str:
        """Create the table"""
        table = ' '.join([name, columns])
        return table
    
    def fornecedores(self) -> str:
        """Create the table 'Fornecedores'"""
        columns = '''(
        IDFornecedor INTEGER PRIMARY KEY AUTO_INCREMENT,
        nomeFornecedor TEXT,
        ruaFornecedor TEXT,
        numeroFornecedor INTEGER,
        bairroFornecedor TEXT,
        cidadeFornecedor TEXT
        )'''
        table = self.createTable(self.names.fornecedores, columns)         
        
        return table
    
    def categorias(self) -> str:
        """Create the table 'Categorias'"""
        columns = '''(
        IDCategoria INTEGER PRIMARY KEY AUTO_INCREMENT,
        IDFornecedor INTEGER,
        nomeCategoria TEXT,
        descricao TEXT,
        FOREIGN KEY (IDFornecedor) REFERENCES Fornecedores(IDFornecedor)
        )'''
        table = self.createTable(self.names.categorias, columns)

        return table
    
    def produtos(self) -> str:
        """Create the table 'Produtos'"""
        columns = '''(
        IDProduto INTEGER PRIMARY KEY AUTO_INCREMENT,
        IDCategoria INTEGER,
        nomeProduto TEXT,
        precoUnitario REAL CHECK (precoUnitario > 0),
        estoque INTEGER CHECK (estoque >= 0),
        FOREIGN KEY (IDCategoria) REFERENCES Categorias(IDCategoria)
        )'''
        table = self.createTable(self.names.produtos, columns)

        return table
    

    def clientes(self) -> str:
        """Create the table 'Clientes'"""
        columns = '''(
        IDCliente INTEGER PRIMARY KEY AUTO_INCREMENT,
        CPF VARCHAR(11) UNIQUE,
        nomeCompleto TEXT,
        rua TEXT,
        numero TEXT,
        bairro TEXT,
        cidade TEXT,
        telefone TEXT,
        email VARCHAR(255) UNIQUE
        )'''
        table = self.createTable(self.names.clientes, columns)

        return table
    
    def pedidos(self) -> str:
        columns = '''(
        IDPedido INTEGER PRIMARY KEY AUTO_INCREMENT,
        IDCliente INTEGER,
        data TEXT,
        frete REAL,
        FOREIGN KEY (IDCliente) REFERENCES Clientes(IDCliente)
        )'''
        table = self.createTable(self.names.pedidos, columns)

        return table
    
    def itensPedido(self) -> str:
        columns = '''(
        IDPedido INTEGER,
        IDProduto INTEGER,
        quantidade INTEGER CHECK (quantidade > 0),
        FOREIGN KEY (IDPedido) REFERENCES Pedidos(IDPedido),
        FOREIGN KEY (IDProduto) REFERENCES Produtos(IDProduto)
        )'''
        table = self.createTable(self.names.itensPedido, columns)

        return table
