import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

if __name__ == '__main__':
    # connect to redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # user data to store in redis
    user1 = {
        "name": "Paul John",
        "email": "paul.john@example.com",
        "age": 42,
        "city": "London"
    }

    user2 = {
        "name": "Eden Zamir",
        "email": "eden.zamir@example.com",
        "age": 29,
        "city": "Tel Aviv"
    }

    user3 = {
        "name": "Paul Zamir",
        "email": "paul.zamir@example.com",
        "age": 35,
        "city": "Tel Aviv"
    }

    # create a schema to create index on
    schema = (
        TextField("$.name", as_name="name"),
        TagField("$.city", as_name="city"),
        NumericField("$.age", as_name="age")
    )

    index_name = "idx:users"
    index_list = r.execute_command('FT._LIST')

    if index_name in index_list:
        r.execute_command('FT.DROPINDEX', index_name)

    # create index
    rs = r.ft(index_name)
    rs.create_index(
        schema,
        definition=IndexDefinition(
            prefix=["user:"], index_type=IndexType.JSON
        )
    )

    # Use JSON.SET to set each user value at the specified path.
    r.json().set("user:1", Path.root_path(), user1)
    r.json().set("user:2", Path.root_path(), user2)
    r.json().set("user:3", Path.root_path(), user3)

    # Let's find user Paul and filter the results by age.
    print(rs.search(
        Query("Paul @age:[30 40]")
    ))

    # Query using JSON Path expressions
    print(rs.search(
        Query("Paul").return_field("$.city", as_field="city")
    ).docs)

    # Aggregate your results
    req = aggregations.AggregateRequest("*").group_by('@city', reducers.count().alias('count'))
    print(rs.aggregate(req).rows)
