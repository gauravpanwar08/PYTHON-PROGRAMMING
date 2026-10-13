-- ==================================================
-- PostgreSQL Roles & Permissions
-- Purpose: Manage database access securely
-- ==================================================

-- Create group roles

CREATE ROLE app_readonly NOLOGIN;
CREATE ROLE app_writer NOLOGIN;

-- Create login roles

CREATE ROLE app_reader_user
    LOGIN
    PASSWORD 'replace_with_a_strong_secret';

CREATE ROLE app_writer_user
    LOGIN
    PASSWORD 'replace_with_another_strong_secret';

-- Assign group roles to login roles

GRANT app_readonly TO app_reader_user;
GRANT app_writer TO app_writer_user;

-- Create a schema and sample table

CREATE SCHEMA app_data;

CREATE TABLE app_data.employees (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL
);

INSERT INTO app_data.employees (name, email, department, salary)
VALUES ('Rahul', 'rahul@example.com', 'IT', 80000),
       ('Priya', 'priya@example.com', 'HR', 65000);

-- Allow roles to access the schema

GRANT USAGE ON SCHEMA app_data TO app_readonly;
GRANT USAGE ON SCHEMA app_data TO app_writer;

-- Grant table privileges

GRANT SELECT
ON ALL TABLES IN SCHEMA app_data
TO app_readonly;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA app_data
TO app_writer;

-- Configure privileges for future tables
-- Run as app_owner, or an administrator authorized to configure defaults.

ALTER DEFAULT PRIVILEGES
FOR ROLE app_owner
IN SCHEMA app_data
GRANT SELECT ON TABLES TO app_readonly;

ALTER DEFAULT PRIVILEGES
FOR ROLE app_owner
IN SCHEMA app_data
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLES TO app_writer;

-- Revoke a privilege

REVOKE DELETE
ON app_data.employees
FROM app_writer;

-- Inspect roles

SELECT
    rolname,
    rolcanlogin,
    rolsuper,
    rolcreatedb,
    rolcreaterole
FROM pg_roles
WHERE rolname IN (
    'app_readonly',
    'app_writer',
    'app_reader_user',
    'app_writer_user'
)
ORDER BY rolname;

-- Inspect table privileges

SELECT
    grantee,
    privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'app_data'
  AND table_name = 'employees'
ORDER BY grantee, privilege_type;

-- Inspect role memberships

SELECT
    member_role.rolname AS member,
    granted_role.rolname AS granted_role
FROM pg_auth_members AS membership
JOIN pg_roles AS member_role
    ON member_role.oid = membership.member
JOIN pg_roles AS granted_role
    ON granted_role.oid = membership.roleid
WHERE member_role.rolname IN (
    'app_reader_user',
    'app_writer_user'
);
