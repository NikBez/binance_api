CREATE TABLE IF NOT EXISTS example_table (
    id SERIAL PRIMARY KEY,
    name TEXT
);

INSERT INTO example_table (name) VALUES ('example_value');
