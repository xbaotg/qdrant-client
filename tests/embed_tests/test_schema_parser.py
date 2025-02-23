import pytest

from qdrant_client import models
from qdrant_client.embed.schema_parser import ModelSchemaParser
from qdrant_client.embed.utils import FieldPath


def check_path_recursive(plain_path_parts: list[str], paths: list[FieldPath]) -> bool:
    if not plain_path_parts:
        return True

    for path in paths:
        if path.current == plain_path_parts[0]:
            return check_path_recursive(plain_path_parts[1:], path.tail)
    return False


@pytest.mark.parametrize(
    "model",
    [
        models.Batch,
        models.ContextPair,
        models.ContextQuery,
        models.DiscoverInput,
        models.DiscoverQuery,
        models.NearestQuery,
        models.PointStruct,
        models.PointVectors,
        models.PointsBatch,
        models.PointsList,
        models.RecommendInput,
        models.RecommendQuery,
        models.UpdateVectors,
        models.UpdateVectorsOperation,
        models.UpsertOperation,
        models.Prefetch,
        models.QueryGroupsRequest,
        models.QueryRequest,
        models.QueryRequestBatch,
        models.UpdateOperations,
    ],
)
def test_parser(model):
    parser = ModelSchemaParser()
    parser.parse_model(model)

    for model_name, plain_paths in parser._cache.items():
        count = 0
        paths = parser.path_cache[model_name]
        for plain_path in plain_paths:
            count += check_path_recursive(plain_path.split("."), paths)

        assert count == len(plain_paths)
