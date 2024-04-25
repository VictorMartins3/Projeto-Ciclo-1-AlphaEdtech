BEGIN;

CREATE TABLE IF NOT EXISTS users (
   id_user SERIAL PRIMARY KEY,
   username VARCHAR(255),
   email VARCHAR(255),
   password VARCHAR(255),
   date_joined TIMESTAMP WITH TIME ZONE,
   active BOOL
);

CREATE TABLE IF NOT EXISTS doc_rg (
   id_doc SERIAL PRIMARY KEY,
   name VARCHAR(255),
   rg_number VARCHAR(255),
   cpf_number VARCHAR(255),
   issuing_body VARCHAR(255),
   issue_date DATE,
   birth_place VARCHAR(255),
   birthdate DATE,
   photo BYTEA,
   father_name VARCHAR(255),
   mother_name VARCHAR(255),
   signature BYTEA,
   doc_origin VARCHAR(255),
   observation VARCHAR(255),
   id_user INT REFERENCES users(id_user)
);

CREATE TABLE IF NOT EXISTS doc_cnh (
   id_doc SERIAL PRIMARY KEY,
   name VARCHAR(255),
   cpf_number VARCHAR(255),
   validator_number BIGINT,
   registration_number BIGINT,
   issuing_body VARCHAR(255),
   uf VARCHAR(255),
   rg_number VARCHAR(255),
   birthdate DATE,
   issue_date DATE,
   issue_place VARCHAR(255),
   expiration_date DATE,
   photo BYTEA,
   mother_name VARCHAR(255),
   father_name VARCHAR(255),
   id_user INT REFERENCES users(id_user)
);

CREATE TABLE IF NOT EXISTS roles (
   id_role SERIAL PRIMARY KEY,
   role_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_roles (
   id_user INT REFERENCES users(id_user),
   id_role INT REFERENCES roles(id_role),
   PRIMARY KEY (id_user, id_role)
);

CREATE INDEX IF NOT EXISTS idx_id_role ON roles(id_role);
CREATE INDEX IF NOT EXISTS idx_role_name ON roles(role_name);

CREATE INDEX IF NOT EXISTS idx_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_id_user ON users(id_user);
CREATE INDEX IF NOT EXISTS idx_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_active ON users(active);
CREATE INDEX IF NOT EXISTS idx_date_joined ON users USING BRIN (date_joined);

CREATE INDEX IF NOT EXISTS idx_id_doc_rg ON doc_rg(id_doc);
CREATE INDEX IF NOT EXISTS idx_name_rg ON doc_rg(name);
CREATE INDEX IF NOT EXISTS idx_rg_number ON doc_rg(rg_number);
CREATE INDEX IF NOT EXISTS idx_cpf_number_rg ON doc_rg(cpf_number);

CREATE INDEX IF NOT EXISTS idx_id_doc_cnh ON doc_cnh(id_doc);
CREATE INDEX IF NOT EXISTS idx_name_cnh ON doc_cnh(name);
CREATE INDEX IF NOT EXISTS idx_cpf_number_cnh ON doc_cnh(cpf_number);
CREATE INDEX IF NOT EXISTS idx_registration_number ON doc_cnh(registration_number);

END;
