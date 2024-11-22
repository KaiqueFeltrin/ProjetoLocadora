import sqlite3
conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS Cliente('
    'ID INTEGER PRIMARY KEY,'
    'NomeDoCliente TEXT,'
    'Genero TEXT,'
    'Idade INTEGER)'
)