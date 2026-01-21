--
-- PostgreSQL database dump
--

\restrict ontHHgBfoNZZlEDXAfdpBc53mKawTSBN66lecfuFKkVu1yZXFwII7j36mcqKjrN

-- Dumped from database version 17.6 (Debian 17.6-1.pgdg12+1)
-- Dumped by pg_dump version 17.6 (Debian 17.6-1.pgdg12+1)

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
-- Name: question_type_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.question_type_enum AS ENUM (
    'CLOSED',
    'OPEN'
);


ALTER TYPE public.question_type_enum OWNER TO root;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO root;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.answer (
    id bigint NOT NULL,
    assessment_id integer NOT NULL,
    question_id integer NOT NULL,
    selected_option_id integer,
    text_answer text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.answer OWNER TO root;

--
-- Name: COLUMN answer.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.answer.id IS 'unique identifier for the entity';


--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.answer_id_seq OWNER TO root;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: assessment; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.assessment (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    survey_id integer NOT NULL,
    started_at timestamp with time zone NOT NULL,
    finished_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.assessment OWNER TO root;

--
-- Name: COLUMN assessment.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.assessment.id IS 'unique identifier for the entity';


--
-- Name: assessment_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.assessment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assessment_id_seq OWNER TO root;

--
-- Name: assessment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.assessment_id_seq OWNED BY public.assessment.id;


--
-- Name: feedback; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.feedback (
    id bigint NOT NULL,
    assessment_id integer NOT NULL,
    summary_text text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.feedback OWNER TO root;

--
-- Name: COLUMN feedback.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.feedback.id IS 'unique identifier for the entity';


--
-- Name: feedback_answer; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.feedback_answer (
    assessment_id integer NOT NULL,
    answer_id integer NOT NULL,
    feedback text NOT NULL,
    score double precision NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id bigint NOT NULL
);


ALTER TABLE public.feedback_answer OWNER TO root;

--
-- Name: COLUMN feedback_answer.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.feedback_answer.id IS 'unique identifier for the entity';


--
-- Name: feedback_answer_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.feedback_answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feedback_answer_id_seq OWNER TO root;

--
-- Name: feedback_answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.feedback_answer_id_seq OWNED BY public.feedback_answer.id;


--
-- Name: feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feedback_id_seq OWNER TO root;

--
-- Name: feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.feedback_id_seq OWNED BY public.feedback.id;


--
-- Name: option; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.option (
    id bigint NOT NULL,
    question_id integer NOT NULL,
    text text NOT NULL,
    is_correct boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.option OWNER TO root;

--
-- Name: COLUMN option.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.option.id IS 'unique identifier for the entity';


--
-- Name: option_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.option_id_seq OWNER TO root;

--
-- Name: option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.option_id_seq OWNED BY public.option.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.question (
    id bigint NOT NULL,
    survey_id integer NOT NULL,
    description text NOT NULL,
    question_type public.question_type_enum NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    hint text
);


ALTER TABLE public.question OWNER TO root;

--
-- Name: COLUMN question.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.question.id IS 'unique identifier for the entity';


--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_id_seq OWNER TO root;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: survey; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.survey (
    id bigint NOT NULL,
    topic character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.survey OWNER TO root;

--
-- Name: COLUMN survey.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.survey.id IS 'unique identifier for the entity';


--
-- Name: survey_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.survey_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.survey_id_seq OWNER TO root;

--
-- Name: survey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.survey_id_seq OWNED BY public.survey.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."user" (
    id bigint NOT NULL,
    nickname character varying(100) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public."user" OWNER TO root;

--
-- Name: COLUMN "user".id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public."user".id IS 'unique identifier for the entity';


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO root;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: assessment id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.assessment ALTER COLUMN id SET DEFAULT nextval('public.assessment_id_seq'::regclass);


--
-- Name: feedback id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback ALTER COLUMN id SET DEFAULT nextval('public.feedback_id_seq'::regclass);


--
-- Name: feedback_answer id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback_answer ALTER COLUMN id SET DEFAULT nextval('public.feedback_answer_id_seq'::regclass);


--
-- Name: option id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.option ALTER COLUMN id SET DEFAULT nextval('public.option_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: survey id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.survey ALTER COLUMN id SET DEFAULT nextval('public.survey_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.alembic_version (version_num) FROM stdin;
23111be7e35c
\.


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.answer (id, assessment_id, question_id, selected_option_id, text_answer, created_at, updated_at) FROM stdin;
1	1	65	\N	No sé	2026-01-21 09:36:38.128963+00	2026-01-21 09:36:38.128968+00
2	1	66	168	\N	2026-01-21 09:36:38.128968+00	2026-01-21 09:36:38.128969+00
3	1	67	\N	No sé	2026-01-21 09:36:38.128969+00	2026-01-21 09:36:38.12897+00
4	1	68	171	\N	2026-01-21 09:36:38.12897+00	2026-01-21 09:36:38.128971+00
5	1	69	\N	es un numero que cambia proporcionalmente 	2026-01-21 09:36:38.128971+00	2026-01-21 09:36:38.128971+00
6	1	70	175	\N	2026-01-21 09:36:38.128972+00	2026-01-21 09:36:38.128972+00
7	2	65	\N	Un numero que no se puede expresar como multiplicacion de otros, en cambio compuesto si	2026-01-21 09:38:24.069861+00	2026-01-21 09:38:24.069866+00
8	2	66	168	\N	2026-01-21 09:38:24.069866+00	2026-01-21 09:38:24.069867+00
9	2	67	\N	a*a + b*b = c*c	2026-01-21 09:38:24.069867+00	2026-01-21 09:38:24.069868+00
10	2	68	171	\N	2026-01-21 09:38:24.069868+00	2026-01-21 09:38:24.069869+00
11	2	69	\N	es un numero que cambia proporcionalmente 	2026-01-21 09:38:24.069869+00	2026-01-21 09:38:24.06987+00
12	2	70	175	\N	2026-01-21 09:38:24.06987+00	2026-01-21 09:38:24.06987+00
13	3	65	\N	Un numero primo que no se puede expresar como multiplicacion de otros, en cambio compuesto si	2026-01-21 09:39:06.598758+00	2026-01-21 09:39:06.598763+00
14	3	66	168	\N	2026-01-21 09:39:06.598763+00	2026-01-21 09:39:06.598764+00
15	3	67	\N	a*a + b*b = c*c	2026-01-21 09:39:06.598764+00	2026-01-21 09:39:06.598765+00
16	3	68	171	\N	2026-01-21 09:39:06.598765+00	2026-01-21 09:39:06.598766+00
17	3	69	\N	es un numero que cambia proporcionalmente, con la relacion y = mx+b 	2026-01-21 09:39:06.598766+00	2026-01-21 09:39:06.598767+00
18	3	70	175	\N	2026-01-21 09:39:06.598767+00	2026-01-21 09:39:06.598768+00
\.


--
-- Data for Name: assessment; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.assessment (id, user_id, survey_id, started_at, finished_at, created_at, updated_at) FROM stdin;
1	1	12	2026-01-21 09:36:38.114089+00	\N	2026-01-21 09:36:38.114092+00	2026-01-21 09:36:38.114093+00
2	2	12	2026-01-21 09:38:24.055961+00	\N	2026-01-21 09:38:24.055965+00	2026-01-21 09:38:24.055966+00
3	3	12	2026-01-21 09:39:06.584885+00	\N	2026-01-21 09:39:06.584889+00	2026-01-21 09:39:06.584889+00
\.


--
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.feedback (id, assessment_id, summary_text, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: feedback_answer; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.feedback_answer (assessment_id, answer_id, feedback, score, created_at, updated_at, id) FROM stdin;
1	1	Es comprensible no saber la respuesta, pero sería útil intentar aprender sobre los números primos y compuestos. Te animo a investigar y practicar con ejemplos como 2 y 3 para primos, y 4 y 6 para compuestos.	0	2026-01-21 09:39:27.199405+00	2026-01-21 09:39:27.199409+00	1
1	3	Es comprensible no saber la respuesta, pero sería útil intentar explicar lo que se conoce sobre el teorema de Pitágoras. ¡No te desanimes, siempre hay oportunidad de aprender!	0	2026-01-21 09:39:27.19941+00	2026-01-21 09:39:27.199411+00	2
1	5	Has captado la idea de que una función implica un cambio, pero la explicación es muy básica y no aborda el concepto completo. Intenta incluir más detalles y un ejemplo específico para mejorar tu respuesta.	0.3	2026-01-21 09:39:27.199411+00	2026-01-21 09:39:27.199412+00	3
1	2	La suma de dos números se obtiene al agregar sus valores. En este caso, 7 + 5 = 12.	0	2026-01-21 09:39:27.199412+00	2026-01-21 09:39:27.199412+00	4
1	4	El área de un triángulo se calcula con la fórmula: Área = (base * altura) / 2. En este caso, (10 * 5) / 2 = 25 cm².	0	2026-01-21 09:39:27.199413+00	2026-01-21 09:39:27.199413+00	5
1	6	¡Respuesta correcta! Buen trabajo 🎉	1	2026-01-21 09:39:27.199414+00	2026-01-21 09:39:27.199414+00	6
2	7	Has captado la idea básica de los números primos y compuestos, pero la explicación es un poco confusa y falta de ejemplos claros. ¡Sigue practicando para mejorar la claridad y la precisión!	0.4	2026-01-21 09:39:39.075786+00	2026-01-21 09:39:39.075791+00	7
2	9	Has mencionado la fórmula del teorema de Pitágoras, lo cual es un buen comienzo. Sin embargo, sería útil incluir una explicación sobre cómo se aplica en problemas específicos de triángulos rectángulos para mejorar la respuesta.	0.4	2026-01-21 09:39:39.075791+00	2026-01-21 09:39:39.075792+00	8
2	11	Has captado la idea de que una función implica un cambio, pero la explicación es muy básica y no aborda el concepto completo. Intenta incluir más detalles y un ejemplo específico para mejorar tu respuesta.	0.3	2026-01-21 09:39:39.075792+00	2026-01-21 09:39:39.075793+00	9
2	8	La suma de dos números se obtiene al agregar sus valores. En este caso, 7 + 5 = 12.	0	2026-01-21 09:39:39.075793+00	2026-01-21 09:39:39.075794+00	10
2	10	El área de un triángulo se calcula con la fórmula: Área = (base * altura) / 2. En este caso, (10 * 5) / 2 = 25 cm².	0	2026-01-21 09:39:39.075794+00	2026-01-21 09:39:39.075794+00	11
2	12	¡Respuesta correcta! Buen trabajo 🎉	1	2026-01-21 09:39:39.075795+00	2026-01-21 09:39:39.075795+00	12
3	13	Has captado la idea básica de los números primos y compuestos, pero la explicación es un poco confusa y falta claridad. Sería genial que incluyeras ejemplos específicos para mejorar tu respuesta.	0.4	2026-01-21 09:39:48.929703+00	2026-01-21 09:39:48.929708+00	13
3	15	¡Buen intento al mencionar la fórmula del teorema de Pitágoras! Sin embargo, sería útil incluir una explicación sobre cómo se aplica en problemas específicos de triángulos rectángulos para mejorar la respuesta.	0.4	2026-01-21 09:39:48.929709+00	2026-01-21 09:39:48.929709+00	14
3	17	Has capturado la idea de que una función implica una relación proporcional, lo cual es un buen comienzo. Sin embargo, la explicación podría ser más clara y completa, y sería útil incluir un ejemplo específico de una función lineal.	0.5	2026-01-21 09:39:48.92971+00	2026-01-21 09:39:48.92971+00	15
3	14	La suma de dos números se obtiene al agregar sus valores. En este caso, 7 + 5 = 12.	0	2026-01-21 09:39:48.929711+00	2026-01-21 09:39:48.929711+00	16
3	16	El área de un triángulo se calcula con la fórmula: Área = (base * altura) / 2. En este caso, (10 * 5) / 2 = 25 cm².	0	2026-01-21 09:39:48.929712+00	2026-01-21 09:39:48.929712+00	17
3	18	¡Respuesta correcta! Buen trabajo 🎉	1	2026-01-21 09:39:48.929713+00	2026-01-21 09:39:48.929713+00	18
\.


--
-- Data for Name: option; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.option (id, question_id, text, is_correct, created_at, updated_at) FROM stdin;
141	54	Aventura	f	2026-01-21 09:28:50.695305+00	2026-01-21 09:28:50.695309+00
142	54	Deportes	f	2026-01-21 09:28:50.69531+00	2026-01-21 09:28:50.69531+00
143	54	Rol	t	2026-01-21 09:28:50.695311+00	2026-01-21 09:28:50.695311+00
144	54	Simulación	f	2026-01-21 09:28:50.695311+00	2026-01-21 09:28:50.695312+00
145	56	Spider-Man	f	2026-01-21 09:28:50.695312+00	2026-01-21 09:28:50.695313+00
146	56	Iron Man	t	2026-01-21 09:28:50.695313+00	2026-01-21 09:28:50.695314+00
147	56	The Dark Knight	f	2026-01-21 09:28:50.695314+00	2026-01-21 09:28:50.695315+00
148	56	Avengers	f	2026-01-21 09:28:50.695315+00	2026-01-21 09:28:50.695316+00
149	58	Friends	f	2026-01-21 09:28:50.695319+00	2026-01-21 09:28:50.69532+00
150	58	The Big Bang Theory	t	2026-01-21 09:28:50.69532+00	2026-01-21 09:28:50.695321+00
151	58	Game of Thrones	f	2026-01-21 09:28:50.695321+00	2026-01-21 09:28:50.695321+00
152	58	Breaking Bad	f	2026-01-21 09:28:50.695322+00	2026-01-21 09:28:50.695322+00
153	60	A) La Luna	f	2026-01-21 09:29:43.993526+00	2026-01-21 09:29:43.99353+00
154	60	B) El Sol	t	2026-01-21 09:29:43.993531+00	2026-01-21 09:29:43.993531+00
155	60	C) El viento	f	2026-01-21 09:29:43.993532+00	2026-01-21 09:29:43.993532+00
156	60	D) El agua	f	2026-01-21 09:29:43.993533+00	2026-01-21 09:29:43.993533+00
157	62	A) Ribosoma	f	2026-01-21 09:29:43.993534+00	2026-01-21 09:29:43.993534+00
158	62	B) Mitocondria	t	2026-01-21 09:29:43.993535+00	2026-01-21 09:29:43.993535+00
159	62	C) Lisosoma	f	2026-01-21 09:29:43.993536+00	2026-01-21 09:29:43.993536+00
160	62	D) Núcleo	f	2026-01-21 09:29:43.993537+00	2026-01-21 09:29:43.993537+00
161	64	A) Un tipo de evolución artificial	f	2026-01-21 09:29:43.993538+00	2026-01-21 09:29:43.993538+00
162	64	B) Un proceso de extinción	f	2026-01-21 09:29:43.993538+00	2026-01-21 09:29:43.993539+00
163	64	C) Un mecanismo de evolución	t	2026-01-21 09:29:43.993539+00	2026-01-21 09:29:43.99354+00
164	64	D) Un fenómeno meteorológico	f	2026-01-21 09:29:43.99354+00	2026-01-21 09:29:43.993541+00
165	66	10	f	2026-01-21 09:29:59.732898+00	2026-01-21 09:29:59.7329+00
166	66	11	f	2026-01-21 09:29:59.7329+00	2026-01-21 09:29:59.732901+00
167	66	12	t	2026-01-21 09:29:59.732901+00	2026-01-21 09:29:59.732902+00
168	66	13	f	2026-01-21 09:29:59.732902+00	2026-01-21 09:29:59.732903+00
169	68	20 cm²	f	2026-01-21 09:29:59.732903+00	2026-01-21 09:29:59.732904+00
170	68	25 cm²	t	2026-01-21 09:29:59.732904+00	2026-01-21 09:29:59.732904+00
171	68	30 cm²	f	2026-01-21 09:29:59.732905+00	2026-01-21 09:29:59.732905+00
172	68	35 cm²	f	2026-01-21 09:29:59.732906+00	2026-01-21 09:29:59.732906+00
173	70	-8	f	2026-01-21 09:29:59.732907+00	2026-01-21 09:29:59.732907+00
174	70	0	f	2026-01-21 09:29:59.732908+00	2026-01-21 09:29:59.732908+00
175	70	8	t	2026-01-21 09:29:59.732909+00	2026-01-21 09:29:59.732909+00
176	70	16	f	2026-01-21 09:29:59.73291+00	2026-01-21 09:29:59.73291+00
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.question (id, survey_id, description, question_type, created_at, updated_at, hint) FROM stdin;
53	10	Explica cómo la cultura geek ha influido en la industria del entretenimiento en las últimas décadas.	OPEN	2026-01-21 09:28:50.68186+00	2026-01-21 09:28:50.681864+00	\N
54	10	¿Cuál de los siguientes géneros de videojuegos es más popular entre los geeks?	CLOSED	2026-01-21 09:28:50.681864+00	2026-01-21 09:28:50.681865+00	Los géneros de videojuegos pueden variar, pero uno de los más populares es conocido por su narrativa y desarrollo de personajes.
55	10	Describe el impacto de las convenciones de cómics y cultura pop en la comunidad geek.	OPEN	2026-01-21 09:28:50.681865+00	2026-01-21 09:28:50.681866+00	\N
56	10	¿Qué película de superhéroes, estrenada en 2008, marcó un hito en la popularidad de la cultura geek?	CLOSED	2026-01-21 09:28:50.681866+00	2026-01-21 09:28:50.681867+00	Esta película es conocida por ser la primera de una exitosa franquicia de superhéroes.
57	10	Analiza la evolución de los cómics desde su creación hasta su papel actual en la cultura geek.	OPEN	2026-01-21 09:28:50.681867+00	2026-01-21 09:28:50.681868+00	\N
58	10	¿Cuál de las siguientes series de televisión es considerada un pilar de la cultura geek moderna?	CLOSED	2026-01-21 09:28:50.681868+00	2026-01-21 09:28:50.681869+00	Esta serie es famosa por su humor y referencias a la cultura pop, y ha ganado numerosos premios.
59	11	Explica el proceso del ciclo del agua y su importancia para los ecosistemas.	OPEN	2026-01-21 09:29:43.981096+00	2026-01-21 09:29:43.981098+00	\N
60	11	¿Cuál es la principal fuente de energía para la Tierra?	CLOSED	2026-01-21 09:29:43.981099+00	2026-01-21 09:29:43.9811+00	La respuesta correcta es el Sol, ya que es la fuente primaria de energía que impulsa la mayoría de los procesos en la Tierra.
61	11	Describe cómo se produce la energía en las células a través de la respiración celular.	OPEN	2026-01-21 09:29:43.9811+00	2026-01-21 09:29:43.981101+00	\N
62	11	¿Qué organelo celular es responsable de la producción de energía en las células eucariotas?	CLOSED	2026-01-21 09:29:43.981101+00	2026-01-21 09:29:43.981102+00	La respuesta correcta es la mitocondria, que es conocida como la 'central energética' de la célula.
63	11	Explica la teoría de la evolución de las especies y menciona un ejemplo que la respalde.	OPEN	2026-01-21 09:29:43.981102+00	2026-01-21 09:29:43.981103+00	\N
64	11	¿Qué es la selección natural?	CLOSED	2026-01-21 09:29:43.981103+00	2026-01-21 09:29:43.981104+00	La selección natural es un proceso por el cual los organismos mejor adaptados a su entorno tienen más probabilidades de sobrevivir y reproducirse.
65	12	Explica la diferencia entre un número primo y un número compuesto, proporcionando ejemplos de cada uno.	OPEN	2026-01-21 09:29:59.73136+00	2026-01-21 09:29:59.731361+00	\N
66	12	¿Cuál es el resultado de la suma de 7 y 5?	CLOSED	2026-01-21 09:29:59.731362+00	2026-01-21 09:29:59.731363+00	La suma de dos números se obtiene al agregar sus valores. En este caso, 7 + 5 = 12.
67	12	Describe cómo se utiliza el teorema de Pitágoras en la resolución de problemas de triángulos rectángulos.	OPEN	2026-01-21 09:29:59.731363+00	2026-01-21 09:29:59.731364+00	\N
68	12	¿Cuál es el área de un triángulo con base de 10 cm y altura de 5 cm?	CLOSED	2026-01-21 09:29:59.731364+00	2026-01-21 09:29:59.731365+00	El área de un triángulo se calcula con la fórmula: Área = (base * altura) / 2. En este caso, (10 * 5) / 2 = 25 cm².
69	12	Explica el concepto de función en matemáticas y proporciona un ejemplo de una función lineal.	OPEN	2026-01-21 09:29:59.731365+00	2026-01-21 09:29:59.731366+00	\N
70	12	¿Qué es el valor absoluto de -8?	CLOSED	2026-01-21 09:29:59.731367+00	2026-01-21 09:29:59.731367+00	El valor absoluto de un número es su distancia desde cero en la recta numérica, sin considerar la dirección. Por lo tanto, el valor absoluto de -8 es 8.
\.


--
-- Data for Name: survey; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.survey (id, topic, created_at, updated_at) FROM stdin;
9	animes populares	2026-01-21 09:22:02.777541+00	2026-01-21 09:22:02.777546+00
10	cultura geek	2026-01-21 09:28:50.67839+00	2026-01-21 09:28:50.678394+00
11	ciencia	2026-01-21 09:29:43.978636+00	2026-01-21 09:29:43.97864+00
12	matematicas	2026-01-21 09:29:59.729895+00	2026-01-21 09:29:59.7299+00
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public."user" (id, nickname, created_at, updated_at) FROM stdin;
1	maria	2026-01-21 09:06:15.66849+00	2026-01-21 09:06:15.668494+00
2	sofia	2026-01-21 09:06:20.710536+00	2026-01-21 09:06:20.71054+00
3	pedro	2026-01-21 09:06:25.207476+00	2026-01-21 09:06:25.207481+00
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.answer_id_seq', 18, true);


--
-- Name: assessment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.assessment_id_seq', 3, true);


--
-- Name: feedback_answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.feedback_answer_id_seq', 18, true);


--
-- Name: feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.feedback_id_seq', 1, false);


--
-- Name: option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.option_id_seq', 176, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.question_id_seq', 70, true);


--
-- Name: survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.survey_id_seq', 12, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.user_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: answer answer_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_pkey PRIMARY KEY (id);


--
-- Name: assessment assessment_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.assessment
    ADD CONSTRAINT assessment_pkey PRIMARY KEY (id);


--
-- Name: feedback_answer feedback_answer_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback_answer
    ADD CONSTRAINT feedback_answer_pkey PRIMARY KEY (id);


--
-- Name: feedback feedback_assessment_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_assessment_id_key UNIQUE (assessment_id);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- Name: option option_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.option
    ADD CONSTRAINT option_pkey PRIMARY KEY (id);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- Name: survey survey_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.survey
    ADD CONSTRAINT survey_pkey PRIMARY KEY (id);


--
-- Name: answer uq_answer_per_question; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT uq_answer_per_question UNIQUE (assessment_id, question_id);


--
-- Name: feedback_answer uq_feedback_answer; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback_answer
    ADD CONSTRAINT uq_feedback_answer UNIQUE (assessment_id, answer_id);


--
-- Name: assessment uq_user_survey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.assessment
    ADD CONSTRAINT uq_user_survey UNIQUE (user_id, survey_id);


--
-- Name: user user_nickname_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_nickname_key UNIQUE (nickname);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_answer_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_answer_id ON public.answer USING btree (id);


--
-- Name: ix_assessment_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_assessment_id ON public.assessment USING btree (id);


--
-- Name: ix_feedback_answer_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_feedback_answer_id ON public.feedback_answer USING btree (id);


--
-- Name: ix_feedback_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_feedback_id ON public.feedback USING btree (id);


--
-- Name: ix_option_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_option_id ON public.option USING btree (id);


--
-- Name: ix_question_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_question_id ON public.question USING btree (id);


--
-- Name: ix_survey_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_survey_id ON public.survey USING btree (id);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: answer answer_assessment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_assessment_id_fkey FOREIGN KEY (assessment_id) REFERENCES public.assessment(id);


--
-- Name: answer answer_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: answer answer_selected_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_selected_option_id_fkey FOREIGN KEY (selected_option_id) REFERENCES public.option(id);


--
-- Name: assessment assessment_survey_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.assessment
    ADD CONSTRAINT assessment_survey_id_fkey FOREIGN KEY (survey_id) REFERENCES public.survey(id);


--
-- Name: assessment assessment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.assessment
    ADD CONSTRAINT assessment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: feedback_answer feedback_answer_answer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback_answer
    ADD CONSTRAINT feedback_answer_answer_id_fkey FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: feedback_answer feedback_answer_assessment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback_answer
    ADD CONSTRAINT feedback_answer_assessment_id_fkey FOREIGN KEY (assessment_id) REFERENCES public.assessment(id);


--
-- Name: feedback feedback_assessment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_assessment_id_fkey FOREIGN KEY (assessment_id) REFERENCES public.assessment(id);


--
-- Name: option option_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.option
    ADD CONSTRAINT option_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question question_survey_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_survey_id_fkey FOREIGN KEY (survey_id) REFERENCES public.survey(id);


--
-- PostgreSQL database dump complete
--

\unrestrict ontHHgBfoNZZlEDXAfdpBc53mKawTSBN66lecfuFKkVu1yZXFwII7j36mcqKjrN

