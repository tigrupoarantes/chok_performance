console.log("dashboard.js carregou");

async function carregarDados() {
    const dataInicio = document.getElementById("data_inicio").value;
    const dataFim = document.getElementById("data_fim").value;

    let url = "/api/vendas";

    if (dataInicio && dataFim) {
        url += `?data_inicio=${dataInicio}&data_fim=${dataFim}`;
    }

    const response = await fetch(url);
    const dados = await response.json();

    console.log("Dados recebidos:", dados);

    const tbody = document.getElementById("tabela-vendas");
    tbody.innerHTML = "";

    dados.forEach(linha => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${linha.nu_ped}</td>
            <td>${linha.dt_ped}</td>
            <td>${linha.vendedor}</td>
            <td>${linha.cliente}</td>
            <td>${linha.vl_venda}</td>
        `;

        tbody.appendChild(tr);
    });
}

// carrega ao abrir
carregarDados();