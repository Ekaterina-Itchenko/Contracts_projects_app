PRAGMA foreign_keys = ON;
CREATE TABLE projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    created_at NUMERIC DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE statuses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE contracts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at NUMERIC DEFAULT CURRENT_TIMESTAMP,
    signed_at NUMERIC,
    status_id INTEGER,
    project_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES statuses(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
INSERT INTO statuses(name) VALUES("draft"), ("active"), ("completed");
