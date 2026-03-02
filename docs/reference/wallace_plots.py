from pathlib import Path
from multiplied import df_global_heatmap, df_global_3d_heatmap, pq_extract_stages, SUPPORTED_BITWIDTHS

THEMES = ["", "_dark"] # "" == default. Do not delete.
FILE_TYPES = ["png", "svg"]


def gen_pq_global_heatmap(dark=False) -> None:

    for bit in SUPPORTED_BITWIDTHS:
        for theme in THEMES:
            for file_type in FILE_TYPES:
                path = (
                    Path(__file__).parent.parent.parent
                    / f"examples/datasets/example_{bit}b_mult_truthtable.parquet"
                )
                print(path)
                df = pq_extract_stages(str(path))
                # print(df.head())
                path2 = (
                    Path(__file__).parent.parent.parent
                    / f"examples/outputs/example{theme}_{bit}b_wallace_heatmap.{file_type}"
                )
                print(path2)
                title = f"{bit}-Bit Wallace-Tree Truth Table As Cumulative Heatmap"

                if theme == "":
                    df_global_heatmap(str(path2), title, df)
                else:
                    df_global_heatmap(str(path2), title, df, dark=True)
    return None


def gen_pq_global_3d_heatmap() -> None:

    for bit in SUPPORTED_BITWIDTHS:
        for theme in THEMES:
            for file_type in FILE_TYPES:
                path = (
                    Path(__file__).parent.parent.parent
                    / f"examples/datasets/example_{bit}b_mult_truthtable.parquet"
                )
                print(path)
                df = pq_extract_stages(str(path))
                # print(df)
                path2 = (
                    Path(__file__).parent.parent.parent
                    / f"examples/outputs/example{theme}_{bit}b_wallace_3d_heatmap.{file_type}"
                )
                print(path2)
                title = f"{bit}-Bit Wallace-Tree Truth Table As 3D Heatmap"

                if theme == "":
                    df_global_3d_heatmap(str(path2), title, df)
                else:
                    df_global_3d_heatmap(str(path2), title, df, dark=True)
    return None


def main():
    gen_pq_global_heatmap()
    gen_pq_global_3d_heatmap()


if __name__ == "__main__":
    main()
