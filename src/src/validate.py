"""Validate the consolidated table and save the errors in a separate report.

Valida a tabela consolidada e salva os erros em um relatório separado.
"""

import sys
from pathlib import Path

import pandas as pd

# EN: Column names come from consolidate.py (date, date_raw, source_file).
#     CATEGORY_COL and AMOUNT_COL must match generate_data.py.
# PT: Os nomes vêm do consolidate.py (date, date_raw, source_file).
#     CATEGORY_COL e AMOUNT_COL precisam bater com o generate_data.py.
DATE_COL = "date"
DATE_RAW_COL = "date_raw"
SOURCE_COL = "source_file"
CATEGORY_COL = "category"
AMOUNT_COL = "amount"
REQUIRED_COLS = [DATE_COL, DATE_RAW_COL, CATEGORY_COL, AMOUNT_COL]

# EN: Allowed categories, copied from generate_data.py (CATEGORIES list).
# PT: Categorias permitidas, copiadas do generate_data.py (lista CATEGORIES).
VALID_CATEGORIES = {"Alimentação", "Transporte", "Moradia", "Lazer", "Saúde"}

INPUT_FILE = Path("data/processed/consolidated.csv")
REPORT_FILE = Path("reports/validation_errors.csv")
ERROR_COLS = ["row", "source_file", "column", "error_type", "value"]


def _build_errors(
    df: pd.DataFrame, mask: pd.Series, column: str, error_type: str, value_col: str
) -> pd.DataFrame:
    """Build an error table for the rows selected by a mask.

    Monta a tabela de erros das linhas selecionadas por uma máscara.
    """
    # EN: Keep the row index and the source file to trace each error.
    # PT: Mantém o índice da linha e o arquivo de origem para rastrear cada erro.
    rows = df.loc[mask]
    source = rows[SOURCE_COL].astype(str) if SOURCE_COL in rows else ""
    return pd.DataFrame(
        {
            "row": rows.index,
            "source_file": source,
            "column": column,
            "error_type": error_type,
            "value": rows[value_col].astype(str).values,
        },
        columns=ERROR_COLS,
    )


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Find empty values in the required columns.

    Encontra valores vazios nas colunas obrigatórias.
    """
    # EN: For dates, "empty" means the original text was empty (date_raw).
    # PT: Para datas, "vazio" significa que o texto original era vazio (date_raw).
    columns = [DATE_RAW_COL, CATEGORY_COL, AMOUNT_COL]
    parts = [_build_errors(df, df[c].isna(), c, "missing_value", c) for c in columns]
    return pd.concat(parts, ignore_index=True)


def check_negative_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Find negative amounts.

    Encontra valores negativos.
    """
    # EN: errors="coerce" turns non-numeric text into NaN (NaN < 0 is False).
    # PT: errors="coerce" transforma texto não numérico em NaN (NaN < 0 é False).
    amounts = pd.to_numeric(df[AMOUNT_COL], errors="coerce")
    return _build_errors(df, amounts < 0, AMOUNT_COL, "negative_amount", AMOUNT_COL)


def check_invalid_date(df: pd.DataFrame) -> pd.DataFrame:
    """Find dates that were filled in but could not be parsed.

    Encontra datas preenchidas que não puderam ser interpretadas.
    """
    # EN: consolidate.py turns invalid dates into NaT but keeps the text in date_raw.
    # PT: O consolidate.py transforma datas inválidas em NaT e guarda o texto em date_raw.
    parsed = pd.to_datetime(df[DATE_COL], errors="coerce")
    mask = parsed.isna() & df[DATE_RAW_COL].notna()
    return _build_errors(df, mask, DATE_COL, "invalid_date", DATE_RAW_COL)


def check_unknown_category(df: pd.DataFrame) -> pd.DataFrame:
    """Find categories that are not in the allowed list.

    Encontra categorias que não estão na lista permitida.
    """
    cleaned = df[CATEGORY_COL].astype("string").str.strip()
    mask = (cleaned.notna() & ~cleaned.isin(VALID_CATEGORIES)).fillna(False)
    return _build_errors(df, mask, CATEGORY_COL, "unknown_category", CATEGORY_COL)


def validate_all(df: pd.DataFrame) -> pd.DataFrame:
    """Run all checks and return one table with every error.

    Roda todas as checagens e devolve uma tabela com todos os erros.
    """
    missing = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns / Colunas ausentes: {missing}")

    checks = [
        check_missing_values,
        check_negative_amount,
        check_invalid_date,
        check_unknown_category,
    ]
    return pd.concat([check(df) for check in checks], ignore_index=True)


def save_error_report(errors: pd.DataFrame, path: Path = REPORT_FILE) -> Path:
    """Save the error table as a CSV file in the reports folder.

    Salva a tabela de erros em CSV na pasta reports.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    errors.to_csv(path, index=False)
    return path


def main() -> None:
    """Load the consolidated file, validate it and save the report.

    Carrega a base consolidada, valida e salva o relatório.
    """
    df = pd.read_csv(INPUT_FILE)
    errors = validate_all(df)
    out = save_error_report(errors)
    print(f"{len(errors)} erros encontrados / errors found. Relatório: {out}")
    print(errors["error_type"].value_counts())


if __name__ == "__main__":
    main()
