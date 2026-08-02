from processador_etiquetas import processar_etiquetas


if __name__ == "__main__":
    try:
        resultado = processar_etiquetas("etiquetas.pdf")
    except FileNotFoundError as erro:
        print(f"Erro: {erro}")
    except ValueError as erro:
        print(f"Erro: {erro}")
    else:
        print(f"{resultado['quantidade']} etiquetas foram separadas!\nO PDF já está pronto para impressão!")
        print(f"O PDF processado foi salvo em: {resultado['caminho']}")