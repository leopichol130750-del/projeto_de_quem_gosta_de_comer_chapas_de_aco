import psycopg2

def conectar():
    return psycopg2.connect(
        "postgresql://neondb_owner:npg_dBWfMT9S3Hmb@ep-wispy-heart-acrdf0q1-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )

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


print(listar_chapas())