# VeloCap Backend

This is where we store the data and stuff

## Running

1. Start a PosgresSQL instance
```
docker run --name velocap-postgres \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -d postgres
```

2. Start PgAdmin
```
docker run --name velocap-pgadmin \
    -p 80:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=user@domain.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=SuperSecret' \
    -d dpage/pgadmin4
```

3. Go to `localhost:80` for PgAdmin homepage
4. Login with `postgres:mysecretpassword`
5. Run `docker network inspect bridge` and find the IPv4 of the PostgreSQL instance
6. Input it into PgAdmin when connecting to server.
7. To seed the tables, run `main.py` to generate tables and import `founders.csv` and `startups.csv` into the tables, and ensure that `id` isnt included in the `Columns to import`.

## Running REST API

```
flask --app main --debug run
```