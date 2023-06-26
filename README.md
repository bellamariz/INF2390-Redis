# INF2390 - Bancos NoSQL e Redes Sociais

Estudo sobre utilização dos bancos NoSQL voltado para Redes Sociais. 

NoSQL: Redis
Aluno: Isabella Mariz 
Disciplina: INF2390
Universidade: PUC-Rio

## Rodar Redis-Stack via Docker


Vamos subir o servidor Redis com o Redis-Stack na porta `10001`, sendo acessível via browser na porta `13333`:

```
docker run -p 10001:6379 -p 13333:8001 redis/redis-stack:latest
```

## Acessando o Banco

1) Para acessar o banco via **CLI**, pegamos o ID do container via `docker ps` e fazemos:
  ```
  docker exec -it <container-id> redis-cli
  ```

2) Também é possível conectar ao banco via **cliente Python** usando a lib `redis-py`:
  ```
  redisConn = redis.Redis(host="localhost",port=10001)
  ```

3) Ou podemos usar a interface do **RedisInsight**:

- Host: `127.0.0.1`
- Port: `10001`
- Database Alias: `127.0.0.1:10001`
