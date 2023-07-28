-- create database and user for production environment
REASSIGN OWNED BY store_prod TO postgres;
DROP OWNED BY store_prod;
DROP USER IF EXISTS store_prod;
DROP DATABASE IF EXISTS store_prod_db;

CREATE USER store_prod WITH password 'store_prod_pwd' CREATEDB CREATEROLE;
CREATE DATABASE store_prod_db
	TEMPLATE template0
	OWNER store_prod
	ENCODING 'utf8'
	LC_COLLATE 'en_US.utf8'
	LC_CTYPE 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE store_prod_db to store_prod;
GRANT USAGE, CREATE ON SCHEMA public TO store_prod;
