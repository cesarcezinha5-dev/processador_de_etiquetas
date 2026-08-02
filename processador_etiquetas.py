import fitz
from pathlib import Path


def processar_etiquetas(caminho_entrada, caminho_saida=None):
    caminho_entrada = Path(caminho_entrada)
    if caminho_saida is None:
        caminho_saida = caminho_entrada.with_name(
            f"{caminho_entrada.stem}_processada.pdf"
        )
    if not caminho_entrada.exists():
        raise FileNotFoundError(f"O arquivo {caminho_entrada} não foi encontrado.")
    if caminho_entrada.suffix.lower() != ".pdf":
        raise ValueError(f"O arquivo {caminho_entrada} não é um PDF válido.")
    try:
        documento = fitz.open(caminho_entrada)
    except RuntimeError:
        raise ValueError("O arquivo não é um PDF válido.")
    novo_pdf = fitz.open()

    try:
        if documento.page_count == 0:
            raise ValueError("O PDF de entrada não contém páginas.")

        for indice_pagina in range(documento.page_count):
            pagina = documento[indice_pagina]

            altura_etiqueta = pagina.rect.height 
            largura_etiqueta = pagina.rect.width /3

            primeira_etiqueta = fitz.Rect(
                0,
                0,
                largura_etiqueta,
                altura_etiqueta
            )

            segunda_etiqueta = fitz.Rect(
                largura_etiqueta,
                0,
                largura_etiqueta * 2,
                altura_etiqueta 
            )

            terceira_etiqueta = fitz.Rect(
                largura_etiqueta * 2,
                0,
                largura_etiqueta * 3,
                altura_etiqueta
            )

            etiquetas = [
                primeira_etiqueta,
                segunda_etiqueta,
                terceira_etiqueta
            ]

            for etiqueta in etiquetas:
                nova_pagina = novo_pdf.new_page(
                    width=largura_etiqueta,
                    height=altura_etiqueta
                )

                nova_pagina.show_pdf_page(
                    nova_pagina.rect,
                    documento,
                    indice_pagina,
                    clip=etiqueta
                )

        quantidade_etiquetas = novo_pdf.page_count
        novo_pdf.save(caminho_saida)

    finally:
        novo_pdf.close()
        documento.close()

    return {
        "quantidade": quantidade_etiquetas,
        "caminho":str (caminho_saida)
    }


