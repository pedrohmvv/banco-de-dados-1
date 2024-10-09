import logging
from src.database import DB
from src.user import User
from src.items import Items

import random
from faker import Faker
from mysql.connector import Error

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        """Create the database passed"""
        logging.info("Creating database...")
        try:
            db.createDatabase(self.user)
        except Exception as e:
            logging.error(f"Error while creating database: {e}")
        return db.userConnect(self.user)

    def createTables(self, db: DB) -> None:
        """Creates the database tables"""
        logging.info("Creating tables...")
        try:
            if db.userConnect(self.user):
                db.createTables()
        except Exception as e:
            logging.error(f"Error while creating tables: {e}")

    def close(self, db: DB) -> None:
        """Close the database connection"""
        logging.info("Closing database connection...")
        db.close()

    def checkSSN(self, db: DB, ssn: str) -> bool:
        """Check if the SSN exists in the database"""
        logging.info(f"Checking if SSN {ssn} exists in database...")
        query = "SELECT CPF FROM Clientes WHERE CPF = %s"
        db.cursor.execute(query, (ssn,))
        return db.cursor.fetchone() is not None

    def insertFornecedores(self, db: DB, qtd_fornecedores: int = 15) -> None:
        """Insert Fornecedores data into the database"""
        logging.info(f"Inserting {qtd_fornecedores} suppliers...")
        table_name = db.tables.names.fornecedores
        fornecedores_columns = db.getColumns(table=table_name, insert=True)

        for _ in range(qtd_fornecedores):
            name = self.faker.company()
            street, number, neighborhood, city = self.faker.street_name(), self.faker.building_number(), self.faker.city(), self.faker.city()

            db.insertData(
                table=table_name,
                columns=fornecedores_columns,
                values=(name, street, number, neighborhood, city)
            )
            self.fornecedores_ids.append(db.cursor.lastrowid)
        logging.info(f"Suppliers inserted successfully.")

    def insertCategorias(self, db: DB) -> None:
        """Insert Categorias data into the database"""
        logging.info("Inserting categories...")
        categories = list(self.items.products_for_categories.keys())
        table_name = db.tables.names.categorias
        categories_columns = db.getColumns(table=table_name, insert=True)

        for category in categories:
            description = self.items.category_descriptions[category]

            db.insertData(
                table=table_name,
                columns=categories_columns,
                values=(random.choice(self.fornecedores_ids), category, description)
            )
            self.categorias_ids.append(db.cursor.lastrowid)
        logging.info("Categories inserted successfully.")

    def insertProdutos(self, db: DB) -> None:
        """Insert Produtos data into the database"""
        logging.info("Inserting products...")
        table_name = db.tables.names.produtos
        products_with_prices = self.items.products_for_categories
        categories = list(products_with_prices.keys())
        produtos_columns = db.getColumns(table=table_name, insert=True)

        categoria_nome_to_id = {nome: id_ for nome, id_ in zip(categories, self.categorias_ids)}

        for category, products in products_with_prices.items():
            categoria_id = categoria_nome_to_id[category]
            for product_name, product_price in products:
                stock = random.randint(10, 500)

                db.insertData(
                    table=table_name,
                    columns=produtos_columns,
                    values=(categoria_id, product_name, product_price, stock)
                )
                self.produtos_ids.append(db.cursor.lastrowid)
        logging.info("Products inserted successfully.")

    def insertClientes(self, db: DB, qtd_clientes: int = 70) -> None:
        """Insert Clientes data into the database"""
        logging.info(f"Inserting {qtd_clientes} clients...")
        table_name = db.tables.names.clientes
        clientes_columns = db.getColumns(table=table_name, insert=True)

        for _ in range(qtd_clientes):
            ssn = self.faker.unique.ssn()
            while self.checkSSN(db, ssn):
                ssn = self.faker.unique.ssn()

            name = self.faker.name()
            street, number, neighborhood, city = self.faker.street_name(), self.faker.building_number(), self.faker.city(), self.faker.city()
            phone = self.faker.phone_number()
            email = self.faker.unique.email()

            db.insertData(
                table=table_name,
                columns=clientes_columns,
                values=(ssn, name, street, number, neighborhood, city, phone, email)
            )
            self.clientes_ids.append(db.cursor.lastrowid)
        logging.info(f"{qtd_clientes} clients inserted successfully.")

    def insertPedidos(self, db: DB, qtd_pedidos: int = 70) -> None:
        """Insert Pedidos data into the database"""
        logging.info(f"Inserting {qtd_pedidos} orders...")
        for _ in range(qtd_pedidos):
            table_name = db.tables.names.pedidos
            pedidos_columns = db.getColumns(table=table_name, insert=True)

            client_id = random.choice(self.clientes_ids)
            order_date = self.faker.date_this_year()
            freight = round(random.uniform(10, 100), ndigits=2)

            try:
                db.insertData(
                    table=table_name,
                    columns=pedidos_columns,
                    values=(client_id, order_date, freight)
                )
                order_id = db.cursor.lastrowid
                self.pedidos_ids.append(order_id)

                table_name = db.tables.names.itensPedido
                itensPedido_columns = db.getColumns(table=table_name, insert=True)

                items_quantities = random.randint(1, 5)
                for _ in range(items_quantities):
                    product_id = random.choice(self.produtos_ids)
                    quantity = random.randint(1, 10)

                    db.insertData(
                        table=table_name,
                        columns=itensPedido_columns,
                        values=(order_id, product_id, quantity)
                    )

                db.connection.commit()
                logging.info(f"Order {order_id} inserted successfully.")

            except Error as e:
                logging.error(f"Error while inserting order: {e}")
                db.connection.rollback()
