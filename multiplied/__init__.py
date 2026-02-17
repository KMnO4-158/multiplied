#!bin/python3


# -- core -----------------------------------------------------------

##########################################################
# explicit order: map -> matrix -> template -> algorithm #
##########################################################


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


# -- Tests ----------------------------------------------------------

# from .tests.test_population import (
#     test_pop_empty_matrix,
#     test_pop_build_matrix,
#     test_pop_algorithm,
# )

# from .tests.test_templates import (
#    test_temp_build_csa4,
#    test_temp_build_csa8,
#    test_temp_build_adder4,
#    test_temp_build_adder8,
# )

# from .tests.test_to_json import (
#     test_to_json4,
#     test_to_json8,
# )


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
