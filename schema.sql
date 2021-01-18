drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  full string not null,
  alias string not null,
  password string,
  expiration integer
);