create schema api;

-- TABLES
create table api.articles (
    id serial primary key,
    topic text not null,
    body text not null,
    published bigint not null
);

create table api.subscriptions (
    id serial primary key,
    user_name text not null,
    topic text not null,
    user_policy int not null,
    last_published bigint not null
);

-- insert into api.todos (task) values
--   ('finish tutorial 0'), ('pat self on back');
-- ROLES
create role actie nologin;

create role authenticator noinherit login password 'mysecretpassword';

-- PRIVILEGES
grant usage on schema api to actie;

grant usage,
select
    on all sequences in schema api to actie;

grant all on api.articles to actie;

grant all on api.subscriptions to actie;

grant actie to authenticator;