from pathlib import Path
import multiplied as mp
import pandas as pd
import pyarrow as pa


def test_pq_extract_bits() -> None:
    ...

def test_pq_extract_stages() -> None:
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_4b_mult_truthtable.parquet'
    print(path)
    df1 = mp.pq_extract_stages(str(path))
    print(df1.head())

    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_4b_mult_truthtable.parquet'
    print(path)
    df2 = mp.pq_extract_stages(str(path))
    print(df2.head())


def test_df_global_heatmap_4() -> None:
    alg = mp.Algorithm(4)
    alg.auto_resolve_stage()
    scope = mp.truth_scope((1, 15), (1, 255))
    df = mp.truth_dataframe(scope, alg)
    # pd.set_option('display.max_columns', None)
    # print(df)
    path = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_4b_wallace_heatmap.svg'
    print(path)
    title = "4-Bit Wallace-Tree Truth Table As Cumulative Heatmap"
    mp.df_global_heatmap(str(path), title, df, dark=True)

def test_df_global_heatmap_8() -> None:
    alg = mp.Algorithm(8)
    alg.auto_resolve_stage()
    scope = mp.truth_scope((1, 255), (1, 1000))
    df = mp.truth_dataframe(scope, alg)
    # pd.set_option('display.max_columns', None)
    # print(df)
    path = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_8b_wallace_heatmap.svg'
    print(path)
    title = "8-Bit Wallace-Tree Truth Table As Cumulative Heatmap"
    mp.df_global_heatmap(str(path), title, df, dark=True)

def test_df_global_3d_heatmap_8() -> None:
    alg = mp.Algorithm(8)
    alg.auto_resolve_stage()
    scope = mp.truth_scope((1, 255), (1, 1000))
    df = mp.truth_dataframe(scope, alg)
    # pd.set_option('display.max_columns', None)
    # print(df)
    path = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_8b_wallace_3d_heatmap.svg'
    print(path)
    title = "8-Bit Wallace-Tree Truth Table As 3D Heatmap"
    mp.df_global_3d_heatmap(str(path), title, df, dark=True)

def test_df_global_3d_heatmap_4() -> None:
    alg = mp.Algorithm(4)
    alg.auto_resolve_stage()
    scope = mp.truth_scope((1, 15), (1, 255))
    df = mp.truth_dataframe(scope, alg)
    # pd.set_option('display.max_columns', None)
    # print(df)
    path = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_4b_wallace_3d_heatmap.svg'
    print(path)
    title = "4-Bit Wallace-Tree Truth Table As 3D Heatmap"
    mp.df_global_3d_heatmap(str(path), title, df, dark=True)



def test_pq_global_heatmap_4() -> None:
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_4b_mult_truthtable.parquet'
    print(path)
    df = mp.pq_extract_stages(str(path))
    # print(df.head())
    path2 = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_4b_wallace_heatmap.svg'
    print(path2)
    title = "4-Bit Wallace-Tree Truth Table As Cumulative Heatmap"
    mp.df_global_heatmap(str(path2), title, df, dark=True)

def test_pq_global_heatmap_8() -> None:
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_8b_mult_truthtable.parquet'
    print(path)
    df = mp.pq_extract_stages(str(path))
    # print(df.head())
    path2 = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_8b_wallace_heatmap.svg'
    print(path2)
    title = "8-Bit Wallace-Tree Truth Table As Cumulative Heatmap"
    mp.df_global_heatmap(str(path2), title, df, dark=True)

def test_pq_global_3d_heatmap_4() -> None:
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_4b_mult_truthtable.parquet'
    print(path)
    df = mp.pq_extract_stages(str(path))
    # print(df)
    path2 = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_4b_wallace_3d_heatmap.svg'
    print(path2)
    title = "4-Bit Wallace-Tree Truth Table As 3D Heatmap"
    mp.df_global_3d_heatmap(str(path2), title, df, dark=True)


def test_pq_global_3d_heatmap_8() -> None:
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_8b_mult_truthtable.parquet'
    print(path)
    df = mp.pq_extract_stages(str(path))
    path2 = Path(__file__).parent.parent.parent / 'examples/outputs/example_dark_8b_wallace_3d_heatmap.svg'
    print(path2)
    title = "8-Bit Wallace-Tree Truth Table As 3D Heatmap"
    mp.df_global_3d_heatmap(str(path2), title, df, dark=True)

def test_pq_extract_formatted_all() -> None:
    ...


def test_pq_extract_formatted_stages() -> None:
    ...




def main() -> None:
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_8b_mult_truthtable.parquet'
    ...


if __name__ == "__main__":
    main()
