"""Import modules"""
from src.database import DB
from src.user import User
from src.items import Items

import random
from faker import Faker
from mysql.connector import Error

class Controller:
    """Database controller class"""

    def __init__(self, user: User):
        self.user = user

        self.items = Items()

        self.faker = Faker('en_US')
        self.fornecedores_ids = []
        self.categorias_ids = []
        self.produtos_ids = []
        self.clientes_ids = []
        self.pedidos_ids = []

    def createDatabase(self, db: DB) -> bool:
        """Create the database passed

        Args: db (DB): Database object
        return: bool
        """
        database = db
        try:
            database.createDatabase(self.user)
        except Exception as e:
            print(e)

        return db.userConnect(self.user)

    def createTables(self, db: DB) -> None:
        """Creates the database tables
        
        Args: db (DB): Database object
        return: None
        """
        try:
            if db.userConnect(self.user):
                db.createTables()
        except Exception as e:
            print(e)

    def close(self, db: DB) -> None:
        """Close the database connection
        
        Args: db (DB): Database object
        return: None
        """
        db.close()

    def checkSSN(self, db: DB, ssn: str) -> bool:
        """Check if the SSN exists in the database

        Args: db (DB): Database object
              ssn (str): Social Security Number
        return: bool
        """
        query = "SELECT CPF FROM Clientes WHERE CPF = %s"  
        db.cursor.execute(query, (ssn,))

        return db.cursor.fetchone() is not None

    def insertFornecedores(self, db: DB, qtd_fornecedores: int = 15) -> None:
        """Insert Fornecedores data into the database
        
        Args: db (DB): Database object
                qtd_fornecedores (int): Number of suppliers to insert
        return: None
        """
        for _ in range(qtd_fornecedores):
            name = self.faker.company()
            street = self.faker.street_name()
            number = self.faker.building_number()
            neighborhood = self.faker.city()
            city = self.faker.city()
            query = '''
                    INSERT INTO Fornecedores (nomeFornecedor, ruaFornecedor, numeroFornecedor, bairroFornecedor, cidadeFornecedor)
                    VALUES (%s, %s, %s, %s, %s)
                    '''
            db.insertData(query, (name,street,number,neighborhood,city))
            self.fornecedores_ids.append(db.cursor.lastrowid)

    def insertCategorias(self, db: DB) -> None:
        """Insert Categorias data into the database
        
        Args: db (DB): Database object
                qtd_categorias (int): Number of categories to insert 
        return: None
        """
        categories = list(self.items.products_for_categories.keys())
        description = self.items.category_descriptions

        for category in categories:
            description = self.items.category_descriptions[category]
            query = '''
                    INSERT INTO Categorias (IDFornecedor, nomeCategoria, descricao)
                    VALUES (%s, %s, %s)
                    '''
            db.insertData(query, (random.choice(self.fornecedores_ids), category, description))
            self.categorias_ids.append(db.cursor.lastrowid)

    def insertProdutos(self, db: DB) -> None:
        """Insert Produtos data into the database

        Args: db (DB): Database object
            qtd_produtos (int): Number of products to insert
        return: None
        """
        # Lista de produtos correspondentes às suas categorias com preços
        products_with_prices = self.items.products_for_categories
        categories = list(products_with_prices.keys())

        # Criando um dicionário para mapear nome da categoria com o ID
        categoria_nome_to_id = {nome: id_ for nome, id_ in zip(
            categories,
            self.categorias_ids
        )}

        for category, products in products_with_prices.items():
            categoria_id = categoria_nome_to_id[category]
            for product_name, product_price in products:
                stock = random.randint(10, 500)
                query = '''
                        INSERT INTO Produtos (IDCategoria, nomeProduto, precoUnitario, estoque)
                        VALUES (%s, %s, %s, %s)
                        '''
                db.insertData(query, (categoria_id, product_name, product_price, stock))
                self.produtos_ids.append(db.cursor.lastrowid)


    def insertClientes(self, db: DB, qtd_clientes: int = 70) -> None:
        """Insert Clientes data into the database
        
        Args: db (DB): Database object
                qtd_clientes (int): Number of clients to insert
        return: None
        """
        for _ in range(qtd_clientes):
            ssn = self.faker.unique.ssn()
            while self.checkSSN(db, ssn):
                ssn = self.faker.unique.ssn()

            name = self.faker.name()
            street = self.faker.street_name()
            number = self.faker.building_number()
            neighborhood = self.faker.city()
            city = self.faker.city()
            phone = self.faker.phone_number()
            email = self.faker.unique.email()

            query = '''
                    INSERT INTO Clientes (CPF, nomeCompleto, rua, numero, bairro, cidade, telefone, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
            db.insertData(query, (ssn, name, street, number, neighborhood, city, phone, email))
            self.clientes_ids.append(db.cursor.lastrowid)

    def insertPedidos(self, db: DB, qtd_pedidos: int = 70) -> None:
        """Insert Pedidos data into the database

        Args: db (DB): Database object
                qtd_pedidos (int): Number of orders to insert
        return: None
        """
        for _ in range(qtd_pedidos):
            cliente_id = random.choice(self.clientes_ids)
            order_date = self.faker.date_this_year()
            transport_tax = round(random.uniform(10.0, 50.0), 2)

            # Initiate transaction
            try:
                db.connection.start_transaction()

                query = '''
                        INSERT INTO Pedidos (IDCliente, data, frete)
                        VALUES (%s, %s, %s)
                        '''
                db.cursor.execute(query, (cliente_id, order_date, transport_tax))
                order_id = db.cursor.lastrowid
                self.pedidos_ids.append(order_id)

                # Insert order items
                itens_quantity = random.randint(1, 5)
                for _ in range(itens_quantity):
                    product_id = random.choice(self.produtos_ids)
                    quantity = random.randint(1, 10)

                    query_item = '''
                                INSERT INTO ItemPedidos (IDPedido, IDProduto, quantidade)
                                VALUES (%s, %s, %s)
                                '''
                    db.cursor.execute(query_item, (order_id, product_id, quantity))

                db.connection.commit()

            except Error as e:
                print(f"Error while inserting order and items: {e}")
                db.connection.rollback()