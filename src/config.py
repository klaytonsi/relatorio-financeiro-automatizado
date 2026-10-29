"""Shared settings used by more than one script.

Configurações compartilhadas por mais de um script.
"""

# EN: Single source of truth for the allowed categories.
#     generate_data.py and validate.py both import this list.
# PT: Fonte única das categorias permitidas.
#     generate_data.py e validate.py importam esta lista.
CATEGORIES = ("Alimentação", "Transporte", "Moradia", "Lazer", "Saúde")
