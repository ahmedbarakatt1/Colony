--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2024-11-29 23:46:48

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 16416)
-- Name: oauth_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oauth_tokens (
    oid integer NOT NULL,
    user_id integer,
    access_token text,
    refresh_token text,
    token_type character varying(50),
    expires_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.oauth_tokens OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16415)
-- Name: oauth_tokens_oid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.oauth_tokens_oid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.oauth_tokens_oid_seq OWNER TO postgres;

--
-- TOC entry 4876 (class 0 OID 0)
-- Dependencies: 221
-- Name: oauth_tokens_oid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.oauth_tokens_oid_seq OWNED BY public.oauth_tokens.oid;


--
-- TOC entry 220 (class 1259 OID 16402)
-- Name: project_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_table (
    pid integer NOT NULL,
    pname character varying(255) NOT NULL,
    description text,
    start_date date NOT NULL,
    uid integer NOT NULL
);


ALTER TABLE public.project_table OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16401)
-- Name: project_table_pid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_table_pid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_table_pid_seq OWNER TO postgres;

--
-- TOC entry 4877 (class 0 OID 0)
-- Dependencies: 219
-- Name: project_table_pid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_table_pid_seq OWNED BY public.project_table.pid;


--
-- TOC entry 218 (class 1259 OID 16390)
-- Name: user_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_table (
    uid integer NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password text NOT NULL,
    oauth_provider character varying(255),
    oauth_id character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_table OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: user_table_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_table_uid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_table_uid_seq OWNER TO postgres;

--
-- TOC entry 4878 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_table_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_table_uid_seq OWNED BY public.user_table.uid;


--
-- TOC entry 4708 (class 2604 OID 16419)
-- Name: oauth_tokens oid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_tokens ALTER COLUMN oid SET DEFAULT nextval('public.oauth_tokens_oid_seq'::regclass);


--
-- TOC entry 4707 (class 2604 OID 16405)
-- Name: project_table pid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_table ALTER COLUMN pid SET DEFAULT nextval('public.project_table_pid_seq'::regclass);


--
-- TOC entry 4705 (class 2604 OID 16393)
-- Name: user_table uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_table ALTER COLUMN uid SET DEFAULT nextval('public.user_table_uid_seq'::regclass);


--
-- TOC entry 4870 (class 0 OID 16416)
-- Dependencies: 222
-- Data for Name: oauth_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oauth_tokens (oid, user_id, access_token, refresh_token, token_type, expires_at, created_at) FROM stdin;
\.


--
-- TOC entry 4868 (class 0 OID 16402)
-- Dependencies: 220
-- Data for Name: project_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_table (pid, pname, description, start_date, uid) FROM stdin;
\.


--
-- TOC entry 4866 (class 0 OID 16390)
-- Dependencies: 218
-- Data for Name: user_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_table (uid, username, email, password, oauth_provider, oauth_id, created_at) FROM stdin;
\.


--
-- TOC entry 4879 (class 0 OID 0)
-- Dependencies: 221
-- Name: oauth_tokens_oid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.oauth_tokens_oid_seq', 1, false);


--
-- TOC entry 4880 (class 0 OID 0)
-- Dependencies: 219
-- Name: project_table_pid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_table_pid_seq', 1, false);


--
-- TOC entry 4881 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_table_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_table_uid_seq', 1, false);


--
-- TOC entry 4717 (class 2606 OID 16424)
-- Name: oauth_tokens oauth_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_tokens
    ADD CONSTRAINT oauth_tokens_pkey PRIMARY KEY (oid);


--
-- TOC entry 4715 (class 2606 OID 16409)
-- Name: project_table project_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_table
    ADD CONSTRAINT project_table_pkey PRIMARY KEY (pid);


--
-- TOC entry 4711 (class 2606 OID 16400)
-- Name: user_table user_table_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_table
    ADD CONSTRAINT user_table_email_key UNIQUE (email);


--
-- TOC entry 4713 (class 2606 OID 16398)
-- Name: user_table user_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_table
    ADD CONSTRAINT user_table_pkey PRIMARY KEY (uid);


--
-- TOC entry 4719 (class 2606 OID 16425)
-- Name: oauth_tokens oauth_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_tokens
    ADD CONSTRAINT oauth_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_table(uid);


--
-- TOC entry 4718 (class 2606 OID 16410)
-- Name: project_table project_table_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_table
    ADD CONSTRAINT project_table_uid_fkey FOREIGN KEY (uid) REFERENCES public.user_table(uid) ON DELETE CASCADE;


-- Completed on 2024-11-29 23:46:48

--
-- PostgreSQL database dump complete
--

