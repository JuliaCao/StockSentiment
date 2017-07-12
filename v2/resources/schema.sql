drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  time integer not null,
  ticker text not null,
  title text not null,
  link text not null,
  sentiment real not null
);