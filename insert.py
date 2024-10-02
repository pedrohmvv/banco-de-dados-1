"""Import modules"""
from database import DB
from user import User

"""Import libs"""
import random
from faker import Faker

faker = Faker()

# Instancing entities
database = DB(db='sistema_vendas')
user = User()

# Creating the database and tables
try:
    # Connecting to the database
    database.create_database(user)

    if database.userConnect(user):
        # Create the tables
        database.createTables()

except Exception as e:
    print(e)


# Insert Fornecedores function
def insertFornecedores(qtd_fornecedores:int = 15):
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
def insertCategorias(qtd_categorias:int = 15):
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
def insertProdutos(qtd_produtos:int = 15):
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
def insertClientes(qtd_clientes:int = 70):
    global clientes_ids
    clientes_ids = []

    for _ in range(qtd_clientes):
        cpf = faker.ssn()
        nome = faker.name()
        rua = faker.street_name()
        numero = faker.building_number()
        bairro = faker.city()
        cidade = faker.city()
        telefone = faker.phone_number()
        email = faker.email()
        query = '''
                INSERT INTO Clientes (CPF, nomeCompleto, rua, numero, bairro, cidade, telefone, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
        database.insertData(query, (cpf, nome, rua, numero, bairro, cidade, telefone, email))
        clientes_ids.append(database.cursor.lastrowid)

# Insert ItemPedidos function
def insertPedidosItens(qtd_pedidos:int = 3000):
    for _ in range(qtd_pedidos):
        cliente_id = random.choice(clientes_ids)
        data = faker.date_this_year()
        frete = round(random.uniform(5.0, 50.0), 2)
        query = '''
                INSERT INTO Pedidos (IDCliente, data, frete)
                VALUES (%s, %s, %s)
                '''
        database.insertData(query, (cliente_id, data, frete))
        pedido_id = database.cursor.lastrowid

        # Each order can have 1 to 5 items
        for _ in range(random.randint(1, 5)):
            produto_id = random.choice(produtos_ids)
            quantidade = random.randint(1, 10)
            query = '''
                    INSERT INTO ItemPedidos (IDPedido, IDProduto, quantidade)
                    VALUES (%s, %s, %s)
                    '''
            database.insertData(query, (pedido_id, produto_id, quantidade))

# Inserir all data
def main():
    insertFornecedores()
    insertCategorias()
    insertProdutos()
    insertClientes()
    insertPedidosItens()