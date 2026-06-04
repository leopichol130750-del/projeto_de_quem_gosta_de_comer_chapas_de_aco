import psycopg2
from bcrypt import hashpw, gensalt, checkpw
from dotenv import load_dotenv
import os
load_dotenv()

def conectar():

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

def criar_tabela():
    conexao = conectar() 
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chapas (
            id SERIAL PRIMARY KEY,
            largurax INT,
            larguray INT,
            espessura NUMERIC(5,2),
            material TEXT
        )                
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            login VARCHAR(50) UNIQUE NOT NULL,
            senha TEXT NOT NULL
            )
        """)
    conexao.commit()
    conexao.close()


def add_chapa(x, y, espessura, material):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO chapas (largurax, larguray, espessura, material)
        VALUES (%s, %s, %s, %s)
        """, (x, y, espessura, material))
    conexao.commit()
    conexao.close()

def listar_chapas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM chapas")
    chapas = cursor.fetchall()
    conexao.close()
    return chapas

def deletar_chapa(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM chapas WHERE id = %s", (id,))
    conexao.commit()
    conexao.close()

def atualizar_chapa(id, largurax, larguray,espessura, material):
    conexao = conectar()
    cursor  = conexao.cursor()
    cursor.execute("""
        UPDATE chapas
        SET largurax = %s,
            larguray = %s,
            espessura = %s,
            material = %s
        WHERE id = %s          
        """,(largurax, larguray, espessura, material, id))
    conexao.commit()
    conexao.close()

def cadastro(senha):
    conexao = conectar()
    cursor = conexao.cursor()
    hash_senha = hashpw(senha.encode(), gensalt()).decode()
    cursor.execute(
        "INSERT INTO usuarios (login, senha) VALUES (%s, %s)",
        ("COLOCAR_NOME_DE_USUARIO_AQUI", hash_senha)
        )
    conexao.commit()
    cursor.close()

def buscar_usuario(login):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, login, senha FROM usuarios WHERE login = %s",
        (login,)
    )
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()
    return usuario


def autenticar_usuario(login, senha):
    usuario = buscar_usuario(login)

    if usuario is None:
        return None
    
    elif checkpw(
        senha.encode(),
        usuario[2].encode()
    ):
        return usuario
    
    return None
