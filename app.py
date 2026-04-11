from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from crud import *




app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("interface.html")

@app.route("/adicionar", methods=["POST"])
def adicionar():
    dados = request.get_json()
    x = dados["largurax"]
    y = dados["larguray"]
    esp = dados["espessura"]
    mat = dados["material"]
    add_chapa(x, y, esp, mat)
    return {"mensagem": "MINHAS BATATA PIAZADA VASCO VIROU !!!"}




@app.route("/listar", methods=["GET"])
def listar():
    chapas = listar_chapas()
    resultado = []
    for chapa in chapas:
        resultado.append({
            "id": chapa[0],
            "largurax": chapa[1],
            "larguray": chapa[2],
            "espessura": chapa[3],
            "material": chapa[4]
        })
    return resultado




@app.route("/deletar/<int:id>", methods=["DELETE"])
def deletar(id):
    deletar_chapa(id)
    return {"mensagem": "deletado"}




@app.route("/atualizar/<int:id>", methods=["PUT"])
def atualizar(id):
    print("chegou")
    dados = request.json
    atualizar_chapa(
        id,
        dados["largurax"],
        dados["larguray"],
        dados["espessura"],
        dados["material"],
    )
    return jsonify({"mensagem": "atualizado"})



if __name__ == "__main__":
    app.run(debug=True)