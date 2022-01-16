
# Tables

## Current state of database

```SQL
* users: CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(25), password VARCHAR(26), email VARCHAR(255), permission_id INT, created_at timestamp NOT NULL, modifed_at timestamp NOT NULL);
* permissions: CREATE TABLE permissions (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, permission INTEGER NOT NULL, checkpoint_id INTEGER, created_at timestamp NOT NULL, modifed_at timestamp NOT NULL);
* checkpoint: CREATE TABLE checkpoints (id SERIAL PRIMARY KEY, name VARCHAR(50), description VARCHAR(1000), canBeVisible boolean NOT NULL, location_id INTEGER, created_at timestamp NOT NULL, modifed_at timestamp NOT NULL);
* points: CREATE TABLE points (id SERIAL PRIMARY KEY, checkpoint_id INTEGER NOT NULL, team_id INTEGER NOT NULL, point_amount INTEGER NOT NULL, created_at timestamp NOT NULL, modifed_at timestamp NOT NULL);
* team: CREATE TABLE teams (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, created_at timestamp NOT NULL, modifed_at timestamp NOT NULL);
```

## Possible future developments

* location: id, locationData, checkpoint_id, created, modifed (Possible with PostGIS)
