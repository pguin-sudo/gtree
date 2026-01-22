-- Database initialization script for GTree application
-- This script runs when the PostgreSQL container starts for the first time

-- Create the main user
CREATE USER gtree_user WITH PASSWORD 'gtree_password';

-- Create the database
CREATE DATABASE gtree OWNER gtree_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE gtree TO gtree_user;

-- Connect to the gtree database
\c gtree;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC';

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO gtree_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gtree_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gtree_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gtree_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gtree_user;
