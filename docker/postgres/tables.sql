CREATE TABLE passengers (
    passenger_id INTEGER,
    survived BOOLEAN DEFAULT NULL,
    Pclass TEXT,
    name TEXT,
    sex TEXT, 
    age REAL,
    sib_sp INTEGER,
    parch INTEGER,
    ticket TEXT,
    fare REAL,
    cabin TEXT,
    embarked TEXT
);
COPY passengers FROM '/docker-entrypoint-init.d/titanic_test.csv' HEADER DELIMITER ',' CSV; 
COPY passengers FROM '/docker-entrypoint-init.d/titanic_train.csv' HEADER DELIMITER ',' CSV; 