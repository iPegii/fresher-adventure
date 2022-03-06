CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(25),
    password TEXT,
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE permission (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users NOT NULL,
    permission INTEGER DEFAULT 0 NOT NULL,
    checkpoint_id INTEGER REFERENCES checkpoint,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE checkpoint (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(1000),
    can_be_visible boolean DEFAULT False NOT NULL,
    location_id INTEGER,
    order_number INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE team (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE location (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    longitude float8 NOT NULL,
    latitude float8 NOT NULL,
    checkpoint_id INTEGER REFERENCES checkpoint,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE point (
    id SERIAL PRIMARY KEY,
    point_amount INTEGER NOT NULL,
    user_id INTEGER REFERENCES users NOT NULL,
    checkpoint_id INTEGER REFERENCES checkpoint NOT NULL,
    team_id INTEGER REFERENCES team NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);