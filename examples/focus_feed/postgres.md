# Postgres setup

Install Postgres into a docker container

```shell
sudo docker run --name tutorial -p 5433:5432 \
                -e POSTGRES_PASSWORD=mysecretpassword \
                -d postgres
```

Connect to the SQL console

```shell
sudo docker exec -it tutorial psql -U postgres
```

Create a schema

```sql
create schema api;
```

Create an API endpoint (table)

```sql
create table api.todos (
  id serial primary key,
  done boolean not null default false,
  task text not null,
  due timestamptz
);

insert into api.todos (task) values
  ('finish tutorial 0'), ('pat self on back');
```

Make a role to use for anonymous web requests

```sql
create role web_anon nologin;

grant usage on schema api to web_anon;
grant select on api.todos to web_anon;
grant insert on api.todos to web_anon;
```

Create a dedicated role for connecting to the database, instead of using the highly privileged postgres role.

```sql
create role authenticator noinherit login password 'mysecretpassword';
grant web_anon to authenticator;
```

Now you can exit the console

```sql
\q
```

# PostgREST setup

Create a template.conf file in your project main path, with the following content

```conf
db-uri = "postgres://authenticator:mysecretpassword@localhost:5433/postgres"
db-schemas = "api"
db-anon-role = "web_anon"
```

Run the server

```shell
postgrest tutorial.conf
```

HTTP requests to the postgres instance are now enabled.

```shell
curl http://localhost:3000/todos
```