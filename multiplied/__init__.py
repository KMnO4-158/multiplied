##########################################################
# explicit order: map -> matrix -> template -> algorithm #
##########################################################


# -- version --------------------------------------------------------

__version_info__ = (0, 9, 0)
__version__ = "0.9.0"

# -- core -----------------------------------------------------------

from .core.map import (
    Map,
    empty_map,
    build_dadda_map,
    raw_zero_map,
    raw_dadda_map,
    unify_bounds,
    apply_complex_map,
)

from .core.matrix import (
    Matrix,
    Slice,
    empty_rows,
    raw_empty_row_pos,
    raw_empty_rows,
    raw_empty_matrix,
    raw_zero_matrix,
    matrix_scatter,
    matrix_merge,
)


from .core.template import (
    Pattern,
    Template,
    build_csa,
    build_adder,
    build_noop,
    resolve_pattern,
    build_empty_slice,
)

from .core.algorithm import (
    Algorithm,
    hoist,
)

from .core.truth import (
    truth_scope,
    truth_table,
    truth_dataframe,
    shallow_truth_table,
    truth_multi_parquet,
)


# -- utils ----------------------------------------------------------

from .core.utils.char import (
    chargen,
    chartff,
    allchars,
    to_int_matrix,
)


from .core.utils.pretty import (
    pretty,
    mprint,
)

from .core.utils.bool import (
    isppm,
    isint,
    ishex2,
    ischar,
    isalpha,
    validate_bitwidth,
    SUPPORTED_BITWIDTHS,
)
# -- datasets -------------------------------------------------------


# -- io -------------------------------------------------------------

from .io.lazy_json import (
    export_algorithm,
    import_algorithm,
    json_pretty_store,
)

from .io.parquet import (
    export_parquet,
    import_parquet,
)

# -- Analysis -------------------------------------------------------

# from .analysis.context import ()

from .analysis.extract import (
    pq_extract_bits,
    pq_extract_stages,
    pq_extract_formatted_all,
    pq_extract_formatted_stages,
)


from .analysis.heatmap import (
    df_global_heatmap,
    df_global_3d_heatmap,
    df_stage_heatmap,
    df_stage_bound_heatmap,
)

# from .analysis.search import ()


# -- External -------------------------------------------------------


# -- __all__ --------------------------------------------------------

__all__ = [
    "SUPPORTED_BITWIDTHS",
    "Map",
    "build_dadda_map",
    "empty_map",
    "raw_empty_row_pos",
    "raw_empty_rows",
    "raw_zero_map",
    "raw_dadda_map",
    "unify_bounds",
    "apply_complex_map",
    "Matrix",
    "Slice",
    "Pattern",
    "Template",
    "Algorithm",
    "empty_rows",
    "raw_empty_matrix",
    "raw_zero_matrix",
    "matrix_scatter",
    "matrix_merge",
    "hoist",
    "build_csa",
    "build_adder",
    "build_noop",
    "build_empty_slice",
    "resolve_pattern",
    "truth_scope",
    "truth_table",
    "truth_dataframe",
    "shallow_truth_table",
    "truth_multi_parquet",
    "isppm",
    "ischar",
    "isalpha",
    "ishex2",
    "isint",
    "chargen",
    "chartff",
    "allchars",
    "to_int_matrix",
    "pretty",
    "mprint",
    "validate_bitwidth",
    "export_algorithm",
    "import_algorithm",
    "json_pretty_store",
    "export_parquet",
    "import_parquet",
    "pq_extract_bits",
    "pq_extract_stages",
    "pq_extract_formatted_all",
    "pq_extract_formatted_stages",
    "df_global_heatmap",
    "df_global_3d_heatmap",
    "df_stage_heatmap",
    "df_stage_bound_heatmap",
]
