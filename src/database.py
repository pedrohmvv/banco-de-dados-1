"""import modules"""
import mysql.connector
from mysql.connector import Error

class DB:
    """Database class"""
    def __init__(self, db: str = 'sistema_vendas') -> None:
        from src.tables import Tables
        
        self.tables = Tables()
        self.db = db
        self.connection = None
        self.cursor = None

        self.create_query = 'CREATE TABLE IF NOT EXISTS'


    def userConnect(self, user) -> bool:
        """Connect to the database"""
        try:
            self.connection = mysql.connector.connect(
                host=user.creds.HOST,
                user=user.creds.USER,
                password=user.creds.PASSWORD,
                database=self.db
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
                host=user.creds.HOST,
                user=user.creds.USER,
                password=user.creds.PASSWORD
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

    def createQuery(self, table: str) -> str:
        """Create the query to create a table"""
        query = ' '.join([self.create_query, table])
        return query

    def createFornecedores(self) -> None:
        """Create the table 'Fornecedores'"""
        if self.connection:
            try:
                fornecedores = self.createQuery(self.tables.fornecedores())
                self.cursor.execute(fornecedores)
                self.connection.commit()
                print(f"Table '{self.tables.names.fornecedores}' created with success.")

            except Error as e:
                print(f"Error while creating table '{self.tables.names.fornecedores}': {e}")

    def createCategorias(self) -> None:
        """Create the table 'Categorias'"""
        if self.connection:
            try:
                categorias = self.createQuery(self.tables.categorias())
                self.cursor.execute(categorias)
                self.connection.commit()
                print(f"Table '{self.tables.names.categorias}' created with success.")

            except Error as e:
                print(f"Error while creating table '{self.tables.names.categorias}': {e}")

    def createProdutos(self) -> None:
        """Create the table 'Produtos'"""
        if self.connection:
            try:
                produtos = self.createQuery(self.tables.produtos())
                self.cursor.execute(produtos)
                self.connection.commit()
                print(f"Table '{self.tables.names.produtos}' created with success.")

            except Error as e:
                print(f"Error while creating table '{self.tables.names.produtos}': {e}")

    def createClientes(self) -> None:
        """Create the table 'Clientes'"""
        if self.connection:
            try:
                clientes = self.createQuery(self.tables.clientes())
                self.cursor.execute(clientes)
                self.connection.commit()
                print(f"Table '{self.tables.names.clientes}' created with success.")

            except Error as e:
                print(f"Error while creating table '{self.tables.names.clientes}': {e}")

    def createPedidos(self) -> None:
        """Create the table 'Pedidos'"""
        if self.connection:
            try:
                pedidos = self.createQuery(self.tables.pedidos())
                self.cursor.execute(pedidos)
                self.connection.commit()
                print(f"Table '{self.tables.names.pedidos}' created with success.")

            except Error as e:
                print(f"Error while creating table '{self.tables.names.pedidos}': {e}")

    def createItemPedidos(self) -> None:
        """Create the table 'ItemPedidos'"""
        if self.connection:
            try:
                itemPedidos = self.createQuery(self.tables.itensPedido())
                self.cursor.execute(itemPedidos)
                self.connection.commit()
                print(f"Table '{self.tables.names.itensPedido}' created with success.")

            except Error as e:
                print(f"Error while creating table '{self.tables.names.itensPedido}': {e}")

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