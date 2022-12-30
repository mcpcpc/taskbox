-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS [tasks];

CREATE TABLE IF NOT EXISTS [tasks] (
	[task_id] INTEGER PRIMARY KEY,
	[device] TEXT NOT NULL UNIQUE,
	[description] TEXT NOT NULL UNIQUE,
	[control] TEXT NOT NULL
);
