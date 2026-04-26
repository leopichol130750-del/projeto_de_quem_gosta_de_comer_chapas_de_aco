let modoEdicao = false;

function mostrar_aba(nome_aba) {
    document.getElementById("inputs_chapas").style.display = "none";
    document.getElementById("lista").style.display = "none";
    document.getElementById("zoom").style.display = "none";

    if (nome_aba === "adicionar") {
        document.getElementById("inputs_chapas").style.display = "block";
    }
    else if (nome_aba === "listar") {
        document.getElementById("lista").style.display = "grid";
    }

    else if (nome_aba ==="zoom") {
        document.getElementById("zoom").style.display = "block";
    }
}
    

document.getElementById("BotaoAddChapa")
    .addEventListener("click", () => mostrar_aba("adicionar"));

document.getElementById("BotaoSalvar")
    .addEventListener("click", function () {
        if (modoEdicao) {
            salvar_edicao();
        } else {
            adicionar_chapa();
        }
    });

function adicionar_chapa() {
    let x = Number(document.getElementById("x").value);
    let y = Number(document.getElementById("y").value);
    let esp = Number(document.getElementById("esp").value);
    let mat = document.getElementById("mat").value;

    if (x < 0 || x > 3000 || y < 0 || y > 1210 || !esp || mat === "") {
        alert("Preecha os campos corretamente!");
    }
    else {
        fetch("http://127.0.0.1:5000/adicionar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                largurax: x,
                larguray: y,
                espessura: esp,
                material: mat
            })
        })
            .then(res => res.json())
            .then(data => {
                console.log("Salvo no Banco de dados", data)
            })
        document.getElementById("x").value = "";
        document.getElementById("y").value = "";
        document.getElementById("esp").value = "";
        document.getElementById("mat").value = "";
    }
}


document.getElementById("BotaoListarChapas")
    .addEventListener("click", () => {
        mostrar_aba("listar");
        listar_chapas();
    });


function listar_chapas(){
    fetch("http://127.0.0.1:5000/listar")
        .then(res => res.json())
        .then(dados => {
            mostrarTabela(dados);
        });
}

function deletar_chapa(id) {
    fetch(`http://127.0.0.1:5000/deletar/${id}`, {
        method: "DELETE"
    })
        .then(() => {
            listar_chapas();
        });
}



let idEditada;
function salvar_edicao() {
    console.log("ID", idEditada)
    fetch(`http://127.0.0.1:5000/atualizar/${idEditada}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            largurax: Number(document.getElementById("edit_x").value),
            larguray: Number(document.getElementById("edit_y").value),
            espessura: Number(document.getElementById("edit_esp").value),
            material: document.getElementById("edit_mat").value
        })
    })
        .then(res => res.json())
        .then(() => {
            listar_chapas();
        });
}


document.getElementById("salvarEdicao")
    .addEventListener("click", () => {
        salvar_edicao();
    });

function mostrarTabela(chapas) {
    const lista = document.getElementById("lista");
    lista.innerHTML = "";
    chapas.forEach(tam_chapa => {
        
        let maior = Math.max(tam_chapa.largurax, tam_chapa.larguray);
        let proporcao = 200 / maior;
        let largura = tam_chapa.largurax * proporcao;
        let altura = tam_chapa.larguray * proporcao;
        let card = document.createElement("div");
            card.classList.add("card")

            let acoes = document.createElement("div");
                acoes.classList.add("acoes");
                acoes.innerHTML = `
                    <button class="editar">
                        <i class="fa-solid fa-pen"></i>
                    </button>

                    <button class="excluir">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                `;
            const BotaoEditar = acoes.querySelector(".editar");
                BotaoEditar.addEventListener("click", () => {
                    abrirZoom(tam_chapa);
                    desenharPreviewEdicao(tam_chapa.largurax, tam_chapa.larguray);
                    
                });

            const BotaoExcluir = acoes.querySelector(".excluir");
            BotaoExcluir.dataset.id = tam_chapa.id;
            BotaoExcluir.innerHTML = `
                <div id="telaExclusao" class="telaExclusao">
                    <div class="telaExclusaoConteudo>
                        <p> Tem certeza que deseja excluir essa chapa?</p>
                        <button id="confirmarExclusao">Confirmar</button>
                        <button id="cancelarExclusao">Cancelar</button>
                `
            document.getElementById("confirmarExclusao")
                .addEventListener("click", function() {
                const id = this.dataset.id;
                deletar_chapa(id);
            });

            let desenho = document.createElement("div");
                desenho.classList.add("desenho");
                desenho.style.width = largura + "px";
                desenho.style.height = altura + "px";

            let areaDesenho = document.createElement("div");
                areaDesenho.classList.add("areaDesenho");
    
            let desc= document.createElement("div");
                desc.classList.add("desc");
                desc.innerHTML = `
                    <div class="info">
                        <span>X: ${tam_chapa.largurax}</span>
                        <span>Espessura: ${tam_chapa.espessura}</span>
                        <span>Y: ${tam_chapa.larguray}</span>                        
                        <span>Material: ${tam_chapa.material}</span>
                    </div>
                `;
        areaDesenho.appendChild(desenho);
        card.appendChild(areaDesenho);
        card.appendChild(desc);
        card.appendChild(acoes);
        lista.appendChild(card);
        });
}

function abrirZoom (chapa){
    document.getElementById("zoom").style.display = "flex";

    document.getElementById("edit_x").value = chapa.largurax
    document.getElementById("edit_y").value = chapa.larguray
    document.getElementById("edit_esp").value = chapa.espessura
    document.getElementById("edit_mat").value = chapa.material
    
    idEditada = chapa.id;
}

function desenharPreviewEdicao(x,y) {
    const preview = document.getElementById("previewEdicao");
    console.log(preview);
    preview.innerHTML = "";

    let maior = Math.max(x,y);
    let proporcao = 400 / maior;
    let largura = x * proporcao;
    let altura = y * proporcao;

    const pecaEdit = document.createElement("div");
        pecaEdit.classList.add("pecaEdicao")
        pecaEdit.style.width = largura + "px";
        pecaEdit.style.height = altura + "px";
        preview.appendChild(pecaEdit)
    
}

function atualizarPreviewEdicao() {
    const x = Number(document.getElementById("edit_x").value);
    const y = Number(document.getElementById("edit_y").value);

    if (x > 0 && y > 0) {
        desenharPreviewEdicao(x,y);
    }
}

document.getElementById("edit_x").addEventListener("input", atualizarPreviewEdicao);
document.getElementById("edit_y").addEventListener("input", atualizarPreviewEdicao)
