
# Tables

## Current state of database

```SQL
* users: CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(25), password VARCHAR(26), email VARCHAR(255), permission_id INT, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
* permissions: CREATE TABLE permissions (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, permission INTEGER NOT NULL, checkpoint_id INTEGER, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
* checkpoint: CREATE TABLE checkpoints (id SERIAL PRIMARY KEY, name VARCHAR(50), description VARCHAR(1000), canBeVisible boolean NOT NULL, location_id INTEGER, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
* points: CREATE TABLE points (id SERIAL PRIMARY KEY, checkpoint_id INTEGER NOT NULL, team_id INTEGER NOT NULL, point_amount INTEGER NOT NULL, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
* team: CREATE TABLE teams (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
```

## Possible future developments

* location: id, locationData, checkpoint_id, created, modifed (Possible with PostGIS)

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON todos
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();