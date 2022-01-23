CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(25),
    password TEXT,
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE permission (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users NOT NULL,
    permission INTEGER DEFAULT 1 NOT NULL,
    checkpoint_id INTEGER REFERENCES checkpoint,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE checkpoint (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(1000),
    canBeVisible boolean DEFAULT False NOT NULL,
    location_id INTEGER REFERENCES location,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE point (
    id SERIAL PRIMARY KEY,
    checkpoint_id INTEGER REFERENCES checkpoint NOT NULL,
    team_id INTEGER REFERENCES team NOT NULL,
    point_amount INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE team (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE location (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    longitude float8 NOT NULL,
    latitude float8 NOT NULL,
    checkpoint_id INTEGER REFERENCES checkpoint created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
    modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);