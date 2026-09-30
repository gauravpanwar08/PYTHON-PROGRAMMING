-- Create database
CREATE DATABASE postgresql_db;

-- Create enum type
CREATE TYPE user_status AS ENUM (
    'active',
    'inactive',
    'blocked'
);

-- Create users table
CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email TEXT,
    age SMALLINT,
    salary NUMERIC(10, 2),
    rating DOUBLE PRECISION,
    is_active BOOLEAN,
    birth_date DATE,
    login_time TIME,
    created_at TIMESTAMPTZ,
    account_age INTERVAL,
    user_uuid UUID,
    profile JSONB,
    skills TEXT[],
    status user_status,
    file_data BYTEA
);

-- Insert sample data
INSERT INTO users (
    username,
    email,
    age,
    salary,
    rating,
    is_active,
    birth_date,
    login_time,
    created_at,
    account_age,
    user_uuid,
    profile,
    skills,
    status
)
VALUES (
    'gaurav',
    'gaurav@example.com',
    22,
    75000.50,
    4.8,
    TRUE,
    '2004-01-15',
    '10:30:00',
    CURRENT_TIMESTAMP,
    INTERVAL '2 years',
    '550e8400-e29b-41d4-a716-446655440000',
    '{"city": "Dehradun", "role": "Backend Developer"}',
    ARRAY['Python', 'PostgreSQL', 'FastAPI'],
    'active'
);

-- View data
SELECT * FROM users;

-- View selected columns
SELECT
    username,
    salary,
    is_active,
    skills,
    profile,
    status
FROM users;

