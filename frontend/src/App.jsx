import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

const LIMITE_ARQUIVO_MB = 50 * 1024 * 1024;

function App() {
  const [arquivo, setArquivo] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [erro, setErro] = useState("");

  async function processarArquivo(evento) {
    evento.preventDefault();

    if (!arquivo) {
      setErro("Selecione um arquivo PDF.");
      return;
    }

    const formulario = new FormData();
    formulario.append("arquivo", arquivo);

    setCarregando(true);
    setResultado(null);
    setErro("");

    try {
      const resposta = await fetch(`${API_URL}/processar`, {
        method: "POST",
        body: formulario,
      });

      const dados = await resposta.json();

      if (!resposta.ok) {
        throw new Error(dados.erro || "Não foi possível processar o PDF.");
      }

      setResultado(dados);
    } catch (erroRecebido) {
      setErro(erroRecebido.message);
    } finally {
      setCarregando(false);
    }
  }

  function selecionarArquivo(evento) {
    const arquivoSelecionado = evento.target.files[0];
    if (arquivoSelecionado && arquivoSelecionado.size > LIMITE_ARQUIVO) {
  setArquivo(null);
  setResultado(null);
  setErro("O arquivo ultrapassa o limite de 50 MB.");
  evento.target.value = "";
  return;
}

    setArquivo(arquivoSelecionado || null);
    setResultado(null);
    setErro("");
  }

  return (
    <main className="pagina">
      <section className="painel">
        <header>
          <span className="etiqueta">Automação de PDFs</span>
          <h1>Processador de Etiquetas</h1>
          <p>
            Envie o PDF com três etiquetas por página e receba o documento
            separado, pronto para impressão.
          </p>
        </header>

        <form onSubmit={processarArquivo}>
          <label className="area-upload">
            <span>Selecione o PDF das etiquetas</span>

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={selecionarArquivo}
            />

            <strong>
              {arquivo ? arquivo.name : "Nenhum arquivo selecionado"}
            </strong>
          </label>

          <button type="submit" disabled={carregando}>
            {carregando ? "Processando..." : "Processar etiquetas"}
          </button>
        </form>

        {erro && <div className="mensagem erro">{erro}</div>}

        {resultado && (
          <div className="mensagem sucesso">
            <h2>PDF processado com sucesso!</h2>
            <p>{resultado.quantidade} etiquetas foram separadas.</p>

            <a href={resultado.download_url}>
              Baixar PDF processado
            </a>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;