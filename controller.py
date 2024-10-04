"""Import modules"""
from database import DB
from user import User
import random
from faker import Faker
from mysql.connector import Error

class Controller:

    def __init__(self, user: User):
        self.user = user
        self.faker = Faker('en_US')
        self.fornecedores_ids = []
        self.categorias_ids = []
        self.produtos_ids = []
        self.clientes_ids = []
        self.pedidos_ids = []

    def createDatabase(self, db: DB):
        database = db
        try:
            database.createDatabase(self.user)
        except Exception as e:
            print(e)

        return db.userConnect(self.user)

    def createTables(self, db: DB) -> None:
        try:
            if db.userConnect(self.user):
                db.createTables()
        except Exception as e:
            print(e)

    def close(self, db: DB) -> None:
        db.close()

    def checkSSN(self, db: DB, ssn: str) -> bool:
        query = "SELECT CPF FROM Clientes WHERE CPF = %s"  
        db.cursor.execute(query, (ssn,))

        return db.cursor.fetchone() is not None

    def insertFornecedores(self, db: DB, qtd_fornecedores: int = 15) -> None:
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

    def insertCategorias(self, db: DB, qtd_categorias: int = 15) -> None:
        categorias_names = [
            'Food', 'Electronics', 'Clothing', 'Books', 'Furniture', 
            'Toys', 'Tools', 'Sporting Goods', 'Automotive', 'Health & Beauty', 
            'Home & Garden', 'Jewelry', 'Music', 'Movies', 'Pet Supplies', 'Software', 
            'Video Games'
            ]
        for _ in range(qtd_categorias):
            name = categorias_names.pop(random.randint(0, len(categorias_names)-1))
            description = self.faker.sentence()
            query = '''
                    INSERT INTO Categorias (IDFornecedor, nomeCategoria, descricao)
                    VALUES (%s, %s, %s)
                    '''
            db.insertData(query, (random.choice(self.fornecedores_ids), name, description))
            self.categorias_ids.append(db.cursor.lastrowid)

    def insertProdutos(self, db: DB, qtd_produtos: int = 15) -> None:
        for _ in range(qtd_produtos):
            name = self.faker.word()
            price = round(random.uniform(10.0, 1000.0), 2)
            stock = random.randint(10, 500)
            query = '''
                    INSERT INTO Produtos (IDCategoria, nomeProduto, precoUnitario, estoque)
                    VALUES (%s, %s, %s, %s)
                    '''
            db.insertData(query, (random.choice(self.categorias_ids), name, price, stock))
            self.produtos_ids.append(db.cursor.lastrowid)

    def insertClientes(self, db: DB, qtd_clientes: int = 70) -> None:
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
        for _ in range(qtd_pedidos):
            cliente_id = random.choice(self.clientes_ids)
            data_pedido = self.faker.date_this_year()
            frete = round(random.uniform(10.0, 50.0), 2)

            # Initiate transaction
            try:
                db.connection.start_transaction()

                query = '''
                        INSERT INTO Pedidos (IDCliente, data, frete)
                        VALUES (%s, %s, %s)
                        '''
                db.cursor.execute(query, (cliente_id, data_pedido, frete))
                pedido_id = db.cursor.lastrowid
                self.pedidos_ids.append(pedido_id)

                # Insert order items
                qtd_itens = random.randint(1, 5)
                for _ in range(qtd_itens):
                    produto_id = random.choice(self.produtos_ids)
                    quantidade = random.randint(1, 10)

                    query_item = '''
                                INSERT INTO ItemPedidos (IDPedido, IDProduto, quantidade)
                                VALUES (%s, %s, %s)
                                '''
                    db.cursor.execute(query_item, (pedido_id, produto_id, quantidade))

                db.connection.commit()

            except Error as e:
                print(f"Error while inserting order and items: {e}")
                db.connection.rollback()


"""
faker = Faker('en_US')  # Definimos a localidade dos EUA para gerar SSN corretamente
faker.unique = True

# Instancing entities
database = DB(db='sistema_vendas')
user = User()

# Creating the database and tables
try:
    database.createDatabase(user)
    if database.userConnect(user):
        database.createTables()

except Exception as e:
    print(e)


def genSSN():
    return faker.unique.ssn()

def checkSSN(ssn: str) -> bool:
    query = "SELECT CPF FROM Clientes WHERE CPF = %s"  
    database.cursor.execute(query, (ssn,))
    return database.cursor.fetchone() is not None

# Insert Fornecedores function
def insertFornecedores(qtd_fornecedores: int = 15):
    global fornecedores_ids
    fornecedores_ids = []

    for _ in range(qtd_fornecedores):
        nome = faker.company()
        rua = faker.street_name()
        numero = faker.building_number()
        bairro = faker.city()
        cidade = faker.city()
        query = '''
                INSERT INTO Fornecedores (nomeFornecedor, ruaFornecedor, numeroFornecedor, bairroFornecedor, cidadeFornecedor)
                VALUES (%s, %s, %s, %s, %s)
                '''
        database.insertData(query, (nome, rua, numero, bairro, cidade))
        fornecedores_ids.append(database.cursor.lastrowid)

# Insert Categorias function
def insertCategorias(qtd_categorias: int = 15):
    global categorias_ids
    categorias_ids = []

    for _ in range(qtd_categorias):
        nome = faker.word()
        descricao = faker.sentence()
        query = '''
                INSERT INTO Categorias (IDFornecedor, nomeCategoria, descricao)
                VALUES (%s, %s, %s)
                '''
        database.insertData(query, (random.choice(fornecedores_ids), nome, descricao))
        categorias_ids.append(database.cursor.lastrowid)

# Insert Produtos function
def insertProdutos(qtd_produtos: int = 15):
    global produtos_ids
    produtos_ids = []

    for _ in range(qtd_produtos):
        nome = faker.word()
        preco = round(random.uniform(10.0, 1000.0), 2)
        estoque = random.randint(10, 500)
        query = '''
                INSERT INTO Produtos (IDCategoria, nomeProduto, precoUnitario, estoque)
                VALUES (%s, %s, %s, %s)
                '''
        database.insertData(query, (random.choice(categorias_ids), nome, preco, estoque))
        produtos_ids.append(database.cursor.lastrowid)

# Insert Clientes function
def insertClientes(qtd_clientes: int = 70):
    global clientes_ids
    clientes_ids = []

    for _ in range(qtd_clientes):
        ssn = genSSN()
        while checkSSN(ssn):
            ssn = genSSN()

        nome = faker.name()
        rua = faker.street_name()
        numero = faker.building_number()
        bairro = faker.city()
        cidade = faker.city()
        telefone = faker.phone_number()
        email = faker.unique.email()

        query = '''
                INSERT INTO Clientes (CPF, nomeCompleto, rua, numero, bairro, cidade, telefone, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
        database.insertData(query, (ssn, nome, rua, numero, bairro, cidade, telefone, email))
        clientes_ids.append(database.cursor.lastrowid)

# Insert Pedidos function
def insertPedidos(qtd_pedidos: int = 70):
    global pedidos_ids
    pedidos_ids = []

    for _ in range(qtd_pedidos):
        cliente_id = random.choice(clientes_ids)
        data_pedido = faker.date_this_year()
        frete = round(random.uniform(10.0, 50.0), 2)

        # Iniciar transação
        try:
            database.connection.start_transaction()

            query = '''
                    INSERT INTO Pedidos (IDCliente, data, frete)
                    VALUES (%s, %s, %s)
                    '''
            database.cursor.execute(query, (cliente_id, data_pedido, frete))
            pedido_id = database.cursor.lastrowid
            pedidos_ids.append(pedido_id)

            # Inserir itens do pedido
            qtd_itens = random.randint(1, 5)
            for _ in range(qtd_itens):
                produto_id = random.choice(produtos_ids)
                quantidade = random.randint(1, 10)

                query_item = '''
                             INSERT INTO ItemPedidos (IDPedido, IDProduto, quantidade)
                             VALUES (%s, %s, %s)
                             '''
                database.cursor.execute(query_item, (pedido_id, produto_id, quantidade))

            database.connection.commit()

        except Error as e:
            print(f"Error while inserting order and items: {e}")
            database.connection.rollback()


# Executar as inserções
insertFornecedores()
insertCategorias()
insertProdutos()
insertClientes()
insertPedidos()
"""