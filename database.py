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
                host=user.vars.host,
                database=self.db,
                user=user.vars.user,
                password=user.vars.password
            )

            self.cursor = self.connection.cursor()
            return True
        
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def create_database(self, user) -> None:
        """Create the database"""
        try:
            # Connects without the especific database
            self.connection = mysql.connector.connect(
                host=user.vars.host,
                user=user.vars.user,
                password=user.vars.password
            )
            self.cursor = self.connection.cursor()
            
            # Create the database if not exists
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.db}`")
            self.connection.commit()
            print(f"Database: '{self.db}' already exists.")

        except Error as e:
            raise e
        
        finally:
            if self.cursor:
                # Close the cursor
                self.cursor.close()

            if self.connection:
                # Close the connection
                self.connection.close()

    def close(self) -> None:
        if self.connection:
            self.connection.close()

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
                print("Tabela 'Fornecedores' criada com sucesso.")

            except Error as e:
                print(f"Erro ao criar a tabela 'Fornecedores': {e}")
            
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
                print("Tabela 'Categorias' criada com sucesso.")

            except Error as e:
                print(f"Erro ao criar a tabela 'Categorias': {e}")

    def createProdutos(self) -> None:
        """Create the table 'Produtos'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS Produtos (
                    IDProduto INTEGER PRIMARY KEY AUTO_INCREMENT,
                    IDCategoria INTEGER,
                    nomeProduto TEXT,
                    precoUnitario REAL,
                    estoque INTEGER,
                    FOREIGN KEY (IDCategoria) REFERENCES Categorias(IDCategoria)
                )''')
                self.connection.commit()
                print("Tabela 'Produtos' criada com sucesso.")

            except Error as e:
                print(f"Erro ao criar a tabela 'Produtos': {e}")

    def createClientes(self) -> None:
        """Create the table 'Clientes'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                    IDCliente INTEGER PRIMARY KEY AUTO_INCREMENT,
                    CPF TEXT,
                    nomeCompleto TEXT,
                    rua TEXT,
                    numero TEXT,
                    bairro TEXT,
                    cidade TEXT,
                    telefone TEXT,
                    email TEXT
                )''')
                self.connection.commit()
                print("Tabela 'Clientes' criada com sucesso.")

            except Error as e:
                print(f"Erro ao criar a tabela 'Clientes': {e}")

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
                print("Tabela 'Pedidos' criada com sucesso.")

            except Error as e:
                print(f"Erro ao criar a tabela 'Pedidos': {e}")

    def createItemPedidos(self) -> None:
        """Create the table 'ItemPedidos'"""
        if self.connection:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS ItemPedidos (
                    IDPedido INTEGER,
                    IDProduto INTEGER,
                    quantidade INTEGER,
                    FOREIGN KEY (IDPedido) REFERENCES Pedidos(IDPedido),
                    FOREIGN KEY (IDProduto) REFERENCES Produtos(IDProduto)  -- Corrigido: adicionei o fechamento correto aqui
                )''')
                self.connection.commit()
                print("Tabela 'ItemPedidos' criada com sucesso.")

            except Error as e:
                print(f"Erro ao criar a tabela 'ItemPedidos': {e}")

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
                print("Dados inseridos com sucesso.")

            except Error as e:
                print(f"Erro ao inserir dados: {e}")

