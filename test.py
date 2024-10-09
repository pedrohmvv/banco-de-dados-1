from src.database import DB
from src.user import User

db = DB()
user = User()

db.createDatabase(user=user)
db.userConnect(user=user)
db.createTables()
print(db.getColumns(table=db.tables.names.fornecedores))