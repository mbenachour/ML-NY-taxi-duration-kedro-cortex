from kedro.pipeline import node, Pipeline
from .nodes import (
    extract_features
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=extract_features,
                inputs="trips_train",
                outputs="extract_features",
                name="extract_features",
            )
        ]
    )