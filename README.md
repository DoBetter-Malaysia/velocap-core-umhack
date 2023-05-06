# VeloCap Backend

This is where we store the data and stuff

## Running

1. pip install -r requirements.txt
2. Start a PosgresSQL instance

```
docker run --name velocap-postgres \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -d postgres
```

3. Start PgAdmin

```
docker run --name velocap-pgadmin \
    -p 80:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=user@domain.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=SuperSecret' \
    -d dpage/pgadmin4
```

4. Go to `localhost:80` for PgAdmin homepage
5. Login with `postgres:mysecretpassword`
6. Run `docker network inspect bridge` and find the IPv4 of the PostgreSQL instance
7. Restore the database with `backups/velocap-backup-07052023` using **CUSTOM** Format.

## Running REST API

```
flask --app main --debug run
```
