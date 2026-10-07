-- ============================================================
-- PostgreSQL Constraints
-- ============================================================

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

-- -------------------------
-- Parent Table
-- -------------------------

CREATE TABLE departments (
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    code VARCHAR(10) NOT NULL,
    CONSTRAINT pk_departments PRIMARY KEY (id),
    CONSTRAINT uq_departments_name UNIQUE (name),
    CONSTRAINT uq_departments_code UNIQUE (code)
);

-- -------------------------
-- Child Table
-- -------------------------

CREATE TABLE employees (
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    age INTEGER NOT NULL,
    department_id INTEGER,
    status TEXT DEFAULT 'active',
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_employees PRIMARY KEY (id),
    CONSTRAINT uq_employees_email UNIQUE (email),
    CONSTRAINT chk_employees_salary CHECK (salary > 0),
    CONSTRAINT chk_employees_age CHECK (age >= 18),
    CONSTRAINT chk_employees_status
        CHECK (status IN ('active', 'inactive', 'on_leave')),
    CONSTRAINT fk_employees_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL
);

-- -------------------------
-- Insert Parent Data
-- -------------------------

INSERT INTO departments (name, code)
VALUES
    ('Engineering', 'ENG'),
    ('Human Resources', 'HR'),
    ('Finance', 'FIN');

-- -------------------------
-- Insert Child Data
-- -------------------------

INSERT INTO employees (
    name,
    email,
    salary,
    age,
    department_id
)
VALUES
    (
        'Gaurav',
        'gaurav@example.com',
        75000,
        22,
        1
    ),
    (
        'Rahul',
        'rahul@example.com',
        65000,
        24,
        1
    ),
    (
        'Priya',
        'priya@example.com',
        60000,
        25,
        2
    );

-- -------------------------
-- View Data
-- -------------------------

SELECT * FROM departments;

SELECT * FROM employees;

-- -------------------------
-- Constraint Demonstration
-- -------------------------

SELECT
    id,
    name,
    email,
    salary,
    age,
    department_id,
    status,
    active,
    created_at
FROM employees
ORDER BY id;