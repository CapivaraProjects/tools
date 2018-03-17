CREATE DATABASE GreenEyes;



CREATE TABLE PLANTS (
    id SERIAL PRIMARY KEY,
    scientific_name VARCHAR(2000),
    common_name VARCHAR(2000)
);

CREATE TABLE DISEASES (
    id SERIAL PRIMARY KEY,
    id_plant SERIAL,
    scientific_name VARCHAR(2000),
    common_name VARCHAR(2000),
    FOREIGN KEY (id_plant) REFERENCES PLANTS(id);
);

CREATE TABLE IMAGES (
    id SERIAL PRIMARY KEY,
    id_disease SERIAL,
    url VARCHAR(2000),
    description VARCHAR(2000),
    source VARCHAR(2000)
    FOREIGN KEY (id_disease) REFERENCES DISEASES(id);
);
