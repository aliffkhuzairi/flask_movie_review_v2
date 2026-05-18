--
-- PostgreSQL database dump
--

\restrict q4Q9Kx4OxxJ1kl8eYuTOUysLth4ap0S3jzIlTyHe1SyaajN8qod3TPmRm3TlY8O

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: domain_email; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.domain_email AS text
	CONSTRAINT domain_email_check CHECK ((VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text));


ALTER DOMAIN public.domain_email OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: mal_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mal_user (
    id character varying(15) NOT NULL,
    mal_time timestamp without time zone
);


ALTER TABLE public.mal_user OWNER TO postgres;

--
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying(30) NOT NULL,
    director character varying(30) NOT NULL,
    genre character varying(20) NOT NULL,
    rel_date date NOT NULL,
    poster_url text,
    poster text,
    trailer_url text,
    CONSTRAINT movies_genre_check CHECK (((genre)::text = ANY (ARRAY[('action'::character varying)::text, ('comedy'::character varying)::text, ('drama'::character varying)::text, ('fantasy'::character varying)::text, ('horror'::character varying)::text, ('mystery'::character varying)::text, ('romance'::character varying)::text, ('thriller'::character varying)::text, ('western'::character varying)::text])))
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.movies ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.movies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    mid integer NOT NULL,
    uid character varying(15) NOT NULL,
    ratings smallint NOT NULL,
    review text NOT NULL,
    rev_time timestamp without time zone NOT NULL,
    CONSTRAINT reviews_ratings_check CHECK (((ratings >= 0) AND (ratings <= 5)))
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: ties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ties (
    id character varying(15) NOT NULL,
    opid character varying(15) NOT NULL,
    tie character varying(8) NOT NULL,
    CONSTRAINT ties_tie_check CHECK (((tie)::text = ANY (ARRAY[('follow'::character varying)::text, ('mute'::character varying)::text])))
);


ALTER TABLE public.ties OWNER TO postgres;

--
-- Name: user_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_info (
    id character varying(15) NOT NULL,
    name character varying(15),
    email public.domain_email,
    reg_date date NOT NULL,
    avatar text
);


ALTER TABLE public.user_info OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id character varying(15) NOT NULL,
    password text NOT NULL,
    role character varying(10) NOT NULL,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY (ARRAY[('admin'::character varying)::text, ('user'::character varying)::text])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: mal_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mal_user (id, mal_time) FROM stdin;
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies (id, title, director, genre, rel_date, poster_url, poster, trailer_url) FROM stdin;
9	Titanic	James Cameron	romance	1997-12-19	https://m.media-amazon.com/images/M/MV5BYzYyN2FiZmUtYWYzMy00MzViLWJkZTMtOGY1ZjgzNWMwN2YxXkEyXkFqcGc@._V1_QL75_UX380_CR0,2,380,562_.jpg	\N	https://www.youtube.com/embed/b0KYvGa_nN8
18	Mad Max: Fury Road	George Miller	action	2015-05-15	https://m.media-amazon.com/images/M/MV5BZDRkODJhOTgtOTc1OC00NTgzLTk4NjItNDgxZDY4YjlmNDY2XkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/hEJnMQG9ev8
1	The Shawshank Redemption	Frank Darabont	drama	1995-01-28	https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg	\N	https://www.youtube.com/embed/NmzuHjWmXOc
2	12 Angry Men	Sidney Lumet	drama	1957-04-01	https://m.media-amazon.com/images/M/MV5BYjE4NzdmOTYtYjc5Yi00YzBiLWEzNDEtNTgxZGQ2MWVkN2NiXkEyXkFqcGc@._V1_QL75_UX380_CR0,11,380,562_.jpg	\N	https://www.youtube.com/embed/TEN-2uTi2c0
3	Star Wars	George Lucas	fantasy	1977-05-25	https://m.media-amazon.com/images/M/MV5BOGUwMDk0Y2MtNjBlNi00NmRiLTk2MWYtMGMyMDlhYmI4ZDBjXkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/c_OhgiNE0Dw
4	Toy Story	John Lasseter	comedy	1995-12-23	https://m.media-amazon.com/images/M/MV5BZTA3OWVjOWItNjE1NS00NzZiLWE1MjgtZDZhMWI1ZTlkNzYwXkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/lHg-HPpKpYE
10	Kung Fu Panda	Mark Osborne	comedy	2008-06-06	https://m.media-amazon.com/images/M/MV5BZDU5MDNiMGItYjVmZi00NDUxLTg2OTktNGE0NzNlNzM4NzgyXkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/PXi3Mv6KMzY
11	The Dark Knight	Christopher Nolan	action	2008-07-18	https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/kmJLuwP3MbY
12	Parasite	Bong Joon-ho	thriller	2019-05-30	https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/5xH0HfJHsaY
5	The Truman Show	Peter Weir	comedy	1998-10-24	https://m.media-amazon.com/images/M/MV5BNzA3ZjZlNzYtMTdjMy00NjMzLTk5ZGYtMTkyYzNiOGM1YmM3XkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/nNNdPaEVPxw
6	Nuovo Cinema Paradiso	Giuseppe Tornatore	drama	1988-09-29	https://m.media-amazon.com/images/M/MV5BMTljNzc4YWEtYTZlMS00ODMyLWIwMTAtNWQxY2VkMDEwYTk5XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/JMyVSD6OvO8
7	Inception	Christopher Nolan	action	2010-07-16	https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/8hP9D6kZseM
8	Interstellar	Christopher Nolan	fantasy	2014-11-07	https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/jHiKuXcTrs0
13	La La Land	Damien Chazelle	romance	2016-12-09	https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/0pdqf4P9MB8
14	Whiplash	Damien Chazelle	drama	2014-10-10	https://m.media-amazon.com/images/M/MV5BMDFjOWFkYzktYzhhMC00NmYyLTkwY2EtYjViMDhmNzg0OGFkXkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/7d_jQycdQGo
15	The Matrix	The Wachowskis	action	1999-03-31	https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg	\N	https://www.youtube.com/embed/vKQi3bBA1y8
19	The Grand Budapest Hotel	Wes Anderson	comedy	2014-03-07	https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/1Fg5iWmQjwk
20	Before Sunrise	Richard Linklater	romance	1995-01-27	https://m.media-amazon.com/images/M/MV5BZDZhZmI1ZTUtYWI3NC00NTMwLTk3NWMtNDc0OGNjM2I0ZjlmXkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/6MUcuqbGTxc
38	Wall to Wall	Kim Tae-joon	thriller	2025-07-18	https://m.media-amazon.com/images/M/MV5BM2Y1MjcwMWMtN2IyZi00MGIwLWFiM2YtZjkzZWE1NmJlMGFhXkEyXkFqcGc@._V1_SX300.jpg	\N	https://www.youtube.com/embed/4lLVWhg-_ic
16	Spirited Away	Hayao Miyazaki	fantasy	2001-07-20	https://m.media-amazon.com/images/M/MV5BNTEyNmEwOWUtYzkyOC00ZTQ4LTllZmUtMjk0Y2YwOGUzYjRiXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/ByXuk9QqQkk
17	Joker	Todd Phillips	drama	2019-10-04	https://m.media-amazon.com/images/M/MV5BNzY3OWQ5NDktNWQ2OC00ZjdlLThkMmItMDhhNDk3NTFiZGU4XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N	https://www.youtube.com/embed/zAGVQLHvwOY
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reviews (mid, uid, ratings, review, rev_time) FROM stdin;
1	admin	4	An incredible movie. One that lives with you.	2026-03-25 00:07:15.262335
1	andy	5	the best movie in history and the best ending in any entertainment business	2026-01-23 20:09:15.262335
2	admin	5	What a Character-Study is Meant to Be.	2026-03-19 15:09:15.262335
2	andy	4	So Simple, So Brilliant	2026-04-16 03:08:15.262335
3	admin	5	In A Galaxy Far Away................A Franchise Was Born	2025-11-10 18:05:15.262335
3	andy	5	The Force will be with you, always.	2026-04-24 00:38:15.262335
4	admin	4	Plastic Fantastic.	2026-04-24 00:59:15.262335
4	andy	5	It really is that good. It's taken me 27 years to realise.	2026-04-24 00:56:15.262335
3	khuzairi	5	MAY THE FORCE BE WITH U!	2026-05-11 00:35:14.117882
5	andy	4	Incredibly surreal	2012-08-01 17:02:35.825296
5	lisa	4	The film is an amazing combination of existentialism, surrealism, and symbolism.	2003-05-25 09:26:16.808153
10	aliff	4	There's something about the look of Kung Fu Panda that is so novel and pleasing. Perhaps it's just that we haven't seen this vintage, Far East world in a computer-animated movie before.	2026-04-25 00:19:56.849205
4	lisa	4	The movie was enjoyable and easy to follow. I liked the main character.	2005-03-18 16:43:01.53385
6	andy	5	Very memorable. The atmosphere and music worked well together.	2002-08-20 08:42:55.391251
9	aliff	4	YOU JUMPP I JUMPPP!!!!	2026-04-26 13:31:56.183575
8	andy	5	Fast, intense, and entertaining. No boring moments.	2017-12-12 00:13:06.248201
9	lisa	3	Some funny scenes, but the story was average.	2011-08-29 06:00:57.733758
10	andy	4	Simple but effective. The emotional parts worked well.	2009-02-02 11:35:52.963943
1	lisa	4	I liked the concept and the way the story developed.	2024-10-16 10:03:47.562115
2	lisa	5	Great movie. The ending stayed with me after watching.	1965-12-25 12:39:28.114643
18	khuzairi	4	Mad Max: Fury Road is basically a two-hour, heavy-metal car chase that never lets up. It’s loud, gorgeous, and uses insane real-life stunts that make modern CGI movies look boring by comparison. Furiosa is a total badass, the world is wonderfully weird, and the whole thing is just pure, high-octane energy from start to finish.	2026-04-30 16:44:35.233584
3	lisa	3	EWW THE MONSTERSS	2026-05-01 01:55:08.159189
3	cai	3	⠀⠀⠀⠀⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⡆⣴⣶⣶⣶⡀⠀⢰⣶⣶⣶⣶⣦⡄⠀⠀\r\n⠀⠀⠀⠀⢿⣿⣿⡍⠉⢹⣿⣿⠉⠉⢡⣿⣿⠹⣿⣧⠀⢸⣿⣿⣤⣼⣿⠇⠀⠀\r\n⣶⣶⣶⣶⣶⣿⣿⡿⠀⢸⣿⣿⠀⠀⣾⣿⣿⣿⣿⣿⡆⢸⣿⡟⢿⣿⣷⣶⣶⣶\r\n⣭⣭⡍⢩⣭⣭⡉⣤⣤⡌⢩⣭⣤⣤⡉⠉⢠⣤⣬⣭⣥⣌⡉⠁⢀⣩⣭⣭⣭⣭\r\n⠸⣿⣿⣿⣿⣿⣷⣿⡿⠀⣾⣿⢿⣿⣇⠀⢸⣿⣿⣛⣻⣿⣷⠀⢿⣿⣿⡛⠛⠛\r\n⠀⢻⣿⣿⡿⣿⣿⣿⠃⣸⣿⣿⣼⣿⣿⡄⢸⣿⣿⣿⣿⣿⣥⣤⣬⣿⣿⣿⠀⠀\r\n⠀⠈⠿⠿⠁⠹⠿⠟⠀⠿⠿⠉⠉⠹⠿⠧⠸⠿⠿⠈⠛⠿⠿⠿⠿⠿⠿⠋⠀⠀	2026-05-01 01:56:58.369036
12	cai	3	I think its moderate	2026-04-26 14:46:54.223913
13	aliff	4	I finally got around to watching La La Land and I honestly don't know why I waited so long. I usually don't like musicals, but this felt more like a movie with music rather than a traditional Broadway-style film.\r\n\r\nEven if you aren't a huge fan of musicals, I'd say give it a chance. It’s a sad, beautiful story about chasing dreams, and it’s one of those movies that makes you appreciate the art of filmmaking.	2026-04-26 18:38:24.461082
16	aliff	5	This is more than just a cartoon; it’s a total experience. Even if you've seen it before, it’s worth a rewatch to pick up on the little details. It’s perfect to watch when you want to feel cozy and nostalgic. Absolutely a masterpiece!.	2026-04-26 18:40:01.543848
7	admin	5	A masterpiece of storytelling and visual effects. Nolan at his absolute best. The dream-within-a-dream concept is executed flawlessly.	2010-09-12 14:23:45.123456
7	andy	5	The rotating corridor fight scene alone is worth five stars. Mind-blowing cinema that rewards repeat viewings.	2010-08-02 20:11:30.654321
8	aliff	4	Interstellar is a film that challenges its audience to think while deeply engaging their emotions. It is a contemplative adventure about finding connection across space and time, offering a sense of wonder that few modern films can match. It is an unforgettable experience, a breathtaking journey that remains relevant and highly rewatchable a decade later.	2026-04-27 01:08:11.342448
5	admin	5	Good Afternoon, Good Evening, and Goodnight.	2026-05-05 01:22:29.656892
7	khuzairi	4	Complex but deeply rewarding. Had to watch it twice to fully appreciate what Nolan was doing.	2012-03-15 08:45:22.789012
7	lisa	4	Loved the concept but the ending is deliberately ambiguous. Still a must-watch for any film lover.	2015-06-20 16:30:00.345678
12	khuzairi	5	Parasite is a gripping, entertaining, and intellectually stimulating masterpiece that rightfully made history at the Academy Awards. It is a rare film that is both critically acclaimed and genuinely fun to watch, making it an essential viewing experience.	2026-05-05 01:58:42.787973
7	cai	5	One of the most original films ever made. Absolutely gripping from the first frame to the last.	2011-02-28 21:05:10.901234
7	admin2	3	Visually stunning but the plot gets too convoluted at times. Still an impressive achievement.	2013-11-05 10:00:00.111111
11	admin	5	Heath Ledger's Joker is one of the greatest villain performances in cinema history. A film that transcends its genre.	2008-08-01 19:30:00.222222
11	andy	5	Not just a superhero film â€” a genuinely great crime thriller. Ledger is unforgettable. Nolan's best work.	2008-09-14 22:45:33.333333
11	aliff	5	Rewatched this for the tenth time and it still holds up perfectly. The interrogation scene is pure cinema.	2020-04-10 14:20:00.444444
11	lisa	4	Brilliant film. Ledger deserved every award he received. Dark, intense, and completely gripping.	2009-01-22 11:15:00.555555
11	cai	5	The interrogation scene between Batman and Joker is one of the best scenes ever filmed.	2010-05-05 17:00:00.666666
11	admin2	4	A rare superhero film that transcends the genre entirely. Dark, intelligent, and brilliantly acted.	2011-08-19 09:30:00.777777
14	admin	5	One of the most intense films I have ever seen. J.K. Simmons is terrifying and compelling in equal measure.	2014-12-03 20:00:00.888888
14	andy	5	The final performance scene is one of the best endings in recent cinema. Absolutely electric.	2015-02-14 18:30:00.999999
14	khuzairi	4	Intense and gripping. Makes you question what it truly takes to be great at something.	2015-05-20 15:45:00.10101
14	aliff	5	Every scene with Fletcher is electric. An absolute masterclass in screen performance.	2016-01-08 12:00:00.20202
14	lisa	4	Uncomfortable to watch at times, which is exactly the point. A powerful and important film.	2015-08-30 21:15:00.30303
14	cai	3	Technically impressive but I found it hard to emotionally connect with the characters.	2016-03-12 10:30:00.40404
15	admin	5	Revolutionary filmmaking. Changed action cinema forever. Still looks incredible more than two decades later.	2000-01-15 14:00:00.50505
15	andy	5	The bullet-time sequences were groundbreaking. A genuine game-changer in the history of cinema.	1999-06-20 19:45:00.60606
15	khuzairi	4	A brilliantly crafted sci-fi thriller. The philosophy running beneath the action adds real depth.	2005-11-11 16:00:00.70707
15	aliff	5	Watched this as a kid and it blew my mind completely. Still holds up perfectly decades later.	2019-07-04 20:30:00.80808
15	lisa	4	Iconic for a reason. The action, the story, and the visual effects were all ahead of their time.	2002-04-25 13:15:00.90909
17	admin	5	Joaquin Phoenix disappears into this role completely. One of the greatest performances of the decade.	2019-11-01 21:00:00.010101
17	andy	4	Dark and disturbing in all the right ways. A deeply uncomfortable character study that stays with you.	2019-10-20 18:30:00.020202
17	khuzairi	4	Uncomfortable viewing but important cinema. Phoenix is absolutely mesmerising throughout.	2020-02-14 20:00:00.030303
17	aliff	5	Bold, challenging and brilliantly acted. Not your typical comic book movie by any stretch.	2020-01-10 22:00:00.040404
17	lisa	3	Powerful performance but the film walks a fine line between critique and glorification.	2019-12-25 16:45:00.050505
19	admin	4	Wes Anderson's most accessible film. Charming, witty, and visually stunning in every frame.	2014-04-18 14:30:00.060606
19	andy	5	Pure joy from start to finish. Ralph Fiennes is absolutely perfect in every single scene.	2014-05-22 20:00:00.070707
19	khuzairi	4	Quirky and delightful. The production design alone deserves its own award category.	2015-01-01 12:00:00.080808
19	aliff	4	A beautiful film that works on multiple levels simultaneously. Funny, sad, and utterly unique.	2016-07-15 19:30:00.090909
20	admin	4	Simple, honest and surprisingly moving. Hawke and Delpy have extraordinary chemistry together.	1996-03-10 11:00:00.111222
20	andy	5	A conversation film that somehow feels more real and more alive than most action blockbusters.	1997-08-20 15:30:00.222333
20	khuzairi	3	Beautifully filmed and well-acted but the deliberately slow pace will not be for everyone.	2010-02-14 18:00:00.333444
6	admin	5	A love letter to cinema itself. The ending had me in tears. One of the most beautiful films ever made.	1995-06-15 20:00:00.444555
6	aliff	5	One of the most emotionally powerful films I have ever experienced. An absolute masterpiece.	2018-09-20 21:30:00.555666
6	lisa	4	Slow-burning but deeply rewarding. The final montage sequence is completely unforgettable.	2008-05-10 19:00:00.666777
6	khuzairi	4	Discovered this gem recently. Cannot believe I waited this long to watch it.	2023-01-28 16:45:00.777888
13	admin	4	Gorgeous to look at and listen to. Gosling and Stone are a genuinely perfect pairing.	2017-01-15 20:30:00.888999
13	andy	5	A modern classic. The bittersweet ending is handled with extraordinary emotional intelligence.	2017-02-28 19:00:00.999
13	khuzairi	4	Visually stunning musical with real emotional depth beneath the sparkle. Loved every minute.	2017-04-10 18:00:00.000111
13	lisa	3	Beautiful to look at but I expected more from the story. The original music is truly incredible though.	2018-03-14 21:00:00.111222
16	andy	5	Miyazaki's greatest work. A film that works on every imaginable level. Pure magic.	2002-03-10 14:00:00.222333
16	khuzairi	5	Magical, emotional and unlike anything else in existence. Perfect animation from start to finish.	2010-08-15 20:00:00.333444
16	lisa	4	A stunning visual experience with a surprisingly deep and emotional story. A timeless classic.	2005-12-20 19:30:00.444555
16	cai	4	Studio Ghibli at their absolute peak. Every single frame is a genuine work of art.	2015-07-20 22:00:00.555666
18	admin	4	Pure adrenaline from start to finish. George Miller is a genius for pulling this off at his age.	2015-06-01 20:00:00.666777
18	andy	5	The most impressive action film of the decade. Practical effects used at an extraordinary level.	2015-07-10 21:30:00.777888
18	aliff	4	Relentless and spectacular. Furiosa is one of the best action heroes in years of cinema.	2016-02-20 18:00:00.888999
18	lisa	3	An incredible spectacle but the constant relentless action gets exhausting after a while.	2015-09-15 16:30:00.999
8	khuzairi	5	The docking scene set to Hans Zimmer's score gave me genuine goosebumps. Epic filmmaking.	2015-01-20 21:00:00.000111
8	lisa	4	Ambitious and deeply emotional. The time dilation concepts are genuinely mind-bending.	2015-03-10 19:30:00.111222
8	cai	4	Visually stunning science fiction with a surprisingly heartfelt human story at its core.	2016-04-05 20:00:00.222333
9	admin	5	A technical marvel and an emotional rollercoaster. Still holds up brilliantly after all these years.	1998-02-14 20:00:00.333444
9	andy	4	Epic in every possible sense of the word. The scale of the production is truly staggering.	1998-04-20 19:00:00.444555
9	cai	3	A spectacle for sure but the romance feels somewhat generic beneath all the impressive spectacle.	2012-04-10 18:30:00.555666
10	khuzairi	5	Surprisingly deep for an animated film. The message about believing in yourself is genuinely timeless.	2009-03-14 15:00:00.666777
10	lisa	4	Hilarious and heartwarming in equal measure. Jack Black is absolutely perfect as Po.	2010-06-10 17:30:00.777888
38	admin	4	A surprisingly strong debut. The performances carry the film even when the script falters.	2025-08-10 20:00:00.888999
38	aliff	5	Completely unexpected gem. Did not know what to expect but came away thoroughly impressed.	2025-09-22 18:30:00.999
38	cai	3	Decent enough but feels like it is trying too hard to be profound. Worth watching once.	2025-10-15 21:00:00.000111
7	marco	5	A film that genuinely rewards patience and attention. Nolan constructed something remarkable here.	2011-04-10 18:30:00
11	marco	5	I went in expecting a superhero film and got a crime epic instead. Ledger is beyond words.	2009-03-14 20:00:00
15	marco	4	The world-building in this film is extraordinary. One of the rare films that feels truly original.	2003-07-22 16:45:00
19	marco	4	Every frame is a painting. Anderson has a visual style unlike anyone else working in cinema.	2015-02-08 14:00:00
2	marco	5	Shot almost entirely in one room, yet more gripping than most action films. A genuine masterpiece.	2008-11-30 21:15:00
5	sarah	5	Jim Carrey is absolutely extraordinary in this. A film that gets more relevant every year.	2010-06-18 19:30:00
9	sarah	4	Impossible not to be swept away by this film. The scale and emotion are both equally impressive.	2004-02-14 20:30:00
13	sarah	5	The most beautiful film I have seen in years. Chazelle understands heartache better than most.	2017-03-25 21:00:00
20	sarah	4	Two strangers, one night, one city. Simple premise executed with extraordinary grace and warmth.	2012-09-01 17:00:00
16	sarah	5	Miyazaki created a world so rich and detailed it feels more real than reality. A true wonder.	2008-04-20 15:30:00
1	jake	5	The best film ever made. I know everyone says that but I genuinely believe it. Flawless.	2007-05-20 22:00:00
3	jake	5	Changed cinema forever. The sense of adventure and wonder this film creates is unmatched.	2005-12-25 18:00:00
10	jake	4	Far smarter than it has any right to be. The message lands without ever feeling preachy.	2009-08-15 16:00:00
18	jake	5	Two hours of pure cinematic energy. Miller achieved something nobody thought possible at his age.	2015-08-22 20:30:00
17	jake	4	Phoenix carries this film entirely on his shoulders and never once loses his grip. Stunning.	2020-03-10 19:00:00
4	priya	5	Pixar redefined what animated films could be with this. Still perfect nearly three decades later.	2008-07-04 15:00:00
6	priya	5	I cried for the last twenty minutes. Cinema does not get more beautiful or more honest than this.	2019-03-15 21:30:00
12	priya	5	Bong Joon-ho turns genre expectations upside down in the most satisfying way imaginable.	2020-01-05 20:00:00
14	priya	4	Simmons and Teller are incredible together. The tension in this film is almost unbearable.	2015-04-18 18:30:00
8	priya	4	A rare blockbuster that takes big ideas seriously. The emotional core is what sets it apart.	2015-06-12 17:00:00
\.


--
-- Data for Name: ties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ties (id, opid, tie) FROM stdin;
andy	lisa	follow
lisa	andy	follow
cai	aliff	follow
lisa	aliff	follow
aliff	andy	follow
khuzairi	andy	follow
khuzairi	lisa	mute
khuzairi	aliff	follow
aliff	cai	follow
aliff	lisa	mute
aliff	khuzairi	mute
marco	aliff	follow
marco	andy	follow
marco	sarah	follow
marco	priya	follow
sarah	aliff	follow
sarah	lisa	follow
sarah	marco	follow
sarah	jake	follow
jake	andy	follow
jake	khuzairi	follow
jake	sarah	follow
jake	aliff	follow
priya	aliff	follow
priya	admin	follow
priya	marco	follow
priya	sarah	follow
aliff	marco	follow
aliff	sarah	follow
andy	sarah	follow
andy	jake	follow
khuzairi	marco	follow
khuzairi	priya	follow
lisa	sarah	follow
lisa	priya	follow
\.


--
-- Data for Name: user_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_info (id, name, email, reg_date, avatar) FROM stdin;
admin2	admin2	admin2@korea.ac.kr	2026-04-24	\N
cai	Caii	cai@mail.com	2026-04-26	\N
admin	admin	admin@korea.ac.kr	2026-04-24	\N
andy	Andy Mercury	andym@mail.com	2026-04-24	\N
lisa	Lisa Blackpink	lisabp@mail.com	2026-04-24	\N
khuzairi	Khuzairi	khuzairi@mail.com	2026-04-26	\N
delete	\N	\N	2026-05-10	\N
marco	Marco Rossi	marco.rossi@gmail.com	2026-01-10	\N
sarah	Sarah Chen	sarah.chen@email.com	2026-01-22	\N
jake	Jake Morrison	jake.m@email.com	2026-02-05	\N
priya	Priya Patel	priya.p@email.com	2026-02-18	\N
anon	\N	\N	2026-05-18	\N
aliff	Aliff Khuzairi	aliffkhuzairi07@gmail.com	2026-04-24	https://flask-movie-review.s3.ap-southeast-5.amazonaws.com/avatars/aliff_1479711e8c654f1899c3b705a25edda9.jpg
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, password, role) FROM stdin;
cai	scrypt:32768:8:1$haxai8z9WQ9NAZAW$1ceceac6ecbeaef2c25574012b7f998d47294cc9823c05a3e504f67cd2e22cd05072f9a57d6372b03355180f9b42a41015cb9be18a72e106327ca21d576b8c26	user
khuzairi	scrypt:32768:8:1$t3ZynqFcZmp7zyqu$fd07709fd0683bd0e5fcb53328eae64ed684bbc5cdedecac29e361b6a7802c0c17724bd493d504dd9b3d351299f6793771fc0e45b78af1923e452b6c31287c00	user
aliff	scrypt:32768:8:1$PAKSmKpeGOPeiDJ2$3793c849605eaaa93fdb0f93071ac9c8bbe50e6c8d8b488c36cfd9a3ad76335b69db84af4423d3f1848c1c37e69d0322bb59ecf9463b7e43567a29108600cad8	user
admin	scrypt:32768:8:1$Rt5cC7LFfb93ceJm$a6d3f1667349bf9ff0209e79975ae19b91fb0d8e0bfca3ce9a916f7f3b5df89ae2eac1212bc953ce951f4756137cc8d560ea9f272cfca6f9406fcadd67c3bf6b	admin
lisa	scrypt:32768:8:1$quIc1jvX6NEz6L6G$da53ff042c8a806a404a60d7bcd84b8644b39c6a3269f708f19bb215266bd7c9fa20190ce80de48927d20969775be453537ff9c53664b32dc15eb9b4528923f9	user
andy	scrypt:32768:8:1$TQLl6cQ0NtnLitle$31c99caa470da05f86118c0f4ded12d0e914f28f50e68d0dff02f18b2d13bf5aa970402dbed5a3e7bf85c2e9c3a1ba08feb77717bf6a1539d3a13901cbda1bbf	user
admin2	scrypt:32768:8:1$gmYHIyLN8Bcxxm4v$abaab8c0f52c0e4a2dfa079975f4e9275bfc38ba330cb3a113fad99f25a32e099b565ca2fcd9dd94ab8da424157787b214d76edc5e8ffac27c76d5ae821bdf52	admin
delete	scrypt:32768:8:1$DQErZEsNjzyWlydg$d720386b6f46fa1edcd2b8d1d9bdf88833922b7b21a20b615cfad1722da1a8977c89e8ce0e55d515b1dbb08cb67f8ed6aa0149c00e41f9587b2b8433f5fb6d51	user
anon	scrypt:32768:8:1$k0o7ehkm4RK1SyKv$40a974142b1d22e11bb87c1a013e4a0c1c99d271b2a5f27603b07ee2dd14be64cd2d2486f60d2d26baddcaa52ed4875f49ad9e3a6ee8a803449078ae717454b7	user
marco	scrypt:32768:8:1$ZllCU9RwfddcE0Pu$3d6228eed9e3b3f28ff43a44b5c16b25b800786f45f33d1aed268f69ada21c9bc34ad0e628afdc722be2512a39753630b6abec91154fb436c1e43e099294dba1	user
sarah	scrypt:32768:8:1$ZllCU9RwfddcE0Pu$3d6228eed9e3b3f28ff43a44b5c16b25b800786f45f33d1aed268f69ada21c9bc34ad0e628afdc722be2512a39753630b6abec91154fb436c1e43e099294dba1	user
jake	scrypt:32768:8:1$ZllCU9RwfddcE0Pu$3d6228eed9e3b3f28ff43a44b5c16b25b800786f45f33d1aed268f69ada21c9bc34ad0e628afdc722be2512a39753630b6abec91154fb436c1e43e099294dba1	user
priya	scrypt:32768:8:1$ZllCU9RwfddcE0Pu$3d6228eed9e3b3f28ff43a44b5c16b25b800786f45f33d1aed268f69ada21c9bc34ad0e628afdc722be2512a39753630b6abec91154fb436c1e43e099294dba1	user
\.


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movies_id_seq', 38, true);


--
-- Name: mal_user mal_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mal_user
    ADD CONSTRAINT mal_user_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (mid, uid);


--
-- Name: ties ties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ties
    ADD CONSTRAINT ties_pkey PRIMARY KEY (id, opid);


--
-- Name: movies unique_movie; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT unique_movie UNIQUE (title, rel_date);


--
-- Name: user_info user_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_info
    ADD CONSTRAINT user_info_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: mal_user mal_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mal_user
    ADD CONSTRAINT mal_user_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: reviews reviews_mid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_mid_fkey FOREIGN KEY (mid) REFERENCES public.movies(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(id);


--
-- Name: ties ties_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ties
    ADD CONSTRAINT ties_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: ties ties_opid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ties
    ADD CONSTRAINT ties_opid_fkey FOREIGN KEY (opid) REFERENCES public.users(id);


--
-- Name: user_info user_info_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_info
    ADD CONSTRAINT user_info_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict q4Q9Kx4OxxJ1kl8eYuTOUysLth4ap0S3jzIlTyHe1SyaajN8qod3TPmRm3TlY8O

