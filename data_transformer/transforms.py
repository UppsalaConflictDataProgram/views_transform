"""
In this file, functions are registered in a registry, which exposes them in the
service.
"""
from views_transformation_library import views_2
from . import porting, lags, util_transforms
from . import registry as registry_module

registry = registry_module.TransformFunctionRegistry()

# =UTIL===================================================

registry.register_function(
        util_transforms.rename,
        "util","rename"
        )

# =OPS====================================================

registry.register_function(
        porting.vectorize_across_dataframe(views_2.ln),
        "ops","ln"
        )

# =BOOLEAN TRANSFORMS=====================================

registry.register_function(
        porting.vectorize_across_dataframe(views_2.greater_or_equal),
        "bool","gte"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.smaller_or_equal),
        "bool","lte"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.in_range),
        "bool","in_range"
        )

# =TEMPORAL TRANSFORMS====================================

registry.register_function(
        porting.vectorize_across_dataframe(views_2.delta),
        "temporal","delta"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.tlag),
        "temporal","tlag"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.tlead),
        "temporal","tlead"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.moving_average),
        "temporal","moving_average"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.moving_sum),
        "temporal","moving_sum"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.cweq),
        "temporal","cweq"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.time_since),
        "temporal","time_since"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.decay),
        "temporal","decay"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.onset_possible),
        "temporal","onset_possible"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.onset),
        "temporal","onset"
        )

# =UNIT TRANSFORMS========================================

registry.register_function(
        porting.vectorize_across_dataframe(views_2.mean),
        "unit","mean"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.demean),
        "unit","demean"
        )

registry.register_function(
        porting.vectorize_across_dataframe(views_2.rollmax),
        "unit","rollmax"
        )

# =SPATIAL TRANSFORMS=====================================

registry.register_function(
        lags.spatial_lag,
        "spatial","lag", applicable_to = ["priogrid_month"],
        )
