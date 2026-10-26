"""Consolidate raw spreadsheets into one table.
Consolida as planilhas brutas em uma única tabela."""

from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/processed/consolidated.csv")


def read_all(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Read every CSV/XLSX and tag the source file.
    Lê todos os CSV/XLSX e marca o arquivo de origem."""
    frames = []
    for path in sorted(raw_dir.iterdir()):
        if path.suffix == ".csv":
            df = pd.read_csv(path, dtype={"date": "string"})
        elif path.suffix == ".xlsx":
            df = pd.read_excel(path, dtype={"date": "string"})
        else:
            continue  # EN: ignore other files / PT: ignora outros arquivos
        df["source_file"] = path.name
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def parse_dates(dates: pd.Series) -> pd.Series:
    """Convert mixed date formats; invalid ones become NaT.
    Converte formatos de data diferentes; inválidas viram NaT."""
    # EN: Try ISO (YYYY-MM-DD) first, then DD/MM/YYYY for the rest.
    # PT: Tenta ISO (AAAA-MM-DD) primeiro, depois DD/MM/AAAA no resto.
    iso = pd.to_datetime(dates, format="%Y-%m-%d", errors="coerce")
    br = pd.to_datetime(dates, format="%d/%m/%Y", errors="coerce")
    return iso.fillna(br)


def consolidate(raw_dir: Path = RAW_DIR) -> tuple[pd.DataFrame, int]:
    """Return the unified table and how many duplicates were removed.
    Retorna a tabela unificada e quantos duplicados foram removidos."""
    df = read_all(raw_dir)
    # EN: Keep the original text to report invalid dates later.
    # PT: Guarda o texto original para reportar datas inválidas depois.
    df["date_raw"] = df["date"]
    df["date"] = parse_dates(df["date"])

    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    return df, before - len(df)


def main() -> None:
    """Run consolidation and save the result.
    Executa a consolidação e salva o resultado."""
    df, removed = consolidate()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"{len(df)} linhas salvas; {removed} duplicados removidos")


if __name__ == "__main__":
    main()
