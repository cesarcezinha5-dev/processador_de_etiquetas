from flask import Flask, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
from processador_etiquetas import processar_etiquetas


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_FRONTEND = PASTA_PROJETO / "frontend" / "dist"
PASTA_UPLOADS = PASTA_PROJETO / "uploads"

PASTA_UPLOADS.mkdir(exist_ok=True)


app = Flask(
    __name__,
    static_folder=str(PASTA_FRONTEND / "assets"),
    static_url_path="/assets"
)

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


ORIGENS_PERMITIDAS = {
    "http://localhost:5173",
    "http://127.0.0.1:5173"
}


@app.errorhandler(413)
def arquivo_grande_demais(erro):
    return {"erro": "O arquivo enviado é muito grande."}, 413


@app.after_request
def adicionar_cors(resposta):
    origem = request.headers.get("Origin")

    if origem in ORIGENS_PERMITIDAS:
        resposta.headers["Access-Control-Allow-Origin"] = origem
        resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resposta.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    return resposta


@app.route("/")
def abrir_interface():
    return send_from_directory(
        PASTA_FRONTEND,
        "index.html"
    )


@app.route("/favicon.svg")
def abrir_favicon():
    return send_from_directory(
        PASTA_FRONTEND,
        "favicon.svg",
        mimetype="image/svg+xml"
    )


@app.route("/favicon.ico")
def abrir_favicon_ico():
    return send_from_directory(
        PASTA_FRONTEND,
        "favicon.svg",
        mimetype="image/svg+xml"
    )

    
@app.route("/status")
def verificar_status():
    return {
        "status": "online",
        "mensagem": "Sistema de etiquetas funcionando"
    }


@app.route("/processar", methods=["POST"])
def receber_pdf():
    if "arquivo" not in request.files:
        return {"erro": "Nenhum arquivo enviado."}, 400

    arquivo = request.files["arquivo"]

    if arquivo.filename == "":
        return {"erro": "Nenhum arquivo selecionado."}, 400

    if not arquivo.filename.lower().endswith(".pdf"):
        return {"erro": "O arquivo enviado não é um PDF válido."}, 400

    nome_seguro = secure_filename(arquivo.filename)

    if nome_seguro == "":
        return {"erro": "Nome de arquivo inválido."}, 400

    caminho_entrada = PASTA_UPLOADS / nome_seguro
    arquivo.save(caminho_entrada)

    try:
        resultado = processar_etiquetas(caminho_entrada)
        nome_resultado = Path(resultado["caminho"]).name

    except FileNotFoundError as erro:
        return {"erro": str(erro)}, 404

    except ValueError as erro:
        return {"erro": str(erro)}, 400

    except Exception as erro:
        app.logger.exception(
            "Erro inesperado ao processar o arquivo: %s",
            erro
        )

        return {
            "erro": "Ocorreu um erro ao processar o arquivo."
        }, 500

    finally:
        try:
            caminho_entrada.unlink(missing_ok=True)
        except OSError as erro:
            app.logger.warning(
                "Erro ao remover arquivo temporário: %s",
                erro
            )

    return {
        "quantidade": resultado["quantidade"],
        "download_url": url_for(
            "baixar_pdf",
            nome_arquivo=nome_resultado,
            _external=True
        )
    }, 200


@app.route("/downloads/<path:nome_arquivo>")
def baixar_pdf(nome_arquivo):
    return send_from_directory(
        PASTA_UPLOADS,
        nome_arquivo,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)