-- Create database
CREATE DATABASE company_db;
CREATE DATABASE data_types_db;

-- List all databases in the cluster, excluding template databases
SELECT datname
FROM pg_database
WHERE datistemplate = false;

-- List all tables specifically located in the default 'public' schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'company';

-- List all user-defined base tables across all schemas (excluding system/internal schemas) using standard SQL information_schema
SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE table_type = 'BASE TABLE' 
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;

-- Alternative: List all user-defined tables using PostgreSQL's internal catalog (pg_catalog)
SELECT schemaname, tablename 
FROM pg_catalog.pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;


-- Create schema
CREATE SCHEMA company;

-- Create employees table
CREATE TABLE company.employees (
    id INTEGER,
    name VARCHAR(100),
    salary NUMERIC(10, 2)
);

-- Add a column
ALTER TABLE company.employees
ADD COLUMN email VARCHAR(150);

-- View table structure
SELECT * FROM company.employees;

-- Remove all rows
TRUNCATE TABLE company.employees;

-- Remove table
DROP TABLE company.employees;

-- Remove schema
DROP SCHEMA company;

-- Remove database
DROP DATABASE data_types_db WITH (FORCE);