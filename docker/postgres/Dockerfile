FROM postgres
COPY tables.sql /docker-entrypoint-initdb.d/tables.sql
COPY titanic_test.csv /docker-entrypoint-init.d/titanic_test.csv
COPY titanic_train.csv /docker-entrypoint-init.d/titanic_train.csv