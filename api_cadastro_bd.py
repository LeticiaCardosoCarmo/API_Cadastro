#Objetivo
    #Criar uma API que possibilita a consulta, criação, edição e exclusão de pessoas em um banco de dados  .
#URL base
    #localhost
#Endpoints
    #Consultar -> localhost/cadastro (GET)
    #Consultar por id -> localhost/cadastro/id (GET)
    #Criar -> localhost/cadastro/id (POST)
    #Editar -> localhost/cadastro/id (PUT)
    #Excluir -> localhost/cadastro/id (DELETE)
#Quais recursos
    #cadastro

import mysql.connector
from flask import Flask, jsonify, request
from datetime import datetime

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'cadastro_bd',
)

app = Flask(__name__) #__name__ faz com que o flask assuma o nome do nosso arquivo.
app.config['JSON_SORT_KEYS'] = False #para não autorizar o json colocar as infos em ordem alfabética

#Consultar -> localhost/cadastro (GET)
@app.route('/cadastro', methods=['GET'])
def consultar_cadastro():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM dados')
    todos_cadastros = cursor.fetchall()

    infos = []
    for pessoa in todos_cadastros:
        infos.append({
            'id' : pessoa[0],
            'nome' : pessoa[1],
            'sexo' : pessoa[2],
            'data_nascimento' : pessoa[3],
            'telefone' : pessoa[4],
            'email' : pessoa[5],
        })
    
    return jsonify(
        msg = 'Lista de cadastros:',
        dados = infos)

#Consultar por id -> localhost/cadastro/id (GET)
@app.route('/cadastro/<int:id>', methods=['GET'])
def consultar_cadastro_id(id):
    cursor =  db.cursor()
    sql = f"SELECT * FROM dados WHERE id = '{id}'"
    cursor.execute(sql)
    cadastro = cursor.fetchall()

    infos = []
    for dado in cadastro:
        infos.append({
            'id' : dado[0],
            'nome' : dado[1],
            'sexo' : dado[2],
            'data_nascimento' : dado[3],
            'telefone' : dado[4],
            'email' : dado[5],
        })
    return jsonify(
        msg = 'Cadastro: ',
        dados = infos)
        
#Criar -> localhost/cadastro/id (POST)
@app.route('/cadastro/incluir', methods=['POST'])
def incluir_cadastro():
    novo_cadastro = request.get_json()
    cursor = db.cursor()
    date_object = datetime.strptime(novo_cadastro['data_nascimento'], '%Y-%m-%d').date()
    sql = f"INSERT INTO dados (nome, sexo, data_nascimento, telefone, email) VALUES ('{novo_cadastro['nome']}', '{novo_cadastro['sexo']}', '{date_object}' , {novo_cadastro['telefone']}, '{novo_cadastro['email']}')"
    cursor.execute(sql)
    db.commit()

    return jsonify(
        msg = 'Cadastro feito com sucesso.',
        dados = novo_cadastro)

""" #Editar -> localhost/cadastro/id (PUT)
@app.route('/cadastro/editar/<int:id>', methods=['PUT'])
def editar_cadastro_id(id):
    var_editar = request.get_json()
    dado_editar = request.get_json()
    cursor = db.cursor()
    sql = f"UPDATE dados SET {var_editar} = '{dado_editar}'"
    cursor.execute(sql)
    cadastro_alterado = request.get_json()
    for indice, pessoa in enumerate(cadastro):
        if pessoa.get('id') == id:
            cadastro[indice].update(cadastro_alterado)
    return jsonify(msg = 'Cadastro editado com sucesso') """
        
#Excluir -> localhost/cadastro/id (DELETE)
@app.route('/cadastro/excluir/<int:id>', methods=['DELETE'])
def excluir_cadastro_id(id):
    cursor =  db.cursor()
    sql = f"DELETE FROM dados WHERE id = '{id}'"
    cursor.execute(sql)
    return jsonify(msg = 'Cadastro excluído com sucesso: ')                             

app.run()
        
