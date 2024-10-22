"""Import modules"""
from src.database import DB
from src.user import User
from src.config.items import Items

import logging
import random
from faker import Faker
from datetime import datetime, date, timedelta
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
        self.funcionarios_ids = []

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
    
    def insertCargos(self, db: DB) -> None:
        """Insert Cargos data into the database"""
        logging.info("Inserting positions...")

        table_name = db.tables.names.cargos
        cargos_columns = db.getColumns(table=table_name, insert=True)

        for position, salary in self.items.cargos.items():
            description = f"Position of {position} with a salary of ${salary}."
            db.insertData(
                table=table_name,
                columns=cargos_columns,
                values=(position, salary, description)
            )

        logging.info("Positions inserted successfully.")

    def insertFuncionarios(self, db: DB, qtd_vendedores: int = 50)-> None:
        """Insert Vendedores data into the database"""
        logging.info(f"Inserting {qtd_vendedores} sellers...")

        table_name = db.tables.names.funcionarios
        funcionarios_columns = db.getColumns(table=table_name, insert=True)

        for _ in range(qtd_vendedores):
            cargo_id = random.randint(1, len(self.items.cargos))
            name = self.faker.name()
            
            #Hiring date must be at least 18 years after the birth date
            birth_date = self.faker.date_of_birth(minimum_age=18, maximum_age=65)
            min_hire_date = birth_date + timedelta(days=18*365)
            hire_date = self.faker.date_between_dates(date_start=min_hire_date, date_end=date.today())

            firing_date = None
            if random.choices([True, False], weights=[20, 80], k=1)[0]:  # 20% firing chance
                firing_date = self.faker.date_between_dates(date_start=hire_date, date_end=date.today())

            db.insertData(
                table=table_name,
                columns=funcionarios_columns,
                values=(cargo_id, name, birth_date, hire_date, firing_date)
            )
            self.funcionarios_ids.append(db.cursor.lastrowid)

        logging.info(f"{qtd_vendedores} sellers inserted successfully.")

    def insertFornecedores(self, db: DB, qtd_fornecedores: int = 17) -> None:
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

        for i, category in enumerate(categories):
            description = self.items.category_descriptions.get(category)

            db.insertData(
                table=table_name,
                columns=categories_columns,
                values=(self.fornecedores_ids[i], category, description)
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

        # IDvendedor must be a id from the vendedores table where IDCargo = 2 (Salesperson)
        query = "SELECT IDFuncionario, dataContratacao, dataDesligamento FROM Funcionarios WHERE IDCargo = 2"
        db.cursor.execute(query)
        id_vendedores = db.cursor.fetchall()

        for _ in range(qtd_pedidos):
            table_name = db.tables.names.pedidos
            pedidos_columns = db.getColumns(table=table_name, insert=True)

            # Choose a random salesperson and check if they were employed on the order date
            id_vendedor, hire_date, firing_date = random.choice(id_vendedores)

            client_id = random.choice(self.clientes_ids)
            freight = round(random.uniform(10, 100), ndigits=2)
            order_time = f'{random.randint(8, 18)}:{random.randint(0, 59)}:{random.randint(0, 59)}' 

            if isinstance(hire_date, str):
                hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
            if firing_date is not None and isinstance(firing_date, str):
                firing_date = datetime.strptime(firing_date, '%Y-%m-%d').date()

            order_date = self.faker.date_between_dates(date_start=hire_date, date_end=date.today())

            # Check if the salesperson was employed on the order date
            if (hire_date <= order_date) and (firing_date is None or order_date <= firing_date):
                try:
                    db.insertData(
                        table=table_name,
                        columns=pedidos_columns,
                        values=(client_id, id_vendedor, order_date, order_time, freight)
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

                    logging.info(f"Order {order_id} inserted successfully.")

                except Error as e:
                    logging.error(f"Error while inserting order: {e}")
                    db.connection.rollback()
            else:
                logging.info(f"Order not inserted for vendor {id_vendedor} because they were not employed on {order_date}.")
