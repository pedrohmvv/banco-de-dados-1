"""Main module of the application."""

if __name__ == '__main__':
    from insert import insertFornecedores, insertCategorias, insertProdutos, insertClientes, insertPedidosItens

    insertFornecedores()
    insertCategorias()
    insertProdutos()
    insertClientes()
    insertPedidosItens()
    print('Dados inseridos com sucesso!')

