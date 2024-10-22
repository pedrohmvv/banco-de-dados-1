"""Main module of the application."""
from src.controller import Controller
from src.user import User
from src.database import DB

database = DB()
user = User()
controller = Controller(user=user)

if __name__ == "__main__":
    try:
        # Connect to the database
        if controller.createDatabase(db=database):
            print("Database created or connected successfully.")
            
            # Garantee that the database connection is active
            if database.connection:
                controller.createTables(db=database)
                controller.insertCargos(db=database)
                controller.insertFuncionarios(db=database)
                controller.insertClientes(db=database)
                controller.insertFornecedores(db=database)
                controller.insertCategorias(db=database)
                controller.insertProdutos(db=database)
                controller.insertPedidos(db=database)
            else:
                print("Failed to connect to the specific database after creation.")
        else:
            print("Failed to create or connect to the database.")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the database connection
        if database.connection:
            controller.close(db=database)
            print("Database connection closed.")
        else:
            print("No active database connection to close.")



        

