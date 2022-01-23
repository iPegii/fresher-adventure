
# Tables

## Current state of database

### Users

```SQL
CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(25), password VARCHAR(26), email VARCHAR(255), permission_id INT, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
```

### Permission

```SQL
CREATE TABLE permissions (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, permission INTEGER NOT NULL, checkpoint_id INTEGER, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
```

### Checkpoint

```SQL
CREATE TABLE checkpoints (id SERIAL PRIMARY KEY, name VARCHAR(50), description VARCHAR(1000), canBeVisible boolean NOT NULL, location_id INTEGER, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
```

### Point

```SQL
CREATE TABLE points (id SERIAL PRIMARY KEY, checkpoint_id INTEGER NOT NULL, team_id INTEGER NOT NULL, point_amount INTEGER NOT NULL, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
```

### Team

```SQL
CREATE TABLE teams (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(), modifed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp());
```

## Possible future developments

* location: id, locationData, checkpoint_id, created, modifed (Possible improvement with PostGIS)