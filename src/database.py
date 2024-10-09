import logging
import mysql.connector
from mysql.connector import Error

from src.user import User
from src.tables import Tables

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DB:
    """Database class"""
    def __init__(self, db: str = 'sistema_vendas') -> None:
        self.tables = Tables()
        self.db = db
        self.connection = None
        self.cursor = None
        self.create_query = 'CREATE TABLE IF NOT EXISTS'

    def userConnect(self, user: User) -> bool:
        """Connect to the database
        
        Args: user (User): User object
        return: bool
        """
        try:
            self.connection = mysql.connector.connect(
                host=user.creds.HOST,
                user=user.creds.USER,
                password=user.creds.PASSWORD,
                database=self.db
            )

            self.cursor = self.connection.cursor()
            logging.info(f"Connected to the database '{self.db}' successfully.")
            return True
        
        except Error as e:
            logging.error(f"Error while trying to connect to database: {e}")
            return False

    def createDatabase(self, user: User) -> None:
        """Create the database
        
        Args: user (User): User object
        return: None
        """
        try:
            self.connection = mysql.connector.connect(
                host=user.creds.HOST,
                user=user.creds.USER,
                password=user.creds.PASSWORD
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.db}`")
            self.connection.commit()
            logging.info(f"Database '{self.db}' created successfully.")

        except Error as e:
            logging.error(f"Error while creating database: {e}")
        
        finally:
            if self.cursor:
                self.close()

    def close(self) -> None:
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Database connection closed.")

    def createQuery(self, table: str) -> str:
        """Create the query to create a table
        
        Args: table (str): Table name
        return: str
        """
        query = ' '.join([self.create_query, table])
        return query

    def createFornecedores(self) -> None:
        """Create the table 'Fornecedores'"""
        if self.connection:
            try:
                fornecedores = self.createQuery(self.tables.fornecedores())
                self.cursor.execute(fornecedores)
                self.connection.commit()
                logging.info(f"Table '{self.tables.names.fornecedores}' created successfully.")

            except Error as e:
                logging.error(f"Error while creating table '{self.tables.names.fornecedores}': {e}")

    def createCategorias(self) -> None:
        """Create the table 'Categorias'"""
        if self.connection:
            try:
                categorias = self.createQuery(self.tables.categorias())
                self.cursor.execute(categorias)
                self.connection.commit()
                logging.info(f"Table '{self.tables.names.categorias}' created successfully.")

            except Error as e:
                logging.error(f"Error while creating table '{self.tables.names.categorias}': {e}")

    def createProdutos(self) -> None:
        """Create the table 'Produtos'"""
        if self.connection:
            try:
                produtos = self.createQuery(self.tables.produtos())
                self.cursor.execute(produtos)
                self.connection.commit()
                logging.info(f"Table '{self.tables.names.produtos}' created successfully.")

            except Error as e:
                logging.error(f"Error while creating table '{self.tables.names.produtos}': {e}")

    def createClientes(self) -> None:
        """Create the table 'Clientes'"""
        if self.connection:
            try:
                clientes = self.createQuery(self.tables.clientes())
                self.cursor.execute(clientes)
                self.connection.commit()
                logging.info(f"Table '{self.tables.names.clientes}' created successfully.")

            except Error as e:
                logging.error(f"Error while creating table '{self.tables.names.clientes}': {e}")

    def createPedidos(self) -> None:
        """Create the table 'Pedidos'"""
        if self.connection:
            try:
                pedidos = self.createQuery(self.tables.pedidos())
                self.cursor.execute(pedidos)
                self.connection.commit()
                logging.info(f"Table '{self.tables.names.pedidos}' created successfully.")

            except Error as e:
                logging.error(f"Error while creating table '{self.tables.names.pedidos}': {e}")

    def createItemPedidos(self) -> None:
        """Create the table 'ItemPedidos'"""
        if self.connection:
            try:
                itemPedidos = self.createQuery(self.tables.itensPedido())
                self.cursor.execute(itemPedidos)
                self.connection.commit()
                logging.info(f"Table '{self.tables.names.itensPedido}' created successfully.")

            except Error as e:
                logging.error(f"Error while creating table '{self.tables.names.itensPedido}': {e}")

    def createTables(self) -> None:
        """Create all tables"""
        self.createFornecedores()
        self.createCategorias()
        self.createProdutos()
        self.createClientes()
        self.createPedidos()
        self.createItemPedidos()

    def insertData(self, table: str, columns: str, values: tuple) -> None:
        """Insert generic data into the database
        
        Args: table (str): Table name
                columns (str): Columns to insert
                values (tuple): Values to insert 
        return: None
        """
        logging.info(f"Inserting data into table '{table}'")
        insert_query = "INSERT INTO"
        placeholders = ', '.join(['%s' for _ in range(len(values))])
        query = f"{insert_query} {table} ({columns}) VALUES ({placeholders})"

        if self.connection:
            try:
                logging.info(f"Executing query: {query} with values: {values}")
                self.cursor.execute(query, values)
                self.connection.commit()
                logging.info(f"Data inserted successfully into table '{table}'.")

            except Error as e:
                logging.error(f"Error while inserting data into table '{table}': {e}")

    def getColumns(self, table: str, insert: bool = False) -> list:
        """Get the columns of a table
        
        Args: table (str): Table name
                insert (bool): If the columns are for insert or not (default: False)
        return: list
        """
        if self.connection:
            try:
                self.cursor.execute(f"DESCRIBE {table}")
                result = self.cursor.fetchall()
                if insert:
                    columns = [column[0] for column in result if 'auto_increment' not in column[-1]]
                else:
                    columns = [column[0] for column in result]
                
                return ', '.join(columns)

            except Error as e:
                logging.error(f"Error while getting columns from table '{table}': {e}")
