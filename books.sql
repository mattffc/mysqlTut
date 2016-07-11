USE bookstore;

DROP TABLE IF EXISTS books;
CREATE TABLE books
(
  id              int unsigned NOT NULL auto_increment, # Unique ID for the record
  title           varchar(255) NOT NULL,                # Full title of the book
  author          varchar(255) NOT NULL,                # The author of the book
  price           decimal(10,2) NOT NULL,               # The price of the book

  PRIMARY KEY     (id)
);