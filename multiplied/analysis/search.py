#######################################
# Built-in Complex Truth Table Search #
#######################################

import multiplied as mp
import pandas as pd
import pyarrow as pa


def df_early_bitwidth_cout(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows which carry past operand width during partial product generation"""
    ...


def df_late_bitwidth_cout(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows which carry past operand width during reduction"""
    ...
