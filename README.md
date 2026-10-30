# Relatório Automatizado de Controle Financeiro / Automated Financial Control Report

## EN

### Goal
Automate an administrative routine: merge several spreadsheets, validate the data and generate a ready-to-use report. All data is synthetic.

### Problem
Financial spreadsheets often arrive in different formats, with duplicates, empty values, invalid dates and unknown categories. Fixing this by hand is slow and error-prone.

### Solution
1. `generate_data.py` creates 4 synthetic spreadsheets (3 CSV, 1 Excel) with intentional errors.
2. `consolidate.py` merges them with Pandas, standardizes dates and separates duplicates.
3. `validate.py` checks negative amounts, invalid dates, unknown categories, missing values and duplicates, and saves the errors in `reports/validation_errors.csv`.
4. `report.py` builds a formatted Excel file (openpyxl) with monthly and category summaries, plus clean CSVs for a dashboard.

### Tools
Python, Pandas, openpyxl, Kaggle, GitHub, Looker Studio.

### How to run
Open the notebook in `notebooks/` on Kaggle and use "Run All". It clones the repository, installs the requirements and runs the 4 scripts in order. It works from scratch every time.

### Folder structure
- `src/`: scripts (`config.py`, `generate_data.py`, `consolidate.py`, `validate.py`, `report.py`)
- `notebooks/`: Kaggle notebook
- `data/`: small synthetic data only
- `reports/`: Excel report and CSV outputs

### Results
- 4 spreadsheets consolidated into 160 valid rows (12 duplicates removed).
- 58 inconsistencies detected: 20 missing values, 12 duplicates, 10 negative amounts, 8 invalid dates, 8 unknown categories.
- Excel report generated automatically, with the same numbers on every run.

### Notes
- The "Total" row in the Excel file may appear empty outside Excel, because the totals are formulas. The CSV summaries have no Total row.
- Error details are in `reports/validation_errors.csv`.

### Learnings
- Validating data before summarizing avoids wrong totals.
- A notebook that runs from scratch is easier to trust and to review.
- Sharing settings (categories) in one file avoids inconsistencies between scripts.

---

## PT

### Objetivo
Automatizar uma rotina administrativa: consolidar várias planilhas, validar os dados e gerar um relatório pronto. Todos os dados são sintéticos.

### Problema
Planilhas financeiras chegam em formatos diferentes, com duplicados, valores vazios, datas inválidas e categorias inexistentes. Corrigir isso à mão é lento e propenso a erro.

### Solução
1. `generate_data.py` cria 4 planilhas sintéticas (3 CSV e 1 Excel) com erros de propósito.
2. `consolidate.py` junta tudo com Pandas, padroniza as datas e separa os duplicados.
3. `validate.py` verifica valor negativo, data inválida, categoria inexistente, valor vazio e duplicado, e grava os erros em `reports/validation_errors.csv`.
4. `report.py` gera um Excel formatado (openpyxl) com resumo por mês e por categoria, e CSVs limpos para dashboard.

### Ferramentas
Python, Pandas, openpyxl, Kaggle, GitHub, Looker Studio.

### Como executar
Abra o notebook em `notebooks/` no Kaggle e use "Run All". Ele clona o repositório, instala as dependências e roda os 4 scripts em ordem. Funciona do zero toda vez.

### Estrutura de pastas
- `src/`: scripts (`config.py`, `generate_data.py`, `consolidate.py`, `validate.py`, `report.py`)
- `notebooks/`: notebook do Kaggle
- `data/`: apenas dados sintéticos pequenos
- `reports/`: relatório Excel e arquivos CSV

### Resultados
- 4 planilhas consolidadas em 160 linhas válidas (12 duplicados removidos).
- 58 inconsistências detectadas: 20 valores vazios, 12 duplicados, 10 valores negativos, 8 datas inválidas, 8 categorias inexistentes.
- Relatório em Excel gerado automaticamente, com os mesmos números a cada execução.

### Observações
- A linha "Total" do Excel pode aparecer vazia fora do Excel, pois os totais são fórmulas. Os CSVs de resumo não têm linha Total.
- O detalhe dos erros está em `reports/validation_errors.csv`.

### Aprendizados
- Validar os dados antes de resumir evita totais errados.
- Um notebook que roda do zero é mais confiável e fácil de revisar.
- Centralizar configurações (categorias) em um arquivo evita inconsistência entre scripts.
