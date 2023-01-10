-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP VIEW IF EXISTS task_v;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS task;

CREATE TABLE device (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	description TEXT NOT NULL UNIQUE
);

CREATE TABLE user (
	id INTEGER PRIMARY KEY,
	role TEXT,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL UNIQUE,
	first_name TEXT,
	middle_name TEXT,
	last_name TEXT,
	email TEXT,
	mobile TEXT
);

CREATE TABLE task (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	command TEXT NOT NULL,
	device_id INTEGER NOT NULL,
	FOREIGN KEY(device_id) REFERENCES device(id)
	ON DELETE CASCADE
	ON UPDATE NO ACTION
);

CREATE VIEW task_v AS SELECT
	device.name AS device_name,
	device.description AS device_description,
	task.id as task_id,
	task.name AS task_name
FROM device INNER JOIN task ON task.device_id = device.id;

INSERT INTO user (role, username, password) VALUES ('administrator', 'admin', 'pbkdf2:sha256:260000$gtvpYNx6qtTuY8rt$2e2a4172758fee088e20d915ac4fdef3bdb07f792e42ecb2a77aa5a72bedd5f5');
