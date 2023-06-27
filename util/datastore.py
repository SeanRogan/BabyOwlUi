import chromadb
from chromadb.config import Settings


# section for relational db, and section for vector db specific functions

# ----------- relational -----------

def save_email_to_rdb(email: str):
    pass


def save_comment_to_rdb(comment: str):
    pass


def register_new_user(info):
    pass


def validate_login(username, password):
    pass


# ----------- vector --------------
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="../stored_files/chroma"))
collection = client.get_or_create_collection(name='test')


def create_new_collection(collection_name):
    return client.get_or_create_collection(collection_name)

def add_to_vdb():
    pass


def vdb_query():
    pass


def vdb_get(collection: str, ids=None, documents=None, metadata=None):
    pass

#
# Querying a Collection
# Chroma collections can be queried in a variety of ways, using the .query method.
#
# You can query by a set of query_embeddings.
#
# collection.query(
#     query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2] ...]
#     n_results=10,
#     where={"metadata_field": "is_equal_to_this"},
#     where_document={"$contains":"search_string"}
# )
#
#
# The query will return the n_results closest matches to each query_embedding, in order. An optional where filter dictionary can be supplied to filter the results by the metadata associated with each document. Additionally, an optional where_document filter dictionary can be supplied to filter the results by contents of the document.
#
# If the supplied query_embeddings are not the same dimension as the collection, an exception will be raised.
#
# You can also query by a set of query_texts. Chroma will first embed each query_text with the collection's embedding function, and then perform the query with the generated embedding.
#
# collection.query(
#     query_texts=["doc10", "thus spake zarathustra", ...]
#     n_results=10,
#     where={"metadata_field": "is_equal_to_this"},
#     where_document={"$contains":"search_string"}
# )
#
# You can also retrieve items from a collection by id using .get.
# collection.get(
#     ids=["id1", "id2", "id3", ...],
#     where={"style": "style1"}
# )
