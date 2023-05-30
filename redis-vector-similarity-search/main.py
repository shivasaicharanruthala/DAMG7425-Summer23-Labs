import redis
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import numpy as np
import openai
import cohere

r = redis.Redis(host="localhost", port=6379)

INDEX_NAME = "index"  # Vector Index Name
DOC_PREFIX = "doc:"  # RediSearch Key Prefix for the Index


def create_index(vector_dimensions: int):
    try:
        # check to see if index exists
        r.ft(INDEX_NAME).info()
        print("Index already exists!")

    except:
        # schema
        schema = (
            TagField("tag"),  # Tag Field Name
            VectorField("vector",  # Vector Field Name
                        "FLAT", {  # Vector Index Type: FLAT or HNSW
                            "TYPE": "FLOAT32",  # FLOAT32 or FLOAT64
                            "DIM": vector_dimensions,  # Number of Vector Dimensions
                            "DISTANCE_METRIC": "COSINE",  # Vector Search Distance Metric
                        }
                        ),
        )

        # index Definition
        definition = IndexDefinition(prefix=[DOC_PREFIX], index_type=IndexType.HASH)

        # create Index
        r.ft(INDEX_NAME).create_index(fields=schema, definition=definition)


# define vector dimensions
VECTOR_DIMENSIONS = 1536

# create the index
create_index(vector_dimensions=VECTOR_DIMENSIONS)

pipe = r.pipeline()

# define some dummy data
objects = [
    {"name": "a", "tag": "foo"},
    {"name": "b", "tag": "foo"},
    {"name": "c", "tag": "bar"},
]

# write data
for obj in objects:
    # define key
    key = f"doc:{obj['name']}"
    # create a random "dummy" vector
    obj["vector"] = np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
    # HSET
    pipe.hset(key, mapping=obj)

res = pipe.execute()

# KNN Queries
query = (
    Query("*=>[KNN 2 @vector $vec as score]")
    .sort_by("score")
    .return_fields("id", "score")
    .paging(0, 2)
    .dialect(2)
)

query_params = {
    "vec": np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
}

print(r.ft(INDEX_NAME).search(query, query_params).docs)

# Range Queries
query = (
    Query("@vector:[VECTOR_RANGE $radius $vec]=>{$YIELD_DISTANCE_AS: score}")
    .sort_by("score")
    .return_fields("id", "score")
    .paging(0, 3)
    .dialect(2)
)

# Find all vectors within 0.8 of the query vector
query_params = {
    "radius": 0.8,
    "vec": np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
}
print(r.ft(INDEX_NAME).search(query, query_params).docs)

# Hybrid Queries
query = (
    Query("(@tag:{ foo })=>[KNN 2 @vector $vec as score]")
    .sort_by("score")
    .return_fields("id", "tag", "score")
    .paging(0, 2)
    .dialect(2)
)

query_params = {
    "vec": np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
}
print(r.ft(INDEX_NAME).search(query, query_params).docs)


# Vector Creation and Storage
texts = [
    "Today is a really great day!",
    "The dog next door barks really loudly.",
    "My cat escaped and got out before I could close the door.",
    "It's supposed to rain and thunder tomorrow."
]

# delete index
r.ft(INDEX_NAME).dropindex(delete_documents=True)

# make a new one
create_index(vector_dimensions=VECTOR_DIMENSIONS)

# set your OpenAI API key - get one at https://platform.openai.com
openai.api_key = "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"

# Create Embeddings with OpenAI text-embedding-ada-002
# https://openai.com/blog/new-and-improved-embedding-model
response = openai.Embedding.create(input=texts, engine="text-embedding-ada-002")
embeddings = np.array([r["embedding"] for r in response["data"]], dtype=np.float32)

# Write to Redis
pipe = r.pipeline()
for i, embedding in enumerate(embeddings):
    pipe.hset(f"doc:{i}", mapping = {
        "vector": embedding.tobytes(),
        "content": texts[i],
        "tag": "openai"
    })
res = pipe.execute()

print(embeddings)

# Search with OpenAI Embeddings
text = "animals"

# create query embedding
response = openai.Embedding.create(input=[text], engine="text-embedding-ada-002")
query_embedding = np.array([r["embedding"] for r in response["data"]], dtype=np.float32)[0]

print(query_embedding)

# query for similar documents that have the openai tag
query = (
    Query("(@tag:{ openai })=>[KNN 2 @vector $vec as score]")
    .sort_by("score")
    .return_fields("content", "tag", "score")
    .paging(0, 2)
    .dialect(2)
)

query_params = {"vec": query_embedding.tobytes()}
print(r.ft(INDEX_NAME).search(query, query_params).docs)
# the two pieces of content related to animals are returned

# Cohere Embeddings
# delete index
r.ft(INDEX_NAME).dropindex(delete_documents=True)

# make a new one for cohere embeddings (1024 dimensions)
VECTOR_DIMENSIONS = 1024
create_index(vector_dimensions=VECTOR_DIMENSIONS)

co = cohere.Client("rqrfSWYqpNaoMZpX087jvpu2ZrSNtXItpWkNozv5")
# Create Embeddings with Cohere
# https://docs.cohere.ai/docs/embeddings
response = co.embed(texts=texts, model="small")
embeddings = np.array(response.embeddings, dtype=np.float32)

# Write to Redis
for i, embedding in enumerate(embeddings):
    r.hset(f"doc:{i}", mapping = {
        "vector": embedding.tobytes(),
        "content": texts[i],
        "tag": "cohere"
    })

print(embeddings)

# Search with Cohere Embeddings
text = "animals"

# create query embedding
response = co.embed(texts=[text], model="small")
query_embedding = np.array(response.embeddings[0], dtype=np.float32)

print(query_embedding)

# query for similar documents that have the cohere tag
query = (
    Query("(@tag:{ cohere })=>[KNN 2 @vector $vec as score]")
    .sort_by("score")
    .return_fields("content", "tag", "score")
    .paging(0, 2)
    .dialect(2)
)

query_params = {"vec": query_embedding.tobytes()}
print(r.ft(INDEX_NAME).search(query, query_params).docs)
