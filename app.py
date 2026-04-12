from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import crud




app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
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
        return jsonify({"mensagem": "adicionado"}), 201
    
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
        return jsonify({"mensagem": "deletado"}), 200
    
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
        return jsonify({"mensagem": "atualizado"}), 200
    
    except Exception as e:
        return jsonify({"success": False, "erro": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)