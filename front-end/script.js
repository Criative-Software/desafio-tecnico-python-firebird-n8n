function buscarDados() {
  let mes = document.getElementById("mes").value;
  let ano = document.getElementById("ano").value;

  fetch(`http://127.0.0.1:5000/buscar?mes=${mes}&ano=${ano}`)
    .then((response) => response.json())
    .then((data) => {
      let tabela = document.getElementById("dadosTabela");
      tabela.innerHTML = ""; // Limpa os dados anteriores

      if (data.length === 0) {
        tabela.innerHTML =
          "<tr><td colspan='3'>Nenhum dado encontrado</td></tr>";
      } else {
        data.forEach((item) => {
          let linha = `<tr><td>${item.ano}</td><td>${item.mes}</td><td>${item.total}</td></tr>`;
          tabela.innerHTML += linha;
        });
      }
    })
    .catch((error) => console.error("Erro ao buscar dados:", error));
}

function buscarInsights() {
  fetch("http://127.0.0.1:5000/gerar_insights")
    .then((response) => response.json())
    .then((data) => {
      let insightsDiv = document.getElementById("insights");
      insightsDiv.innerHTML = "";

      if (data.insights) {
        insightsDiv.innerHTML = `
      <div class="insights-text-container">
        <h2>Gemini 2.0 avaliando suas métricas:</h2>
        <p>${data.insights.replace(/\n/g, "<br>")}</p>
      </div>`;
      } else {
        insightsDiv.innerHTML = `
      <div class="insights-text-container">
        <p>Erro ao obter insights.</p>
      </div>`;
      }
    })
    .catch((error) => console.error("Erro ao buscar insights:", error));
}

function exportarExcel() {
  fetch("http://127.0.0.1:5000/gerar_excel")
    .then((response) => response.blob()) // Converte a resposta para Blob (arquivo)
    .then((blob) => {
      const link = document.createElement("a"); // Cria um elemento <a> temporário
      link.href = URL.createObjectURL(blob); // Cria uma URL temporária para o arquivo
      link.download = "dados_completos.xlsx"; // Define o nome do arquivo
      document.body.appendChild(link);
      link.click(); // Simula o clique no link para iniciar o download
      document.body.removeChild(link); // Remove o link temporário após o download
    })
    .catch((error) => console.error("Erro ao gerar o Excel:", error));
}
