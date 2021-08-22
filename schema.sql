CREATE SCHEMA IF NOT EXISTS rest_api;

CREATE TABLE IF NOT EXISTS rest_api.files (
    id SERIAL,
    filename text NOT NULL,
    filesize integer NOT NULL,
    filepath text NOT NULL,
    sensitivity_score integer,
    last_updated timestamp without time zone,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS rest_api.users (
    username text,
    password text
);
