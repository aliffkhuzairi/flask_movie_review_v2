--
-- PostgreSQL database dump
--

\restrict lP9ZAJLIF5xwLxwi6MIzkjgksKlsEzGRqUe64jmXISPnrnz3Yu6xe25uo7dJ7xg

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

COPY public.movies (id, title, director, genre, rel_date, poster_url, poster) FROM stdin;
5	The Truman Show	Peter Weir	comedy	1998-10-24	https://m.media-amazon.com/images/M/MV5BNzA3ZjZlNzYtMTdjMy00NjMzLTk5ZGYtMTkyYzNiOGM1YmM3XkEyXkFqcGc@._V1_SX300.jpg	\N
7	Inception	Christopher Nolan	action	2010-07-16	https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
8	Interstellar	Christopher Nolan	fantasy	2014-11-07	https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
9	Titanic	James Cameron	romance	1997-12-19	https://m.media-amazon.com/images/M/MV5BYzYyN2FiZmUtYWYzMy00MzViLWJkZTMtOGY1ZjgzNWMwN2YxXkEyXkFqcGc@._V1_QL75_UX380_CR0,2,380,562_.jpg	\N
10	Kung Fu Panda	Mark Osborne	comedy	2008-06-06	https://m.media-amazon.com/images/M/MV5BZDU5MDNiMGItYjVmZi00NDUxLTg2OTktNGE0NzNlNzM4NzgyXkEyXkFqcGc@._V1_SX300.jpg	\N
11	The Dark Knight	Christopher Nolan	action	2008-07-18	https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
12	Parasite	Bong Joon-ho	thriller	2019-05-30	https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_SX300.jpg	\N
13	La La Land	Damien Chazelle	romance	2016-12-09	https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
14	Whiplash	Damien Chazelle	drama	2014-10-10	https://m.media-amazon.com/images/M/MV5BMDFjOWFkYzktYzhhMC00NmYyLTkwY2EtYjViMDhmNzg0OGFkXkEyXkFqcGc@._V1_SX300.jpg	\N
15	The Matrix	The Wachowskis	action	1999-03-31	https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg	\N
17	Joker	Todd Phillips	drama	2019-10-04	https://m.media-amazon.com/images/M/MV5BNzY3OWQ5NDktNWQ2OC00ZjdlLThkMmItMDhhNDk3NTFiZGU4XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
18	Mad Max: Fury Road	George Miller	action	2015-05-15	https://m.media-amazon.com/images/M/MV5BZDRkODJhOTgtOTc1OC00NTgzLTk4NjItNDgxZDY4YjlmNDY2XkEyXkFqcGc@._V1_SX300.jpg	\N
19	The Grand Budapest Hotel	Wes Anderson	comedy	2014-03-07	https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
20	Before Sunrise	Richard Linklater	romance	1995-01-27	https://m.media-amazon.com/images/M/MV5BZDZhZmI1ZTUtYWI3NC00NTMwLTk3NWMtNDc0OGNjM2I0ZjlmXkEyXkFqcGc@._V1_SX300.jpg	\N
6	Nuovo Cinema Paradiso	Giuseppe Tornatore	drama	1988-09-29	https://m.media-amazon.com/images/M/MV5BMTljNzc4YWEtYTZlMS00ODMyLWIwMTAtNWQxY2VkMDEwYTk5XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
16	Spirited Away	Hayao Miyazaki	fantasy	2001-07-20	https://m.media-amazon.com/images/M/MV5BNTEyNmEwOWUtYzkyOC00ZTQ4LTllZmUtMjk0Y2YwOGUzYjRiXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg	\N
38	Wall to Wall	Kim Tae-joon	thriller	2025-07-18	https://m.media-amazon.com/images/M/MV5BM2Y1MjcwMWMtN2IyZi00MGIwLWFiM2YtZjkzZWE1NmJlMGFhXkEyXkFqcGc@._V1_.jpg	\N
1	The Shawshank Redemption	Frank Darabont	drama	1995-01-28	https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg	\N
2	12 Angry Men	Sidney Lumet	drama	1957-04-01	https://m.media-amazon.com/images/M/MV5BYjE4NzdmOTYtYjc5Yi00YzBiLWEzNDEtNTgxZGQ2MWVkN2NiXkEyXkFqcGc@._V1_QL75_UX380_CR0,11,380,562_.jpg	\N
3	Star Wars	George Lucas	fantasy	1977-05-25	https://m.media-amazon.com/images/M/MV5BOGUwMDk0Y2MtNjBlNi00NmRiLTk2MWYtMGMyMDlhYmI4ZDBjXkEyXkFqcGc@._V1_SX300.jpg	\N
4	Toy Story	John Lasseter	comedy	1995-12-23	https://m.media-amazon.com/images/M/MV5BZTA3OWVjOWItNjE1NS00NzZiLWE1MjgtZDZhMWI1ZTlkNzYwXkEyXkFqcGc@._V1_SX300.jpg	\N
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
18	khuzairi	4	Mad Max: Fury Road is basically a two-hour, heavy-metal car chase that never lets up. ItΓÇÖs loud, gorgeous, and uses insane real-life stunts that make modern CGI movies look boring by comparison. Furiosa is a total badass, the world is wonderfully weird, and the whole thing is just pure, high-octane energy from start to finish.	2026-04-30 16:44:35.233584
3	lisa	3	EWW THE MONSTERSS	2026-05-01 01:55:08.159189
3	cai	3	ΓáÇΓáÇΓáÇΓáÇΓú┤Γú╢Γú╢Γú╢Γú╢Γú╢Γú╢Γú╢Γú╢Γú╢ΓíåΓú┤Γú╢Γú╢Γú╢ΓíÇΓáÇΓó░Γú╢Γú╢Γú╢Γú╢ΓúªΓíäΓáÇΓáÇ\r\nΓáÇΓáÇΓáÇΓáÇΓó┐Γú┐Γú┐ΓíìΓáëΓó╣Γú┐Γú┐ΓáëΓáëΓóíΓú┐Γú┐Γá╣Γú┐ΓúºΓáÇΓó╕Γú┐Γú┐ΓúñΓú╝Γú┐ΓáçΓáÇΓáÇ\r\nΓú╢Γú╢Γú╢Γú╢Γú╢Γú┐Γú┐Γí┐ΓáÇΓó╕Γú┐Γú┐ΓáÇΓáÇΓú╛Γú┐Γú┐Γú┐Γú┐Γú┐ΓíåΓó╕Γú┐ΓíƒΓó┐Γú┐Γú╖Γú╢Γú╢Γú╢\r\nΓú¡Γú¡ΓíìΓó⌐Γú¡Γú¡ΓíëΓúñΓúñΓíîΓó⌐Γú¡ΓúñΓúñΓíëΓáëΓóáΓúñΓú¼Γú¡ΓúÑΓúîΓíëΓáüΓóÇΓú⌐Γú¡Γú¡Γú¡Γú¡\r\nΓá╕Γú┐Γú┐Γú┐Γú┐Γú┐Γú╖Γú┐Γí┐ΓáÇΓú╛Γú┐Γó┐Γú┐ΓúçΓáÇΓó╕Γú┐Γú┐Γú¢Γú╗Γú┐Γú╖ΓáÇΓó┐Γú┐Γú┐Γí¢Γá¢Γá¢\r\nΓáÇΓó╗Γú┐Γú┐Γí┐Γú┐Γú┐Γú┐ΓáâΓú╕Γú┐Γú┐Γú╝Γú┐Γú┐ΓíäΓó╕Γú┐Γú┐Γú┐Γú┐Γú┐ΓúÑΓúñΓú¼Γú┐Γú┐Γú┐ΓáÇΓáÇ\r\nΓáÇΓáêΓá┐Γá┐ΓáüΓá╣Γá┐ΓáƒΓáÇΓá┐Γá┐ΓáëΓáëΓá╣Γá┐ΓáºΓá╕Γá┐Γá┐ΓáêΓá¢Γá┐Γá┐Γá┐Γá┐Γá┐Γá┐ΓáïΓáÇΓáÇ	2026-05-01 01:56:58.369036
12	cai	3	I think its moderate	2026-04-26 14:46:54.223913
13	aliff	4	I finally got around to watching La La Land and I honestly don't know why I waited so long. I usually don't like musicals, but this felt more like a movie with music rather than a traditional Broadway-style film.\r\n\r\nEven if you aren't a huge fan of musicals, I'd say give it a chance. ItΓÇÖs a sad, beautiful story about chasing dreams, and itΓÇÖs one of those movies that makes you appreciate the art of filmmaking.	2026-04-26 18:38:24.461082
16	aliff	5	This is more than just a cartoon; itΓÇÖs a total experience. Even if you've seen it before, itΓÇÖs worth a rewatch to pick up on the little details. ItΓÇÖs perfect to watch when you want to feel cozy and nostalgic. Absolutely a masterpiece!.	2026-04-26 18:40:01.543848
8	aliff	4	Interstellar is a film that challenges its audience to think while deeply engaging their emotions. It is a contemplative adventure about finding connection across space and time, offering a sense of wonder that few modern films can match. It is an unforgettable experience, a breathtaking journey that remains relevant and highly rewatchable a decade later.	2026-04-27 01:08:11.342448
5	admin	5	Good Afternoon, Good Evening, and Goodnight.	2026-05-05 01:22:29.656892
12	khuzairi	5	Parasite is a gripping, entertaining, and intellectually stimulating masterpiece that rightfully made history at the Academy Awards. It is a rare film that is both critically acclaimed and genuinely fun to watch, making it an essential viewing experience.	2026-05-05 01:58:42.787973
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
aliff	Aliff Khuzairi	aliffkhuzairi07@gmail.com	2026-04-24	aliff_e92aeaaed4774446a7c65b7e255bd558.jpg
delete	\N	\N	2026-05-10	\N
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

\unrestrict lP9ZAJLIF5xwLxwi6MIzkjgksKlsEzGRqUe64jmXISPnrnz3Yu6xe25uo7dJ7xg

