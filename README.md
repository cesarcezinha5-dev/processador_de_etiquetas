# Processador de Etiquetas em PDF

Sistema desenvolvido para automatizar a separação de etiquetas logísticas em arquivos PDF.

O sistema recebe um PDF com três etiquetas posicionadas lado a lado em cada página e gera automaticamente um novo documento com uma etiqueta por página, pronto para download e impressão.

## Problema

Em operações com muitos volumes, separar manualmente cada etiqueta pode consumir bastante tempo e aumentar a possibilidade de erros.

Um documento com 1.000 volumes, por exemplo, exigiria centenas de recortes manuais. A proposta deste projeto é automatizar esse processo em poucos segundos.

## Solução

O usuário seleciona o PDF original pela interface. O sistema:

1. Valida o arquivo enviado.
2. Divide cada página em três partes iguais.
3. Recorta as etiquetas da esquerda para a direita.
4. Gera um novo PDF com uma etiqueta por página.
5. Informa quantas etiquetas foram separadas.
6. Disponibiliza o resultado para download.

## Tecnologias

### Back-end

* Python
* Flask
* PyMuPDF
* Pathlib

### Front-end

* React
* Vite
* HTML
* CSS
* JavaScript

## Fluxo da aplicação

```text
React envia o PDF
        ↓
Flask recebe e valida o arquivo
        ↓
PyMuPDF separa as etiquetas
        ↓
Flask gera o link do resultado
        ↓
React disponibiliza o download
```

## Estrutura do projeto

```text
processador_de_etiquetas/
├── app.py
├── main.py
├── processador_etiquetas.py
├── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── uploads/
```

A pasta `uploads` e os arquivos PDF são ignorados pelo Git para evitar o envio de documentos utilizados durante o processamento.

## Como executar

### Requisitos

* Python 3
* Node.js
* npm

### Back-end

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie a API:

```bash
python app.py
```

O Flask será iniciado em:

```text
http://127.0.0.1:5000
```

### Front-end

Entre na pasta do front-end:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie o React:

```bash
npm run dev
```

A interface estará disponível em:

```text
http://localhost:5173
```

## Funcionalidades atuais

* Upload de arquivos PDF.
* Validação de nome e extensão.
* Validação de PDF vazio, inválido ou corrompido.
* Separação automática de três etiquetas por página.
* Geração de uma etiqueta por página.
* Contagem das etiquetas processadas.
* Mensagens de sucesso e erro.
* Download do PDF final.
* Interface responsiva.
* Comunicação entre React e Flask.

## Segurança e privacidade

O repositório não contém etiquetas reais, dados de clientes ou documentos internos de empresas.

Os arquivos utilizados em testes e demonstrações devem ser totalmente fictícios.

## Status

Versão funcional em desenvolvimento.

O núcleo de processamento, a API e a interface React já estão funcionando. Uma futura versão poderá ser empacotada como aplicativo desktop com janela própria.

## Próximas melhorias

* Testes com diferentes modelos de PDF.
* Limite de tamanho para uploads.
* Limpeza automática de arquivos temporários.
* Empacotamento como aplicativo desktop.
* Geração de instalador para Windows.

## Autor

Desenvolvido por [César Augusto](https://github.com/cesarcezinha5-dev) como projeto de estudo e automação de um problema real.
