-- Connect to default data base
\c vagrant;

-- Recreate 'catalog' database
DROP DATABASE IF EXISTS catalog;
CREATE DATABASE catalog;

-- Recreate 'catalog' user
DROP USER IF EXISTS catalog;
CREATE USER catalog WITH PASSWORD 'Golatac@Udacity';

-- Set privileges
GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
