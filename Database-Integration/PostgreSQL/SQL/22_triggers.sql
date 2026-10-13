-- ==================================================
-- PostgreSQL Triggers
-- Purpose: Automate database actions and audit changes
-- ==================================================

-- Clean up previous examples

DROP TABLE IF EXISTS trigger_employees CASCADE;
DROP TABLE IF EXISTS employee_audit_logs;

DROP FUNCTION IF EXISTS set_employee_updated_at();
DROP FUNCTION IF EXISTS audit_employee_changes();

-- Create the employee table

CREATE TABLE trigger_employees (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL CHECK (salary >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create the audit table

CREATE TABLE employee_audit_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    employee_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    old_salary NUMERIC(10, 2),
    new_salary NUMERIC(10, 2),
    changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT NOT NULL DEFAULT CURRENT_USER
);

-- Create a function to update the timestamp

CREATE FUNCTION set_employee_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- Create a BEFORE UPDATE trigger

CREATE TRIGGER trg_employee_updated_at
BEFORE UPDATE ON trigger_employees
FOR EACH ROW
EXECUTE FUNCTION set_employee_updated_at();

-- Create an audit trigger function

CREATE FUNCTION audit_employee_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO employee_audit_logs (
            employee_id,
            employee_name,
            operation,
            new_salary
        )
        VALUES (
            NEW.id,
            NEW.name,
            TG_OP,
            NEW.salary
        );

        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO employee_audit_logs (
            employee_id,
            employee_name,
            operation,
            old_salary,
            new_salary
        )
        VALUES (
            NEW.id,
            NEW.name,
            TG_OP,
            OLD.salary,
            NEW.salary
        );

        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO employee_audit_logs (
            employee_id,
            employee_name,
            operation,
            old_salary
        )
        VALUES (
            OLD.id,
            OLD.name,
            TG_OP,
            OLD.salary
        );

        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$;

-- Create an AFTER trigger for all three operations

CREATE TRIGGER trg_employee_audit
AFTER INSERT OR UPDATE OR DELETE ON trigger_employees
FOR EACH ROW
EXECUTE FUNCTION audit_employee_changes();

-- Insert sample employees

INSERT INTO trigger_employees (name, department, salary)
VALUES
    ('Rahul', 'IT', 80000),
    ('Priya', 'HR', 65000);

-- Update an employee salary

UPDATE trigger_employees
SET salary = 90000
WHERE name = 'Rahul';

-- Delete an employee

DELETE FROM trigger_employees
WHERE name = 'Priya';

-- View current employees

SELECT *
FROM trigger_employees
ORDER BY id;

-- View audit history

SELECT *
FROM employee_audit_logs
ORDER BY id;

-- Inspect triggers on the employee table

SELECT
    trigger_name,
    event_manipulation,
    action_timing,
    action_orientation
FROM information_schema.triggers
WHERE event_object_table = 'trigger_employees'
ORDER BY trigger_name, event_manipulation;

-- Remove a trigger if needed

DROP TRIGGER IF EXISTS trg_employee_audit
ON trigger_employees;
