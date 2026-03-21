CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de Usuarios
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    created_at  TIMESTAMP NOT NULL DEFAULT now(),
    updated_at  TIMESTAMP NOT NULL DEFAULT now()
);

-- Tabla de Gastos (Expenses)
CREATE TABLE expenses (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title          VARCHAR(255) NOT NULL,
    description    TEXT,
    total_amount   DECIMAL(12, 2) NOT NULL,
    currency       CHAR(3) NOT NULL DEFAULT 'COP',
    category       VARCHAR(100),
    merchant       VARCHAR(255),
    type           VARCHAR(50) NOT NULL DEFAULT 'personal',
    payment_method VARCHAR(50),
    expense_date   TIMESTAMP NOT NULL DEFAULT now(),
    ai_notes       TEXT,
    created_at     TIMESTAMP NOT NULL DEFAULT now(),
    updated_at     TIMESTAMP NOT NULL DEFAULT now()
);