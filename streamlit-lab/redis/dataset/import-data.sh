sleep 5
redis-cli -h redis-stack -p 6379 < /dataset/import_actors.redis
redis-cli -h redis-stack -p 6379 < /dataset/import_movies.redis
redis-cli -h redis-stack -p 6379 < /dataset/import_users.redis
redis-cli -h redis-stack -p 6379 < /dataset/import_theaters.redis
redis-cli -h redis-stack -p 6379 < /dataset/import_create_index.redis
