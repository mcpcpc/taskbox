-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS user;
DROP VIEW IF EXISTS task_v;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS task;

CREATE TABLE role (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	slug TEXT UNIQUE NOT NULL,
	description TEXT DEFAULT NULL,
	active INTEGER NOT NULL DEFAULT 0,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT NULL,
	content TEXT DEFAULT NULL
);

CREATE TABLE permission (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	slug TEXT UNIQUE NOT NULL,
	description TEXT DEFAULT NULL,
	active INTEGER NOT NULL DEFAULT 0,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT NULL,
	content TEXT DEFAULT NULL
);

CREATE TABLE role_permission (
	role_id INTEGER NOT NULL,
	permission_id INTEGER NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT NULL,
	PRIMARY KEY(role_id, permission_id)
	FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE NO ACTION ON UPDATE NO ACTION
	FOREIGN KEY(permission_id) REFERENCES permission(id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE user (
	id INTEGER PRIMARY KEY,
	role_id INTEGER NOT NULL,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL UNIQUE,
	first_name TEXT DEFAULT NULL,
	middle_name TEXT DEFAULT NULL,
	last_name TEXT DEFAULT NULL,
	email TEXT DEFAULT NULL,
	mobile TEXT DEFAULT NULL,
	FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE device (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	description TEXT NOT NULL UNIQUE
);

CREATE TABLE task (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	command TEXT NOT NULL,
	device_id INTEGER NOT NULL,
	FOREIGN KEY(device_id) REFERENCES device(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE VIEW task_v AS SELECT
	device.name AS device_name,
	device.description AS device_description,
	task.id as task_id,
	task.name AS task_name
FROM device INNER JOIN task ON task.device_id = device.id;

INSERT INTO permission (title, slug) VALUES ("read", "r"), ("update", "rw"), ("insert", "i"), ("delete", "x");
INSERT INTO role (title, slug) VALUES ("Administrator", "admin"), ("User", "user"), ("Functional User", "functional"), ("Public", "public");
INSERT INTO user (role, username, password) VALUES ("administrator", "admin", "pbkdf2:sha256:260000$gtvpYNx6qtTuY8rt$2e2a4172758fee088e20d915ac4fdef3bdb07f792e42ecb2a77aa5a72bedd5f5");
