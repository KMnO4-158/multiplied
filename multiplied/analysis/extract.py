############################################
# Extract Columns From Multiplied Parquets #
############################################

from copy import copy
import pandas as pd
import pyarrow as pa


# -- cheat sheet ----------------------------------------------------
#
# cols = [("stage_1","ppm_0",f"b{i}") for i in range(8)]
# df   = pd.read_parquet("xyz.parquet", columns=cols)
#
# idx = pd.IndexSlice
#
# df.loc[:, idx["stage_1", :, :]]        # all ppms & bits for stage_1
# df.loc[:, idx[:, "ppm_0", :]]          # that ppm across all stages
# df.loc[:, idx[:, :, "b3"]]             # bit b3 across all stages/ppms
#
#

# TODO add metadata to .parquet datasets to extract bit width, alg length etc


def _validate_path(path: str) -> None:
    """Temporary path validation function"""

    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not path.endswith('.parquet'):
        raise ValueError("path must end with .parquet")

def pq_extract_bits(path: str, bits: list[int], stages: list[int]) -> pd.DataFrame:
    """Return a DataFrame of specified bits across multiple stages from .parquet"""
    _validate_path(path)
    raise NotImplementedError



# -- Sources --
# https://stackoverflow.com/questions/53982871/pandas-reading-first-n-rows-from-parquet-file#69888274
def pq_extract_stages(path: str, *, stages: list[int]=[]) -> pd.DataFrame:
    """Return a DataFrame of specified stages from .parquet

    Parameters
    ----------
    path : str
        Path to Multiplied-generated .parquet file
    stages : list[int]
        List of stages to extract

    Returns
    -------
    pd.DataFrame
        A subset of the original .parquet table

    """

    # Documentation is getting really annoying to find so the following is
    # just an attempt to get things to work

    # -- row[0] without loading entire file -------------------------
    _validate_path(path)
    from pyarrow.parquet import ParquetFile
    pf = ParquetFile(path)
    first = next(pf.iter_batches(batch_size = 1))
    row = pa.Table.from_batches([first]).to_pandas()
    # pd.set_option('display.max_columns', None)

    # print(row)

    # Multiplied datasets will always include formatted string columns
    # with the rightmost columns dedicated to formatted strings.
    # Hence the rightmost column is the final formatted string column

    # This is not optimal at all -- problem for future me ----------- #
    # TODO: manage metadata for .parquet <> DataFrame
    # trim and extract integer
    total_stages = int(copy(row.columns[-1]).split('_')[-1]) + 1
    bits         = (int(str(copy(row.columns[3])).split('_')[-1]) + 1) >> 1


    # print(total_stages,  bits)
    # --------------------------------------------------------------- #

    # loop through stages and push to DataFrame

    if stages == []:
        stages = [s for s in range(total_stages)]

    columns = []
    for s in stages:
        for p in range(bits):
            for b in range((bits << 1)-1, -1, -1):
                # TODO: flatten columns to strings since they're converted anyway
                # e.g: 'stage_0_ppm_4_b_3'
                columns.append(str((f"stage_{s}_ppm_{p}_b_{b}")))

    # Initialize DataFrame with stages as columns
    df = pd.read_parquet(path, columns=columns)
    return df






def pq_extract_formatted_all(path: str) -> pd.DataFrame:
    """Return DataFrame of all formatted strings from .parquet"""
    _validate_path(path)
    raise NotImplementedError

def pq_extract_formatted_stages(path: str, stages: list[int]) -> pd.DataFrame:
    """Return DataFrame of formatted strings across multiple stages from .parquet"""
    _validate_path(path)
    raise NotImplementedError
