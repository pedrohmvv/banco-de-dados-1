Aqui está um exemplo de README para o seu projeto:

---

# Sistema de Gestão de Vendas - Banco de Dados I

Este projeto faz parte do trabalho prático da disciplina **Banco de Dados I** do curso de **Ciência de Dados** na **Universidade Federal da Paraíba (UFPB)**. O sistema simula uma plataforma de gestão de vendas, incluindo fornecedores, produtos, clientes, pedidos e itens de pedidos, utilizando o MySQL como sistema de gerenciamento de banco de dados.

## Objetivo

O objetivo principal do projeto é a construção de um sistema de banco de dados que permita o gerenciamento eficiente de um sistema de vendas, explorando as funcionalidades e boas práticas do design e manipulação de dados, como criação de tabelas, inserção e recuperação de dados, e gerenciamento de transações.

## Funcionalidades

O sistema permite:

- **Gerenciamento de Fornecedores**: Registro de fornecedores com informações como nome, endereço e cidade.
- **Gerenciamento de Categorias**: Organização dos produtos em categorias (ex: alimentos, eletrônicos, móveis).
- **Gerenciamento de Produtos**: Registro de produtos com informações como nome, preço e estoque disponível.
- **Gerenciamento de Clientes**: Cadastro de clientes com nome, CPF, endereço e informações de contato.
- **Gerenciamento de Pedidos**: Registro de pedidos realizados pelos clientes, incluindo a data e o valor do frete.
- **Gerenciamento de Itens de Pedidos**: Registro dos itens comprados em cada pedido, com quantidade e relação ao produto.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação usada para implementação da lógica de inserção de dados e conexão com o banco de dados.
- **MySQL**: Sistema de gerenciamento de banco de dados relacional.
- **Faker**: Biblioteca Python para geração de dados fictícios (nomes, endereços, produtos, etc.).
- **MySQL Connector**: Biblioteca Python para conexão e execução de comandos no MySQL.

## Estrutura do Banco de Dados

O banco de dados é composto pelas seguintes tabelas:

1. **Fornecedores**: Contém informações dos fornecedores.
2. **Categorias**: Armazena categorias dos produtos.
3. **Produtos**: Detalha os produtos oferecidos pelo sistema.
4. **Clientes**: Armazena as informações dos clientes.
5. **Pedidos**: Registra os pedidos feitos pelos clientes.
6. **ItemPedidos**: Armazena os itens que compõem cada pedido.

### Diagrama ER Simplificado

![Diagrama ER](link-diagrama)

## Instalação

### Pré-requisitos

- **Python 3.x** instalado
- **MySQL** instalado e rodando

### Passos para rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema-vendas.git
cd sistema-vendas
```

2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

3. Configure as credenciais de acesso ao MySQL no arquivo `user.py`.

4. Execute o script para criar o banco de dados e as tabelas:

```bash
python main.py
```

## Uso

Ao executar o sistema, as tabelas serão criadas e automaticamente preenchidas com dados fictícios gerados pela biblioteca Faker. Isso inclui fornecedores, categorias, produtos, clientes, pedidos e itens de pedidos.

O código está preparado para gerenciar transações e garantir a integridade dos dados em casos de falhas durante o processo de inserção.

---
