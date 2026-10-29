"""Generate synthetic finance spreadsheets with intentional errors.
Gera planilhas financeiras sintéticas com erros de propósito."""

from pathlib import Path
# EN: Allowed categories live in config.py (single source of truth).
# PT: As categorias permitidas ficam no config.py (fonte única).
from config import CATEGORIES
import numpy as np
import pandas as pd

# EN: Fixed seed so every run creates the same data.
# PT: Semente fixa: toda execução gera os mesmos dados.
SEED = 42
RAW_DIR = Path("data/raw")


def make_base(n_rows: int, rng: np.random.Generator) -> pd.DataFrame:
    """Create a clean synthetic table. / Cria uma tabela limpa sintética."""
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    return pd.DataFrame({
        "id": np.arange(1, n_rows + 1),
        "date": rng.choice(dates, n_rows),
        "category": rng.choice(CATEGORIES, n_rows),
        "description": [f"Lançamento {i}" for i in range(1, n_rows + 1)],
        "amount": rng.uniform(10, 800, n_rows).round(2),
    })


def add_errors(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Inject duplicates, blanks, bad dates, negatives and bad categories.
    Injeta duplicados, vazios, datas ruins, negativos e categorias inválidas."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # EN: Mixed date formats / PT: Formatos de data diferentes
    idx = rng.choice(df.index, 4, replace=False)
    df.loc[idx[:2], "date"] = pd.to_datetime(df.loc[idx[:2], "date"]).dt.strftime("%d/%m/%Y")
    df.loc[idx[2], "date"] = "31/02/2025"  # invalid date / data inválida
    df.loc[idx[3], "date"] = "sem data"

    # EN: Blank values / PT: Valores vazios
    df.loc[rng.choice(df.index, 3, replace=False), "amount"] = np.nan
    df.loc[rng.choice(df.index, 2, replace=False), "category"] = np.nan

    # EN: Negative amounts / PT: Valores negativos
    df.loc[rng.choice(df.index, 3, replace=False), "amount"] *= -1

    # EN: Unknown category / PT: Categoria inexistente
    df.loc[rng.choice(df.index, 2, replace=False), "category"] = "Viagem"

    # EN: Duplicated rows / PT: Linhas duplicadas
    return pd.concat([df, df.sample(3, random_state=SEED)], ignore_index=True)


def main() -> None:
    """Write 4 spreadsheets to data/raw. / Grava 4 planilhas em data/raw."""
    rng = np.random.default_rng(SEED)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):
        df = add_errors(make_base(40, rng), rng)
        if i < 4:
            df.to_csv(RAW_DIR / f"financeiro_{i}.csv", index=False)
        else:
            df.to_excel(RAW_DIR / "financeiro_4.xlsx", index=False)
    print(f"Planilhas geradas em {RAW_DIR}")


if __name__ == "__main__":
    main()
