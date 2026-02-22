##########################################################
# explicit order: map -> matrix -> template -> algorithm #
##########################################################



# -- version -----------------------------------------------------------

__version_info__ = (0, 7, 2)
__version__ = "0.7.2"

# -- core -----------------------------------------------------------

from .core.map import (
    Map,
    build_dadda_map,
    empty_map,
)

from .core.matrix import (
    Matrix,
    Slice,
    empty_rows,
    empty_matrix,
    matrix_merge,
)


from .core.template import (
    Pattern,
    Template,
    build_csa,
    build_adder,
    resolve_pattern,
    build_empty_slice,
)

from .core.algorithm import (
    Algorithm,
    hoist,
    collect_arithmetic_units,
)

from .core.truth import (
    truth_scope,
    truth_table,
    truth_dataframe,
    shallow_truth_table,
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
    isint,
    ishex2,
    ischar,
    isalpha,
    validate_bitwidth,
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
    "Matrix",
    "Slice",
    "Pattern",
    "Template",
    "Algorithm",
    "empty_rows",
    "empty_matrix",
    "matrix_merge",
    "hoist",
    "collect_arithmetic_units",
    "build_dadda_map",
    "empty_map",
    "build_csa",
    "build_adder",
    "build_empty_slice",
    "resolve_pattern",
    "truth_scope",
    "shallow_truth_table",
    "truth_table",
    "truth_dataframe",
    "Map",
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
