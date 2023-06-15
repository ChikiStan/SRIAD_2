create table "patients" (
    "id" bigserial primary key,
    "first_name" varchar(256) not null,
    "middle_name" varchar(256),
    "last_name" varchar(256) not null,
    "male" varchar(256) not null,
    "height" int,
    "weight" int,
    "birthday" timestamp,
    "diagnosis" varchar(256)
);
create table "experiments" (
    "id" bigserial primary key,
    "patient_id" int,
    "created_timestamp" timestamp not null default (now() at time zone 'utc'));

CREATE TABLE "experiment_values"
(
    "id" bigserial primary key,
    "experiment_id" integer not null,
    "head" json,
    "feet_r" json
);