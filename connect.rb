require 'redis'
redis = Redis.new(host: "localhost", port: 6379, db: 1)
redis.set("mykey", "hello world")
redis.get("mykey")
