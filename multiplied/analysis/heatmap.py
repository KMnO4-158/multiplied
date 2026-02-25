from copy import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def df_global_heatmap(path: str, title: str, df: pd.DataFrame, *, dark=False) -> None:
    """Export image of pyplot of global heatmap

    Parameters
    ----------
    path : str
        Path to save the heatmap, ending with a chosen image format.
    title : str
        Title of the heatmap.
    df : pd.DataFrame
        DataFrame containing the data to be plotted. All available columns are used.
    dark : bool, optional
        Whether to use a dark theme for the plot, by default False.

    Returns
    -------
    None
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(title, str):
        raise TypeError(f"title must be a string got {type(title)}")
    if not isinstance(path, str):
        raise TypeError(f"path must be a string got {type(path)}")

    b_index = 0
    s_index = -1

    while df.columns[s_index][:1] != "s":  # find total stages in data
        if 15 < s_index:
            raise IndexError("Unsupported DataFrame")
        s_index -= 1

    while df.columns[b_index][:1] != "s":  # find bit width of data
        if 15 < s_index:
            raise IndexError("Unsupported DataFrame")
        b_index += 1

    col = (
        list(df.columns)[b_index : s_index + 1]
        if s_index != -1
        else list(df.columns)[b_index:]
    )
    df_ = df[col].sum(axis=0)

    df_ = pd.DataFrame([df_.values], columns=col)
    pd.set_option("display.max_rows", None)

    result_bits = int(str(copy(df_.columns[0])).split("_")[-1][1:]) + 1
    total_stages = int(str(copy(df_.columns[-1])).split("_")[0][1:]) + 1
    print(f"2D\nOutput: {result_bits}-bit, Stages: {total_stages}")

    arr = None
    for s in range(total_stages):
        ppm = []
        for p in range(result_bits >> 1):
            row = [0] * (result_bits)
            for b in range((result_bits) - 1, -1, -1):
                row[b] = df_.loc[:, f"s{s}_p{p}_b{b}"][0]
            ppm.append(row[::-1])
        if arr is None:
            arr = np.array(ppm)
            continue
        arr += np.array(ppm)  # Unify all heatmaps

    print(arr)
    if arr is None:
        raise ValueError("No data found")

    plt.rcdefaults()  # force consistency

    cmap = "magma_r"
    if dark:
        plt.style.use("dark_background")
        cmap = "magma"

    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    im = ax.imshow(arr, cmap=cmap)

    ax.set_xticks(
        range(result_bits), labels=[f"b{i}" for i in range((result_bits) - 1, -1, -1)]
    )
    ax.set_yticks(
        range(result_bits >> 1), labels=[f"p{i}" for i in range(result_bits >> 1)]
    )

    for i in range(result_bits >> 1):
        for j in range((result_bits) - 1, -1, -1):
            ax.text(j, i, arr[i, j], ha="center", va="center", color="w")

    ax.set_title(title, pad=50)

    # -- canvas level offsets ---------------------------------------
    pos = ax.get_position()
    ax.set_position((pos.x0 - 0.05, pos.y0, pos.width, pos.height))

    fig.tight_layout()
    plt.colorbar(im, shrink=0.7)
    plt.savefig(path)

    return None


def df_global_3d_heatmap(
    path: str, title: str, df: pd.DataFrame, *, dark=False
) -> None:
    """Export image of 3d plot with heatmap for each stage stacked along the x-axis

    Parameters
    ----------
    path : str
        Path to save the heatmap, ending with a chosen image format.
    title : str
        Title of the heatmap.
    df : pd.DataFrame
        DataFrame containing the data to be plotted. All available columns are used.
    dark : bool, optional
        Whether to use a dark theme for the plot, by default False.

    Returns
    -------
    None
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(title, str):
        raise TypeError(f"title must be a string got {type(title)}")
    if not isinstance(path, str):
        raise TypeError(f"path must be a string got {type(path)}")

    # -- collect data, metadata -------------------------------------

    b_index = 0
    s_index = -1

    while df.columns[s_index][:1] != "s":  # find total stages in data
        if 15 < s_index:
            raise IndexError("Unsupported DataFrame")
        s_index -= 1

    while df.columns[b_index][:1] != "s":  # find bit width of data
        if 15 < s_index:
            raise IndexError("Unsupported DataFrame")
        b_index += 1

    col = (
        list(df.columns)[b_index : s_index + 1]
        if s_index != -1
        else list(df.columns)[b_index:]
    )
    df_ = df[col].sum(axis=0)

    df_ = pd.DataFrame([df_.values], columns=col)

    pd.set_option("display.max_rows", None)

    result_bits = int(str(copy(df_.columns[0])).split("_")[-1][1:]) + 1
    total_stages = int(str(copy(df_.columns[-1])).split("_")[0][1:]) + 1
    print(f"3D\nOutput: {result_bits}-bit, Stages: {total_stages}")

    # -- build stage heatmaps ---------------------------------------
    arr_list = []
    for s in range(total_stages):
        ppm = []
        for p in range(result_bits >> 1):
            row = [0] * (result_bits)
            for b in range(result_bits):
                row[b] = df_.loc[:, f"s{s}_p{p}_b{b}"][0]
            ppm.append(row[::-1])
        arr_list.append(ppm)

    stages = np.stack(arr_list)
    print(stages)
    vmin, vmax = stages.min(), stages.max()
    stages_norm = (stages - vmin) / (vmax - vmin)
    _, nx, ny = stages_norm.shape

    # -- plot setup -------------------------------------------------
    x_spacing = 2.0
    alpha = 0.7

    plt.rcdefaults()  # force consistency
    if dark:
        plt.style.use("dark_background")
        cmap = plt.get_cmap("magma")
    else:
        cmap = plt.get_cmap("magma_r")
    fig = plt.figure(figsize=(16, 9), dpi=200)
    ax = fig.add_subplot(111, projection="3d")

    # -- build 3d stacked heatmaps ----------------------------------
    for i in range(total_stages):
        x_plane = np.full_like(stages[i], i * x_spacing, shape=[nx + 1, ny + 1])
        y_plane, z_plane = np.meshgrid(
            np.arange((result_bits) + 1),
            np.arange(result_bits >> 1, -1, -1),
            indexing="xy",
        )

        facecolors = cmap(stages_norm[i])

        # plane -- heatmap
        surf = ax.plot_surface(
            x_plane,
            y_plane,
            z_plane,
            facecolors=facecolors,
            shade=False,
            linewidth=0,
            antialiased=True,
            alpha=alpha,
        )
        surf.set_clip_on(False)

        # faint grid
        ax.plot_wireframe(
            x_plane, y_plane, z_plane + 0.001, color="k", linewidth=0.3, alpha=0.2
        ).set_clip_on(False)

    # -- axis values ------------------------------------------------
    ax.set_xticks(
        np.arange(-1, total_stages * 2 - 1, 2),
        [f"stage_{i}" for i in range(total_stages)],
    )
    ax.set_yticks(np.arange(result_bits) + 1, np.arange((result_bits) - 1, -1, -1))
    ax.set_zticks(
        np.arange(result_bits >> 1),
        labels=[f"p{i}" for i in range((result_bits >> 1) - 1, -1, -1)],
    )  # type: ignore

    # -- titles -----------------------------------------------------
    ax.set_xlim(-x_spacing, (total_stages - 1) * x_spacing + x_spacing)
    ax.set_ylabel("bits")
    ax.set_zlabel("Partial Product", va="bottom")
    ax.set_ylim(-0.5, (result_bits) + 0.5)
    ax.set_zlim(-0.5, result_bits >> 1)
    ax.set_title(title, pad=70)

    # -- colour bar -------------------------------------------------
    mappable = plt.cm.ScalarMappable(cmap=cmap)
    mappable.set_array(np.linspace(vmin, vmax, 256))
    cb = plt.colorbar(
        mappable, ax=ax, aspect=40, shrink=0.6, pad=0.2, location="bottom"
    )

    # -- canvas level offsets ---------------------------------------
    cax = cb.ax
    cpos = cax.get_position()
    cax.set_position((cpos.x0, cpos.y0 - 0.1, cpos.width, cpos.height))

    pos = ax.get_position()
    ax.set_position((pos.x0, pos.y0 - 0.1, pos.width, pos.height))

    # -- export ----------------------------------------------------
    ax.set_clip_on(False)  # Fixes 2d planes from being clipped
    ax.set_box_aspect((5, 3, 1), zoom=2)
    plt.savefig(path)


def df_stage_heatmap(path: str, df: pd.DataFrame, stages: list[int]) -> None:
    """Export pyplot heatmap for each selected stage"""

    if not isinstance(stages, list):
        raise TypeError(f"Expected list[int] got {type(stages)}")
    if not all([isinstance(i, int) for i in stages]):
        raise TypeError("All elements of stages must be integers")
    # sum all columns
    # cast to nested list
    # cast nested list to .im_show
    # Use columns as hints to generate axis labels
    # plt.savefig('filename.png')

    # print(df)
    df_ = df.sum(axis=0)
    b_index = 0
    s_index = -1
    while df_.columns[s_index][:1] != "s":
        if 15 < s_index:
            raise IndexError("Unsupported DataFrame")
        s_index -= 1

    while df_.columns[b_index][:1] != "s":
        if 15 < s_index:
            raise IndexError("Unsupported DataFrame")
        b_index += 1

    bits = (int(str(copy(df_.columns[b_index])).split("_")[-1]) + 1) >> 1
    total_stages = int(str(copy(df_.columns[s_index])).split("_")[1]) + 1

    mini_heatmaps = []

    if stages == []:
        stages = [i for i in range(total_stages)]

    for s in stages:
        ppm = []
        for p in range(bits):
            row = [0] * (bits << 1)
            for b in range((bits << 1) - 1, -1, -1):
                row[b] = df_.loc[f"s{s}_p{p}_b{b}"]
            ppm.append(row)
        mini_heatmaps.append(ppm)

    print(df_)
    print(df_.index)
    # print(mini_heatmaps)
    # for i in df_:
    #     print(i)


def df_stage_bound_heatmap(
    path: str, df: pd.DataFrame, stages: list[int], bound: list[tuple[int, int]]
) -> None:
    """Export pyplot heatmap of bounding box region across stages"""
    ...
