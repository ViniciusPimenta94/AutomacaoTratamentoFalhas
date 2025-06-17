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
