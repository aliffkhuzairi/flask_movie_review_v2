--
-- PostgreSQL database dump
--

\restrict xz6h1asuuwJKjOi1s1Qea66hwyxNejBaz8RDKIC13pkCoKuoBrFTMK2mgNxgPIc

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
    reg_date date NOT NULL
);


ALTER TABLE public.user_info OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id character varying(15) NOT NULL,
    password character varying(20) NOT NULL,
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

COPY public.movies (id, title, director, genre, rel_date) FROM stdin;
1	The Shawshank Redemption	Frank Darabont	drama	1995-01-28
2	12 Angry Men	Sidney Lumet	drama	1957-04-01
3	Star Wars	George Lucas	fantasy	1977-05-25
4	Toy Story	John Lasseter	comedy	1995-12-23
5	The Truman Show	Peter Weir	comedy	1998-10-24
6	Nuovo Cinema Paradiso	Giuseppe Tornatore	drama	1988-09-29
7	Inception	Christopher Nolan	action	2010-07-16
8	Interstellar	Christopher Nolan	fantasy	2014-11-07
9	Titanic	James Cameron	romance	1997-12-19
10	Kung Fu Panda	Mark Osborne	comedy	2008-06-06
11	The Dark Knight	Christopher Nolan	action	2008-07-18
12	Parasite	Bong Joon-ho	thriller	2019-05-30
13	La La Land	Damien Chazelle	romance	2016-12-09
14	Whiplash	Damien Chazelle	drama	2014-10-10
15	The Matrix	The Wachowskis	action	1999-03-31
16	Spirited Away	Hayao Miyazaki	fantasy	2001-07-20
17	Joker	Todd Phillips	drama	2019-10-04
18	Mad Max: Fury Road	George Miller	action	2015-05-15
19	The Grand Budapest Hotel	Wes Anderson	comedy	2014-03-07
20	Before Sunrise	Richard Linklater	romance	1995-01-27
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
5	admin	5	Good Afternoon, Good Evening, and Goodnight.	1999-06-25 08:10:25.645501
5	andy	4	Incredibly surreal	2012-08-01 17:02:35.825296
5	lisa	4	The film is an amazing combination of existentialism, surrealism, and symbolism.	2003-05-25 09:26:16.808153
8	aliff	5	The heart of the story isn't the spaceship; it's a fatherâ€™s promise to his daughter. You donâ€™t need a physics degree to feel the absolute gut-punch of Cooper watching years of family videos in a matter of minutes. Itâ€™s a movie about the fear of missing out on your childrenâ€™s lives and the desperate lengths youâ€™d go to for their future.	2021-02-07 01:00:54.466997
1	aliff	5	Really strong movie. The story kept me interested until the end.	1998-11-14 19:14:33.855076
2	aliff	4	Good pacing and nice visuals. Some parts felt slow but still worth watching.	1970-11-05 05:23:36.007434
3	aliff	5	One of the best movies here. Great acting and direction.	1986-09-16 14:56:00.533509
4	lisa	4	The movie was enjoyable and easy to follow. I liked the main character.	2005-03-18 16:43:01.53385
5	aliff	3	Not bad, but I expected more from the ending.	2011-10-03 12:32:31.747997
6	andy	5	Very memorable. The atmosphere and music worked well together.	2002-08-20 08:42:55.391251
7	aliff	4	Solid movie with good performances. I would recommend it.	2012-03-16 14:57:22.385147
8	andy	5	Fast, intense, and entertaining. No boring moments.	2017-12-12 00:13:06.248201
9	lisa	3	Some funny scenes, but the story was average.	2011-08-29 06:00:57.733758
10	andy	4	Simple but effective. The emotional parts worked well.	2009-02-02 11:35:52.963943
1	lisa	4	I liked the concept and the way the story developed.	2024-10-16 10:03:47.562115
2	lisa	5	Great movie. The ending stayed with me after watching.	1965-12-25 12:39:28.114643
\.


--
-- Data for Name: ties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ties (id, opid, tie) FROM stdin;
andy	lisa	follow
lisa	andy	follow
\.


--
-- Data for Name: user_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_info (id, name, email, reg_date) FROM stdin;
admin	admin	admin@korea.ac.kr	2026-04-24
admin2	admin2	admin2@korea.ac.kr	2026-04-24
andy	\N	\N	2026-04-24
lisa	\N	\N	2026-04-24
khuzairi	\N	\N	2026-04-24
cai	\N	\N	2026-04-24
aliff	Aliff Khuzairi	aliff@mail.com	2026-04-24
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, password, role) FROM stdin;
admin	0000	admin
admin2	0000	admin
andy	0000	user
lisa	1234	user
aliff	1234	user
cai	1111	user
khuzairi	1111	user
\.


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movies_id_seq', 24, true);


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

\unrestrict xz6h1asuuwJKjOi1s1Qea66hwyxNejBaz8RDKIC13pkCoKuoBrFTMK2mgNxgPIc

