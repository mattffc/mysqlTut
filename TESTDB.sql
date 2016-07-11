USE TESTDB;

DROP TABLE IF EXISTS EMPLOYEE;
CREATE TABLE EMPLOYEE
(
  id              int unsigned NOT NULL auto_increment, # Unique ID for the record
  FIRST_NAME           varchar(255) NOT NULL,                # Full title of the book
  LAST_NAME          varchar(255) NOT NULL,                # The author of the book
  AGE          varchar(255) NOT NULL,                # The author of the book
  SEX          varchar(255) NOT NULL,                # The author of the book
  INCOME          varchar(255) NOT NULL,                # The author of the book

  PRIMARY KEY     (id)
);