DROP DATABASE IF EXISTS todo_database;
CREATE DATABASE todo_database CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE todo_database;

DROP TABLE IF EXISTS todos;
CREATE TABLE todos (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  done BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO todos (title, description)
VALUES
  ("title1", "description1"),
  ("title2", "description2"),
  ("title3", "description3");

