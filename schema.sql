CREATE SCHEMA rest_api;

CREATE TABLE rest_api.files (
    id integer NOT NULL,
    filename text NOT NULL,
    filesize integer NOT NULL,
    filepath text NOT NULL,
    sensitivity_score integer,
    last_updated timestamp without time zone
);

CREATE SEQUENCE rest_api.files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE rest_api.users (
    username text,
    password text
);

ALTER TABLE ONLY rest_api.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);
