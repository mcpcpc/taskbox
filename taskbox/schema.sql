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
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL UNIQUE
);

CREATE TABLE tasks (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	command TEXT NOT NULL UNIQUE,
	device_id INTEGER NOT NULL,
	FOREIGN KEY(device_id) REFERENCES devices(id)
);

CREATE VIEW tasks_v AS SELECT
	devices.name AS device_name,
	devices.description AS device_description,
	tasks.id as task_id,
	tasks.name AS task_name
FROM devices
INNER JOIN tasks ON tasks.device_id = devices.id;
