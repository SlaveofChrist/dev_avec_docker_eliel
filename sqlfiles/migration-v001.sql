DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    promo VARCHAR(100) NOT NULL
);

INSERT INTO students (nom, promo) VALUES 
('Alice', 'M2 Info'),
('Bob', 'M2 Info'),
('Charlie', 'M2 Info');