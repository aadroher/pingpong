drop table if exists bookings;
create table bookings (
  id integer primary key autoincrement,
  start_datetime text not null,
  ping_pong_table text not null,
  booker_name text not null,
  booker_email text,
  notes text
);
