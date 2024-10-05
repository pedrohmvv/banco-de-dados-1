import mysql.connector
from mysql.connector import Error

class DB:
    """Database class"""
    def __init__(self, db: str = 'sistema_vendas') -> None:
        self.db = db
        self.connection = None
        self.cursor = None

    def userConnect(self, user) -> bool:
        """Connect to the database"""
        try:
            self.connection = mysql.connector.connect(
                host=user.creds.host,
                database=self.db,
                user=user.creds.user,
                password=user.creds.password
            )

            self.cursor = self.connection.cursor()
            return True
        
        except Error as e:
            print(f"Error while trying to connect to database: {e}")
            return False

    def createDatabase(self, user) -> None:
        """Create the database"""
        try:
            self.connection = mysql.connector.connect(
                host=user.creds.host,
                user=user.creds.user,
                password=user.creds.password
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.db}`")
            self.connection.commit()

        except Error as e:
            print(f"Error while creating database: {e}")
        
        # Close the connection after creating the database
        finally:
            if self.cursor:
                self.close()

    def close(self) -> None:
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

    def createFornecedores(self) -> None:
        """Create the table 'Fornecedores'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS Fornecedores (
                    IDFornecedor INTEGER PRIMARY KEY AUTO_INCREMENT,
                    nomeFornecedor TEXT,
                    ruaFornecedor TEXT,
                    numeroFornecedor INTEGER,
                    bairroFornecedor TEXT,
                    cidadeFornecedor TEXT
                )''')
                self.connection.commit()
                print("Table 'Fornecedores' created with success.")

            except Error as e:
                print(f"Error while creating table 'Fornecedores': {e}")

    def createCategorias(self) -> None:
        """Create the table 'Categorias'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS Categorias (
                    IDCategoria INTEGER PRIMARY KEY AUTO_INCREMENT,
                    IDFornecedor INTEGER,
                    nomeCategoria TEXT,
                    descricao TEXT,
                    FOREIGN KEY (IDFornecedor) REFERENCES Fornecedores(IDFornecedor)
                )''')
                self.connection.commit()
                print("Created table 'Categorias' with success.")

            except Error as e:
                print(f"Error while creating table 'Categorias': {e}")

    def createProdutos(self) -> None:
        """Create the table 'Produtos'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS Produtos (
                    IDProduto INTEGER PRIMARY KEY AUTO_INCREMENT,
                    IDCategoria INTEGER,
                    nomeProduto TEXT,
                    precoUnitario REAL CHECK (precoUnitario > 0),
                    estoque INTEGER CHECK (estoque >= 0),
                    FOREIGN KEY (IDCategoria) REFERENCES Categorias(IDCategoria)
                )''')
                self.connection.commit()
                print("Table 'Produtos' created with success.")

            except Error as e:
                print(f"Error while creating table 'Produtos': {e}")

    def createClientes(self) -> None:
        """Create the table 'Clientes'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                    IDCliente INTEGER PRIMARY KEY AUTO_INCREMENT,
                    CPF VARCHAR(11) UNIQUE,
                    nomeCompleto TEXT,
                    rua TEXT,
                    numero TEXT,
                    bairro TEXT,
                    cidade TEXT,
                    telefone TEXT,
                    email VARCHAR(255) UNIQUE
                )''')
                self.connection.commit()
                print("Table 'Clientes' created with success.")

            except Error as e:
                print(f"Error while creating table 'Clientes': {e}")

    def createPedidos(self) -> None:
        """Create the table 'Pedidos'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pedidos (
                    IDPedido INTEGER PRIMARY KEY AUTO_INCREMENT,
                    IDCliente INTEGER,
                    data TEXT,
                    frete REAL,
                    FOREIGN KEY (IDCliente) REFERENCES Clientes(IDCliente)
                )''')
                self.connection.commit()
                print("Table 'Pedidos' created with success.")

            except Error as e:
                print(f"Error while creating table 'Pedidos': {e}")

    def createItemPedidos(self) -> None:
        """Create the table 'ItemPedidos'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS ItemPedidos (
                    IDPedido INTEGER,
                    IDProduto INTEGER,
                    quantidade INTEGER CHECK (quantidade > 0),
                    FOREIGN KEY (IDPedido) REFERENCES Pedidos(IDPedido),
                    FOREIGN KEY (IDProduto) REFERENCES Produtos(IDProduto)
                )''')
                self.connection.commit()
                print("Table 'ItemPedidos' created with success.")

            except Error as e:
                print(f"Error while creating table 'ItemPedidos': {e}")

    def createTables(self) -> None:
        """Create all tables"""
        self.createFornecedores()
        self.createCategorias()
        self.createProdutos()
        self.createClientes()
        self.createPedidos()
        self.createItemPedidos()

    def insertData(self, query: str, values: tuple) -> None:
        """Insert generic data into the database"""
        if self.connection:
            try:
                self.cursor.execute(query, values)
                self.connection.commit()
                print(f"Data inserted successfully.")

            except Error as e:
                print(f"Error while inserting data: {e}")