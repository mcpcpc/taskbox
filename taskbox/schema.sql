-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP VIEW IF EXISTS tasks_v;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE devices (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	description TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	role TEXT,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL UNIQUE
);

CREATE TABLE tasks (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	command TEXT NOT NULL,
	device_id INTEGER NOT NULL,
	FOREIGN KEY(device_id) REFERENCES devices(id)
);

CREATE VIEW tasks_v AS SELECT
	devices.name AS device_name,
	devices.description AS device_description,
	tasks.id as task_id,
	tasks.name AS task_name
FROM devices

INSERT INTO users (role, username, password) VALUES ('admin', 'admin', 'pbkdf2:sha256:260000$gtvpYNx6qtTuY8rt$2e2a4172758fee088e20d915ac4fdef3bdb07f792e42ecb2a77aa5a72bedd5f5');
INNER JOIN tasks ON tasks.device_id = devices.id;
