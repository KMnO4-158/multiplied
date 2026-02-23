#######################################
# Built-in Complex Truth Table Search #
#######################################

import pandas as pd


def df_early_bitwidth_cout(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows which carry past operand width during partial product generation"""
    ...


def df_late_bitwidth_cout(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows which carry past operand width during reduction"""
    ...
