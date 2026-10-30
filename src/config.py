"""Shared settings used by more than one script.

Configurações compartilhadas por mais de um script.
"""

# EN: Single source of truth for the allowed categories.
#     generate_data.py and validate.py both import this list.
# PT: Fonte única das categorias permitidas.
#     generate_data.py e validate.py importam esta lista.
CATEGORIES = ("Alimentação", "Transporte", "Moradia", "Lazer", "Saúde")
# EN: Column names shared by all scripts (single source of truth).
# PT: Nomes de colunas compartilhados por todos os scripts (fonte única).
DATE_COL = "date"
DATE_RAW_COL = "date_raw"
SOURCE_COL = "source_file"
ID_COL = "id"
CATEGORY_COL = "category"
AMOUNT_COL = "amount"
ERROR_TYPE_COL = "error_type"
