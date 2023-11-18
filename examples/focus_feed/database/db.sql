create schema api;

-- TABLES
create table api.contents (
    id serial primary key,
    topic text not null,
    content text not null,
    published timestamptz
);

create table api.subscriptions (
    id serial primary key,
    user text not null,
    topic text not null,
    subscribed timestamptz
);

-- insert into api.todos (task) values
--   ('finish tutorial 0'), ('pat self on back');
-- ROLE
create role actie nologin;

grant usage on schema api to actie;

grant all on api.contents to actie;

grant all on api.subscriptions to actie;

create role authenticator noinherit login password 'mysecretpassword';

grant actie to authenticator;