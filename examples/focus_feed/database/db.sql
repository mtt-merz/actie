create schema api;

-- TABLES
create table api.contents (
    id serial primary key,
    topic text not null,
    content text not null,
    published int not null
);

create table api.subscriptions (
    id serial primary key,
    user text not null,
    topic text not null,
    policy int not null,
    last_published int not null
);

-- insert into api.todos (task) values
--   ('finish tutorial 0'), ('pat self on back');
-- ROLES
create role actie nologin;

create role authenticator noinherit login password 'mysecretpassword';

-- PRIVILEGES
grant usage on schema api to actie;

grant all on api.contents to actie;

grant all on api.subscriptions to actie;

grant actie to authenticator;