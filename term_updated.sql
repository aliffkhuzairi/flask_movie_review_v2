DROP TABLE IF EXISTS ties;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS mal_user;
DROP TABLE IF EXISTS user_info;
DROP TABLE IF EXISTS users;
DROP DOMAIN IF EXISTS domain_email;

CREATE TABLE users (
  id VARCHAR(15) NOT NULL PRIMARY KEY,
  password VARCHAR(20) NOT NULL,
  role VARCHAR(10) NOT NULL CHECK (role IN ('admin', 'user'))
);

CREATE DOMAIN domain_email AS TEXT
  CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

CREATE TABLE user_info (
  id VARCHAR(15) NOT NULL PRIMARY KEY,
  name VARCHAR(15),
  email domain_email,
  reg_date DATE NOT NULL,
  FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE mal_user (
  id VARCHAR(15) NOT NULL PRIMARY KEY,
  mal_time TIMESTAMP,
  FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE movies (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title VARCHAR(30) NOT NULL,
  director VARCHAR(30) NOT NULL,
  genre VARCHAR(20) NOT NULL CHECK (
    genre IN ('action', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'thriller', 'western')
  ),
  rel_date DATE NOT NULL
);

CREATE TABLE reviews (
  mid INTEGER NOT NULL,
  uid VARCHAR(15) NOT NULL,
  ratings SMALLINT NOT NULL CHECK (ratings BETWEEN 0 AND 5),
  review TEXT NOT NULL,
  rev_time TIMESTAMP NOT NULL,
  PRIMARY KEY (mid, uid),
  FOREIGN KEY (mid) REFERENCES movies(id) ON DELETE CASCADE,
  FOREIGN KEY (uid) REFERENCES users(id)
);

CREATE TABLE ties (
  id VARCHAR(15) NOT NULL,
  opid VARCHAR(15) NOT NULL,
  tie VARCHAR(8) NOT NULL CHECK (tie IN ('follow', 'mute')),
  PRIMARY KEY (id, opid),
  FOREIGN KEY (id) REFERENCES users(id),
  FOREIGN KEY (opid) REFERENCES users(id)
);

INSERT INTO users VALUES ('admin', '0000', 'admin');
INSERT INTO users VALUES ('admin2', '0000', 'admin');
INSERT INTO users VALUES ('andy', '0000', 'user');
INSERT INTO users VALUES ('lisa', '1234', 'user');

INSERT INTO user_info VALUES ('admin', 'admin', 'admin@korea.ac.kr', CURRENT_DATE);
INSERT INTO user_info VALUES ('admin2', 'admin2', 'admin2@korea.ac.kr', CURRENT_DATE);
INSERT INTO user_info VALUES ('andy', NULL, NULL, CURRENT_DATE);
INSERT INTO user_info VALUES ('lisa', NULL, NULL, CURRENT_DATE);

INSERT INTO ties VALUES ('andy', 'lisa', 'follow');
INSERT INTO ties VALUES ('lisa', 'andy', 'follow');

INSERT INTO movies (title, director, genre, rel_date) VALUES
  ('The Shawshank Redemption', 'Frank Darabont', 'drama', '1995-01-28'),
  ('12 Angry Men', 'Sidney Lumet', 'drama', '1957-04-01'),
  ('Star Wars', 'George Lucas', 'fantasy', '1977-05-25'),
  ('Toy Story', 'John Lasseter', 'comedy', '1995-12-23'),
  ('The Truman Show', 'Peter Weir', 'comedy', '1998-10-24'),
  ('Nuovo Cinema Paradiso', 'Giuseppe Tornatore', 'drama', '1988-09-29');

INSERT INTO reviews VALUES
  (1, 'admin', 4, 'An incredible movie. One that lives with you.', NOW() - INTERVAL '30 day 1 hour 2 minute'),
  (1, 'andy', 5, 'the best movie in history and the best ending in any entertainment business', NOW() - INTERVAL '3 month 5 hour'),
  (2, 'admin', 5, 'What a Character-Study is Meant to Be.', NOW() - INTERVAL '34 day 34 hour'),
  (2, 'andy', 4, 'So Simple, So Brilliant', NOW() - INTERVAL '190 hour 1 minute'),
  (3, 'admin', 5, 'In A Galaxy Far Away................A Franchise Was Born', NOW() - INTERVAL '3943 hour 4 minute'),
  (3, 'andy', 5, 'The Force will be with you, always.', NOW() - INTERVAL '31 minute'),
  (4, 'admin', 4, 'Plastic Fantastic.', NOW() - INTERVAL '10 minute'),
  (4, 'andy', 5, 'It really is that good. It''s taken me 27 years to realise.', NOW() - INTERVAL '13 minute'),
  (5, 'admin', 5, 'Good Afternoon, Good Evening, and Goodnight.', NOW() - INTERVAL '30 hour'),
  (5, 'andy', 4, 'Incredibly surreal', NOW()),
  (5, 'lisa', 4, 'The film is an amazing combination of existentialism, surrealism, and symbolism.', NOW());
