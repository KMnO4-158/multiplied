from collections.abc import Generator
import pandas as pd


"""
Exporting to parquet is pretty simple: .to_parquet
After playing with pandas check if it's worth implementing these
"""


def export_parquet(source: pd.DataFrame, path: str, batch_size: int) -> None:
    raise NotImplementedError # pragma: no cover


def import_parquet(path: str, batch_size: int) -> Generator[pd.DataFrame]:
    raise NotImplementedError # pragma: no cover
