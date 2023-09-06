# Create milvus collection (delete first if exists)
from pymilvus import FieldSchema, CollectionSchema, Collection, DataType
from pymilvus.orm import utility

INDEX_TYPE = 'IVF_FLAT'
METRIC_TYPE = 'L2'


def create_milvus_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        return Collection(name=collection_name)

    fields = [
        FieldSchema(name='path', dtype=DataType.VARCHAR, description='path to image', max_length=500,
                    is_primary=True, auto_id=False),
        FieldSchema(name='image_vector', dtype=DataType.FLOAT_VECTOR, description='image vectors', dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description='reverse image search')
    collection = Collection(name=collection_name, schema=schema)

    index_params = {
        'metric_type': METRIC_TYPE,
        'index_type': INDEX_TYPE,
        'params': {"nlist": dim}
    }
    collection.create_index(field_name='image_vector', index_params=index_params)
    return collection


def rebuild_milvus_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
    return create_milvus_collection(collection_name, dim)
