from flask import Blueprint, Flask, jsonify, request
from utils import connect_to_database

produtos_bp = Blueprint('produtos', __name__)



@produtos_bp.route('/produtos', methods=['GET'])
def get_produtos():
    connection = connect_to_database()
    if connection is None:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    cursor = connection.cursor(dictionary=True)

    # Base da consulta
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []

    # Adiciona filtros com base nos parâmetros de consulta
    categoria = request.args.get('categoria')
    if categoria:
        query += " AND categoria LIKE %s"
        params.append(f"%{categoria}%")
    
    nome_produto = request.args.get('nome_produto')
    if nome_produto:
        query += " AND nome_produto LIKE %s"
        params.append(f"%{nome_produto}%")

    marca = request.args.get('marca')
    if marca:
        query += " AND marca LIKE %s"
        params.append(f"%{marca}%")

    cor = request.args.get('cor')
    if cor:
        query += " AND cor LIKE %s"
        params.append(f"%{cor}%")
    
    preco_min = request.args.get('preco_min')
    if preco_min:
        query += " AND preco >= %s"
        params.append(preco_min)

    preco_max = request.args.get('preco_max')
    if preco_max:
        query += " AND preco <= %s"
        params.append(preco_max)

    # Executa a consulta com os filtros
    cursor.execute(query, params)
    produtos = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(produtos)
# Obter um produto pelo ID
@produtos_bp.route('/produtos/<int:id>', methods=['GET'])
def get_produto(id):
    connection = connect_to_database()
    if connection is None:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM produtos WHERE id = %s"
    cursor.execute(query, (id,))
    produto = cursor.fetchone()
    cursor.close()
    connection.close()

    if produto is None:
        return jsonify({'error': 'Produto não encontrado'}), 404

    return jsonify(produto)

# Criar um novo produto
@produtos_bp.route('/produtos', methods=['POST'])
def create_produto():
    data = request.json
    connection = connect_to_database()
    if connection is None:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    cursor = connection.cursor()
    query = """
        INSERT INTO produtos (categoria, cor, qntd, nome_produto, preco, imagem, descricao, autor, ano_lancamento, genero, marca)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['nome_produto'],data['cor'], data['quantidade'], data['nome_produto'],
        data['preco'], data['imagem'], data.get('descricao'),
        data.get('autor'), data.get('ano_lancamento'),
        data.get('genero'), data.get('marca')
    )
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Produto criado com sucesso!'}), 201

# Atualizar um produto
@produtos_bp.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    data = request.json
    connection = connect_to_database()
    if connection is None:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    cursor = connection.cursor()
    query = """
        UPDATE produtos
        SET nome = %s, cor = %s, quantidade = %s, preco = %s,
            descricao = %s,imagem = %s, 
        WHERE id = %s
    """
    values = (
        data['nome'], data['cor'], data['quantidade'],
        data['preco'],data.get('descricao'),data['imagem'], id
    )
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Produto atualizado com sucesso!'})

# Deletar um produto
@produtos_bp.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    connection = connect_to_database()
    if connection is None:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    cursor = connection.cursor()
    query = "DELETE FROM produtos WHERE id = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Produto deletado com sucesso!'})

