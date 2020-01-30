 create table discount (
    id serial,
    minimum_amount integer not null,
    percentage  integer not null
);

create table tax (
    id serial,
    state varchar(2) not null,
    rate  decimal(5, 2) not null
);

insert into discount (minimum_amount, percentage)
values
    (1000, 3),
    (5000, 5),
    (7000, 7),
    (10000, 10),
    (50000, 15);

insert into tax (state, rate)
values
    ('UT', 6.85),
    ('NV', 8),
    ('TX', 6.25),
    ('AL', 4),
    ('CA', 8.25);
