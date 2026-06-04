from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import crud
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    if not session.get("logado"):
        return redirect("/login")
    return render_template("interface.html")

@app.route("/adicionar", methods=["POST"])
def adicionar():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"success":False, "erro": "sem dados"}), 400
        
        campos_requeridos = ["largurax", "larguray", "espessura", "material"]
        for campo in campos_requeridos:
            if campo not in dados:
                return jsonify({"success": False, "erro": f"faltando {campo}"}), 400
        x = int(dados["largurax"])
        y = int(dados["larguray"])
        esp = float(dados["espessura"])
        mat = dados["material"].strip()

        crud.add_chapa(x, y, esp, mat)
        return jsonify({"success": True, "mensagem": "adicionado"}), 201
    
    except Exception as e:
        return jsonify({"success": False, "erro": str(e)}), 500




@app.route("/listar", methods=["GET"])
def listar():
    try:
        chapas = crud.listar_chapas()
        resultado = []
        for chapa in chapas:
            resultado.append({
                "id": chapa[0],
                "largurax": chapa[1],
                "larguray": chapa[2],
                "espessura": chapa[3],
                "material": chapa[4]
            })
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"success": False, "erro": str(e)}), 500




@app.route("/deletar/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        crud.deletar_chapa(id)
        return jsonify({"success": True, "mensagem": "deletado"}), 200
    
    except Exception as e:
        return jsonify({"success": False, "erro": str(e)}), 500




@app.route("/atualizar/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"success": False, "erro": "sem dados"}), 400
        
        campos_requeridos = ["largurax", "larguray", "espessura", "material"]

        for campo in campos_requeridos:
            if campo not in dados:
                return jsonify({"success": False, "erro": f"faltando {campo}"}), 400
            
        x = int(dados["largurax"])
        y = int(dados["larguray"])
        esp = float(dados["espessura"])
        mat = dados["material"].strip()
        crud.atualizar_chapa(id, x, y, esp, mat)
        return jsonify({"success": True, "mensagem": "atualizado"}), 200
    
    except Exception as e:
        return jsonify({"success": False, "erro": str(e)}), 500

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    login = request.form.get("usuario")
    senha = request.form.get("senha")

    usuario = crud.autenticar_usuario(login, senha)

    if usuario:
        session["logado"] = True
        return redirect("/")
    return "Usuário ou senha inválidos"

if __name__ == "__main__":
    crud.criar_tabela()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
