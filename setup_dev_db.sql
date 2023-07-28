-- create database and user for development environment
REASSIGN OWNED BY store_dev TO postgres;
DROP OWNED BY store_dev;
DROP USER IF EXISTS store_dev;
DROP DATABASE IF EXISTS store_dev_db;

CREATE USER store_dev WITH password 'store_dev_pwd' CREATEDB CREATEROLE;
CREATE DATABASE store_dev_db
	TEMPLATE template0
	OWNER store_dev
	ENCODING 'utf8'
	LC_COLLATE 'en_US.utf8'
	LC_CTYPE 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE store_dev_db to store_dev;
GRANT USAGE, CREATE ON SCHEMA public TO store_dev;
