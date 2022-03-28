-- SQLite

drop table if exists students;
drop table if exists dates;
drop table if exists attendance;

create table students(
    id integer primary key not null,
    fullname text not null,
    gender text not null,
    dob text not null,
    absent_count integer default 0,
    image blob
);

create table dates(
    date text primary key not null
);

create table attendance(
    student_id integer not null,
    date text not null,
    foreign key(student_id) references students(id),
    foreign key(date) references dates(date)
);
