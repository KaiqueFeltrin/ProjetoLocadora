from flask import Flask, render_template, g, request, redirect, jsonify,flash,session, send_file
import sqlite3
import io

from flask_cors import CORS

lista = []

def recuperar_foto(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Foto FROM Catalogo WHERE ID = ?', (id,))
    imagem_blob = cursor.fetchone()
    return imagem_blob[0]

def ligar_banco():
    banco = g._database = sqlite3.connect('banco.db')
    return banco


app = Flask(__name__)
app.secret_key = '123'
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route('/')
def login():
    return render_template('Login.html', Titulo='Login - Locadora de Filmes')

@app.route('/home')
def home():
        return render_template('Home.html', Titulo='Locadora de Filmes')

@app.route('/cadastrarCatalogo')
def exibircatalogo():
    return render_template('CadCatalogo.html', Titulo='Exibir - Locadora de Filmes')

@app.route('/cadastrarLocacao')
def cadastrarlocacao():
    return render_template('CadLocacao.html', Titulo='Locação - Locadora de Filmes')

@app.route('/editarCliente')
def editarclientes():
    return render_template('EditarClientes.html', Titulo='Clientes - Locadora de Filmes')

@app.route('/cadastrarCliente')
def cadastrarclientes():
    return render_template('CadClientes.html', Titulo='Clientes - Locadora de Filmes')

@app.route('/sobrenos')
def sobrenos():
    return render_template('SobreNos.html', Titulo='Sobre Nós - Locadora de Filmes')

@app.route('/criarCatalogo', methods = ['GET', 'POST'])
def cadastrarCatalogo():
    nome = request.form['nome']
    dataDeLancamento = request.form['dataDeLancamento']
    diretor = request.form['diretor']
    categoria = request.form['categoria']
    banco = ligar_banco()
    cursor = banco.cursor()
    with open('static/Imagens/cinemaFixa.png', 'rb') as padrao:
            foto_blob = padrao.read()
    cursor.execute('INSERT INTO Catalogo'
                   '(NomeDoFilme, DataDeLancamento, Diretor, Categoria, Foto)'
                   'VALUES (?, ?, ?, ?, ?);',
                   (nome, dataDeLancamento, diretor, categoria, foto_blob ))
    banco.commit()
    return redirect('/catalogo')


@app.route('/excluirCatalogo/<id>', methods=['GET'])
def excluirCatalogo(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Catalogo WHERE ID = ?;', (id,))
    banco.commit()
    return redirect('/catalogo')

@app.route('/editarCatalogo/<id>', methods=['GET'])
def editarCatalogo(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Catalogo WHERE ID=?;', (id,))
    encontrado2 = cursor.fetchone()
    return render_template('EditarCatalogo.html', Catalogo=encontrado2, Titulo="Editar Catalogo")


@app.route('/catalogo')
def exibirCatalogo():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Catalogo')
    Catalogos = cursor.fetchall()  # retorna uma lista com tuplas
    return render_template('Catalogo.html', ListaCatalogo=Catalogos)

@app.route('/alterarCatalogo/<id>', methods = ['PUT', 'POST'])
def alterarCatalogo(id):
    nome = request.form['nome']
    dataDeLancamento = request.form['dataDeLancamento']
    diretor = request.form['diretor']
    categoria = request.form['categoria']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('UPDATE Catalogo SET NomeDoFilme=?, DataDeLancamento=?,'
                       'Diretor=?, Categoria=? WHERE ID=?;',

                       (nome, dataDeLancamento, diretor, categoria,id))
    banco.commit()
    return redirect('/catalogo')



@app.route('/criarLocacao', methods = ['GET', 'POST'])
def criarLocacao ():
    nomedofilme = request.form['nomedofilme']
    preco = request.form['preco']
    destinatario = request.form['destinatario']
    data = request.form['data']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('INSERT INTO Locacao'
                   '(NomeDoFilme , Preco,  NomeDoDestinario, DataDeLocacao)'
                   'VALUES (?, ?, ?, ?);', ( nomedofilme, preco, destinatario, data ))
    banco.commit()
    return redirect('/locacao')



@app.route('/excluirLocacao/<id>', methods=['GET'])
def excluirLocacao(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Locacao WHERE ID = ?;', (id,))
    banco.commit()
    return redirect('/locacao')

@app.route('/editarLocacao/<id>', methods=['GET'])
def editarLocacao(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Locacao WHERE ID=?;', (id,))
    encontrado = cursor.fetchone()
    return render_template('EditarLocacao.html', Locacao=encontrado, Titulo="Editar Estudante")

@app.route('/alterarLocacao/<id>', methods = ['PUT', 'POST'])
def alterarLocacao(id):
    preco = request.form['preco']
    nomedofilme = request.form['nomedofilme']
    destinatario = request.form['destinatario']
    data = request.form['data']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('UPDATE Locacao SET Preco=?, NomeDoFilme=?,'
                       'NomeDoDestinario=?, DataDeLocacao=? WHERE ID=?;',
                       (preco, nomedofilme, destinatario, data,id))
    banco.commit()
    return redirect('/locacao')

@app.route('/locacao')
def exibirLocacao():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Locacao')
    Locacao = cursor.fetchall()  # retorna uma lista com tuplas
    return render_template('Locacao.html', ListaLocacao=Locacao)

@app.route('/cadastrarCliente', methods = ['GET', 'POST'])
def cadastrarCliente ():
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('INSERT INTO Cliente'
                   '(NomeDoCliente, Cpf, Email, Telefone, Endereco)'
                   'VALUES (?, ?, ?, ?,? );',
                   (nome, cpf, email, telefone, endereco))
    banco.commit()
    return redirect('/clientes')


@app.route('/excluirCliente/<id>', methods=['GET'])
def excluirCliente(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Cliente WHERE id = ?;', (id,))
    banco.commit()
    return redirect('/clientes')

@app.route('/editarCliente/<id>', methods=['GET'])
def editarCliente(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Cliente WHERE ID=?;', (id,))
    encontrado = cursor.fetchone()
    return render_template('EditarClientes.html', Cliente = encontrado, Titulo="Editar Cliente")

@app.route('/alterarCliente/<id>', methods = ['PUT', 'POST'])
def alterarCliente(id):
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('UPDATE Cliente SET NomeDoCliente=?, Cpf=?,'
                       'Email=?, Telefone=?, Endereco = ? WHERE ID=?;',
                       (nome, cpf, email, telefone, endereco, id))
    banco.commit()
    return redirect('/clientes')

@app.route('/clientes')
def exibirCliente():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Cliente')
    Cliente = cursor.fetchall()  # retorna uma lista com tuplas
    return render_template('Clientes.html', ListaCliente = Cliente)


@app.route('/imagem/<id>')
def imagem(id):
    foto_blob = recuperar_foto(id)
    return send_file(
        io.BytesIO(foto_blob),
        mimetype = 'image/jpeg',
        download_name = f'imagem_{id}.jpg'
    )

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] == 'Bruno' and request.form['senha'] == '123':
        session['Usuario_logado'] = request.form['usuario']
        flash('Usuário Logado')
        return redirect('/home')
    else:
        flash('Usuário ou senha incorretos!')  # Mensagem de erro
        return redirect('/')


if __name__ == '__main__':
    app.run()


