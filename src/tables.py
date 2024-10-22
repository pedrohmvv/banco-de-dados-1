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
    funcionarios: str
    cargos: str

class Tables:
    """Tables class"""
    def __init__(self):
        names_data = {}
        with open(join(dirname(abspath(__file__)), 'tables_names.yaml'), encoding='utf-8') as file:
            names_data = load(file, Loader=SafeLoader)

        self.names = TablesNames(
            fornecedores=names_data.get('fornecedores'),
            categorias=names_data.get('categorias'),
            produtos=names_data.get('produtos'),
            clientes=names_data.get('clientes'),
            pedidos=names_data.get('pedidos'),
            itensPedido=names_data.get('itensPedido'),
            funcionarios=names_data.get('funcionarios'),
            cargos=names_data.get('cargos')
        )
        
    def createTable(self, name: str, columns: str) -> str:
        """Create the table"""
        table = ' '.join([name, columns])
        return table

    def cargos(self) -> str:
        """Create the table 'Cargos'"""
        columns_types = '''(
        IDCargo INTEGER PRIMARY KEY AUTO_INCREMENT,
        nomeCargo TEXT,
        salario REAL CHECK (salario > 0),
        descricao TEXT
        )'''
        table = self.createTable(self.names.cargos, columns_types)

        return table
    
    def funcionarios(self) -> str:
        """Create the table 'Vendedores'"""
        columns_types = '''(
        IDFuncionario INTEGER PRIMARY KEY AUTO_INCREMENT,
        IDCargo INTEGER,
        nomeVendedor TEXT,
        dataNascimentoVendedores TEXT,
        dataContratacao TEXT,
        dataDesligamento TEXT,
        FOREIGN KEY (IDCargo) REFERENCES Cargos(IDCargo) ON DELETE SET NULL
        )'''
        table = self.createTable(self.names.funcionarios, columns_types)

        return table
    
    def fornecedores(self) -> str:
        """Create the table 'Fornecedores'"""
        columns_types = '''(
        IDFornecedor INTEGER PRIMARY KEY AUTO_INCREMENT,
        nomeFornecedor TEXT,
        ruaFornecedor TEXT,
        numeroFornecedor INTEGER,
        bairroFornecedor TEXT,
        cidadeFornecedor TEXT
        )'''
        table = self.createTable(self.names.fornecedores, columns_types)         
        
        return table
    
    def categorias(self) -> str:
        """Create the table 'Categorias'"""
        columns_types = '''(
        IDCategoria INTEGER PRIMARY KEY AUTO_INCREMENT,
        IDFornecedor INTEGER,
        nomeCategoria TEXT,
        descricao TEXT,
        FOREIGN KEY (IDFornecedor) REFERENCES Fornecedores(IDFornecedor) ON DELETE CASCADE
        )'''
        table = self.createTable(self.names.categorias, columns_types)

        return table
    
    def produtos(self) -> str:
        """Create the table 'Produtos'"""
        columns_types = '''(
        IDProduto INTEGER PRIMARY KEY AUTO_INCREMENT,
        IDCategoria INTEGER,
        nomeProduto TEXT,
        precoUnitario REAL CHECK (precoUnitario > 0),
        estoque INTEGER CHECK (estoque >= 0),
        FOREIGN KEY (IDCategoria) REFERENCES Categorias(IDCategoria) ON DELETE CASCADE
        )'''
        table = self.createTable(self.names.produtos, columns_types)

        return table

    def clientes(self) -> str:
        """Create the table 'Clientes'"""
        columns_types = '''(
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
        table = self.createTable(self.names.clientes, columns_types)

        return table
    
    def pedidos(self) -> str:
        """Create the table 'Pedidos'"""
        columns_types = '''(
        IDPedido INTEGER PRIMARY KEY AUTO_INCREMENT,
        IDCliente INTEGER,
        IDFuncionario INTEGER,
        data TEXT,
        frete REAL,
        FOREIGN KEY (IDCliente) REFERENCES Clientes(IDCliente) ON DELETE CASCADE,
        FOREIGN KEY (IDFuncionario) REFERENCES Funcionarios(IDFuncionario) ON DELETE SET NULL
        )'''
        table = self.createTable(self.names.pedidos, columns_types)

        return table
    
    def itensPedido(self) -> str:
        """Create the table 'ItensPedido'"""
        columns_types = '''(
        IDPedido INTEGER,
        IDProduto INTEGER,
        quantidade INTEGER CHECK (quantidade > 0),
        FOREIGN KEY (IDPedido) REFERENCES Pedidos(IDPedido) ON DELETE CASCADE,
        FOREIGN KEY (IDProduto) REFERENCES Produtos(IDProduto) ON DELETE CASCADE
        )'''
        table = self.createTable(self.names.itensPedido, columns_types)

        return table
