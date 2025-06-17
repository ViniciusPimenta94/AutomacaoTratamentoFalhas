# Automação de Tratamento de Falhas

Este projeto tem como objetivo automatizar o tratamento de falhas identificadas em transações de faturas extraídas do Elastic Search (Kibana), organizando os arquivos por tipo de erro, corrigindo registros e gerando relatórios estruturados em Excel.

## 📦 Estrutura do Projeto

- `automacao_falhas.py`: Script principal que coordena a leitura dos dados, aplicação de expressões regulares, categorização de erros e organização de arquivos ZIP.
- `resolucaofalhas.py`: Contém a classe `Automacao`, que realiza o processamento detalhado das falhas, descompactação de arquivos e aplicação de correções nos dados.
- `pattern.json`: Arquivo de configuração que mapeia expressões regulares para tipos de erro e pastas de destino.

## 🛠 Requisitos

- Python 3.x
- Bibliotecas:
  - `pandas`
  - `openpyxl`
  - `shutil`
  - `re`
  - `patoolib`
  - `json`
  - `os`

Instale os requisitos com:

```bash
pip install pandas openpyxl patool
```

## ▶️ Como Executar

- Exporte o CSV de falhas do Kibana para o local indicado no código (Downloads/Pesquisa Fatura NotOk.csv).

- Execute o script principal:

```bash
python automacao_falhas.py
```
Os arquivos serão organizados e o relatório Falhas.xlsx será gerado com os erros classificados.

## 🔍 Funcionalidades

- Classificação automática por erro com base em regex (pattern.json).

- Geração de relatório Excel com erros identificados.

- Correção automática de arquivos .zip com falhas.

- Registro de alterações em arquivos de observação (.txt).

- Backup diário dos arquivos de falha processados.

## 📂 Organização de Pastas

O script organiza os arquivos em subpastas como:

- `ID/`

- `Conta Aglutinada/`

- `NotaFiscal/`

- `Parser/`

- `GED/`

Essas pastas são determinadas a partir dos padrões definidos no pattern.json.
