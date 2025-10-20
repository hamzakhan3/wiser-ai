--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Homebrew)
-- Dumped by pg_dump version 17.5 (Homebrew)

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
-- Name: anomalies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.anomalies (
    id integer NOT NULL,
    machine_id character varying(255) NOT NULL,
    sensor_type character varying(100) NOT NULL,
    start_timestamp timestamp without time zone NOT NULL,
    end_timestamp timestamp without time zone NOT NULL,
    severity numeric(10,6) NOT NULL,
    anomaly_type character varying(100),
    description text,
    run_id uuid,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    mac_id character varying(255)
);


--
-- Name: TABLE anomalies; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.anomalies IS 'Stores detected anomalies with severity scores and time ranges';


--
-- Name: COLUMN anomalies.mac_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anomalies.mac_id IS 'MAC address of the sensor device';


--
-- Name: anomalies_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.anomalies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: anomalies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.anomalies_id_seq OWNED BY public.anomalies.id;


--
-- Name: anomaly_detections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.anomaly_detections (
    id integer NOT NULL,
    machine_id character varying(255) NOT NULL,
    sensor_type character varying(100) NOT NULL,
    detection_timestamp timestamp without time zone NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    severity numeric(10,6) NOT NULL,
    confidence numeric(5,4),
    anomaly_category character varying(100),
    description text,
    model_used character varying(100),
    parameters jsonb,
    run_id uuid,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    mac_id character varying(255)
);


--
-- Name: TABLE anomaly_detections; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.anomaly_detections IS 'Comprehensive anomaly detection results with model metadata';


--
-- Name: COLUMN anomaly_detections.mac_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.anomaly_detections.mac_id IS 'MAC address of the sensor device';


--
-- Name: anomaly_detections_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.anomaly_detections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: anomaly_detections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.anomaly_detections_id_seq OWNED BY public.anomaly_detections.id;


--
-- Name: critical_health_machine; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.critical_health_machine (
    id uuid NOT NULL,
    machine_id uuid NOT NULL,
    machine_name text NOT NULL,
    severity_level text NOT NULL,
    last_anomaly timestamp without time zone,
    sensor_type text NOT NULL
);


--
-- Name: current_sensor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.current_sensor (
    current_sensor_id uuid DEFAULT gen_random_uuid() NOT NULL,
    node_id uuid NOT NULL,
    status text,
    phase text,
    threshold_current_min double precision,
    threshold_current_max double precision,
    rating double precision,
    scaler double precision,
    fault_threshold double precision
);


--
-- Name: database_conn; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.database_conn (
    id integer NOT NULL,
    databasetype character varying(50) NOT NULL,
    url text NOT NULL
);


--
-- Name: database_conn_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.database_conn_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: database_conn_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.database_conn_id_seq OWNED BY public.database_conn.id;


--
-- Name: humidity_sensor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.humidity_sensor (
    humidity_sensor_id uuid DEFAULT gen_random_uuid() NOT NULL,
    node_id uuid NOT NULL,
    status text,
    phase text,
    humidity_threshold_min double precision,
    humidity_threshold_max double precision
);


--
-- Name: inference_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inference_data (
    id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    value double precision NOT NULL,
    run_id uuid NOT NULL,
    machine_id uuid NOT NULL,
    sensor_type character varying(50) NOT NULL
);


--
-- Name: inference_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inference_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inference_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inference_data_id_seq OWNED BY public.inference_data.id;


--
-- Name: inference_data_multi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inference_data_multi (
    id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    value1 double precision NOT NULL,
    value2 double precision NOT NULL,
    value3 double precision NOT NULL,
    run_id uuid NOT NULL,
    machine_id uuid NOT NULL,
    sensor_type character varying(50) NOT NULL
);


--
-- Name: inference_data_multi_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inference_data_multi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inference_data_multi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inference_data_multi_id_seq OWNED BY public.inference_data_multi.id;


--
-- Name: lab; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lab (
    lab_id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    description text,
    image text,
    start_time time without time zone,
    end_time time without time zone,
    location text,
    duration interval,
    days text[],
    contact text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: lab_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lab_user (
    lab_id uuid NOT NULL,
    user_id uuid NOT NULL,
    role text DEFAULT 'member'::text,
    assigned_at timestamp with time zone DEFAULT now()
);


--
-- Name: machine; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine (
    machine_id uuid DEFAULT gen_random_uuid() NOT NULL,
    lab_id uuid NOT NULL,
    name text NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT now(),
    created_by uuid,
    updated_at timestamp with time zone DEFAULT now(),
    updated_by uuid,
    image_url text
);


--
-- Name: machine_anomaly_screenshots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_anomaly_screenshots (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid NOT NULL,
    sensor_type character varying(50) DEFAULT 'Vibration'::character varying NOT NULL,
    screenshot_data bytea,
    screenshot_url text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    analysis_id integer,
    chart_title character varying(255)
);


--
-- Name: TABLE machine_anomaly_screenshots; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.machine_anomaly_screenshots IS 'Stores automatic screenshots of anomaly inspection page graphs for AI vision analysis';


--
-- Name: COLUMN machine_anomaly_screenshots.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.id IS 'Primary key UUID';


--
-- Name: COLUMN machine_anomaly_screenshots.machine_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.machine_id IS 'Foreign key to machine table';


--
-- Name: COLUMN machine_anomaly_screenshots.sensor_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.sensor_type IS 'Type of sensor data (Vibration, Temperature, Humidity, etc.)';


--
-- Name: COLUMN machine_anomaly_screenshots.screenshot_data; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.screenshot_data IS 'Binary image data of the captured screenshot';


--
-- Name: COLUMN machine_anomaly_screenshots.screenshot_url; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.screenshot_url IS 'Optional file path reference for the screenshot';


--
-- Name: COLUMN machine_anomaly_screenshots.created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.created_at IS 'Timestamp when screenshot was captured';


--
-- Name: COLUMN machine_anomaly_screenshots.updated_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.updated_at IS 'Timestamp when record was last updated';


--
-- Name: COLUMN machine_anomaly_screenshots.analysis_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.machine_anomaly_screenshots.analysis_id IS 'Foreign key to machine_vision_analysis table linking the AI analysis';


--
-- Name: machine_current_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_current_log (
    mac text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    ct1 double precision,
    ct2 double precision,
    ct3 double precision,
    ct_avg double precision,
    total_current double precision,
    state text,
    state_duration integer,
    fault_status text,
    fw_version text,
    machineid uuid,
    hi text
);


--
-- Name: machine_energy_consumption; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_energy_consumption (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid,
    machine_name character varying(255) NOT NULL,
    energy_consumption_kwh numeric(10,2) NOT NULL,
    power_consumption_watts numeric(10,2),
    measurement_date date NOT NULL,
    measurement_period character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT machine_energy_consumption_measurement_period_check CHECK (((measurement_period)::text = ANY ((ARRAY['daily'::character varying, 'weekly'::character varying, 'monthly'::character varying])::text[])))
);


--
-- Name: machine_issue_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_issue_history (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid NOT NULL,
    machine_name character varying(255) NOT NULL,
    issue_description text NOT NULL,
    issue_type character varying(100) NOT NULL,
    severity_level character varying(20) NOT NULL,
    reported_by character varying(255),
    reported_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    resolved_at timestamp without time zone,
    resolution_description text,
    resolution_steps text[],
    parts_used text[],
    downtime_hours numeric(5,2),
    cost_of_repair numeric(10,2),
    technician_name character varying(255),
    status character varying(20) DEFAULT 'open'::character varying
);


--
-- Name: machine_parts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_parts (
    part_id bigint NOT NULL,
    machine_id uuid NOT NULL,
    part_name character varying(255) NOT NULL,
    part_number character varying(100),
    last_replaced_date date,
    next_maintenance_date date,
    notes text
);


--
-- Name: machine_parts_inventory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_parts_inventory (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid NOT NULL,
    machine_name character varying(255) NOT NULL,
    part_name character varying(255) NOT NULL,
    part_number character varying(100),
    current_stock integer DEFAULT 0,
    minimum_stock integer DEFAULT 1,
    maximum_stock integer DEFAULT 10,
    unit_cost numeric(10,2),
    supplier character varying(255),
    lead_time_days integer,
    is_critical boolean DEFAULT false,
    last_ordered timestamp without time zone,
    last_used timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: machine_parts_part_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.machine_parts ALTER COLUMN part_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.machine_parts_part_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: machine_performance_benchmarks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_performance_benchmarks (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid NOT NULL,
    machine_name character varying(255) NOT NULL,
    parameter_name character varying(100) NOT NULL,
    normal_min_value numeric(10,3),
    normal_max_value numeric(10,3),
    warning_min_value numeric(10,3),
    warning_max_value numeric(10,3),
    critical_min_value numeric(10,3),
    critical_max_value numeric(10,3),
    unit character varying(20),
    measurement_frequency_minutes integer DEFAULT 5,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: machine_troubleshooting; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_troubleshooting (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid NOT NULL,
    machine_name character varying(255) NOT NULL,
    issue_type character varying(100) NOT NULL,
    severity_level character varying(20) NOT NULL,
    symptoms text NOT NULL,
    possible_causes text[] NOT NULL,
    recommended_actions text[] NOT NULL,
    estimated_downtime_hours integer,
    required_parts text[],
    required_skills text[],
    priority_level integer DEFAULT 1,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: machine_vision_analysis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_vision_analysis (
    id integer NOT NULL,
    machine_id uuid NOT NULL,
    image_path text NOT NULL,
    analysis_text text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    sensor_type character varying(50)
);


--
-- Name: machine_vision_analysis_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.machine_vision_analysis_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: machine_vision_analysis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.machine_vision_analysis_id_seq OWNED BY public.machine_vision_analysis.id;


--
-- Name: maintenance_procedures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.maintenance_procedures (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid NOT NULL,
    machine_name character varying(255) NOT NULL,
    procedure_name character varying(255) NOT NULL,
    procedure_type character varying(100) NOT NULL,
    description text NOT NULL,
    steps jsonb NOT NULL,
    estimated_duration_minutes integer,
    required_tools text[],
    required_parts text[],
    safety_requirements text[],
    skill_level_required character varying(20),
    frequency_days integer,
    last_performed timestamp without time zone,
    next_due timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: maintenance_task; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.maintenance_task (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid NOT NULL,
    machine_name character varying(100) NOT NULL,
    task_type character varying(100) NOT NULL,
    description text,
    scheduled_date date NOT NULL,
    duration integer NOT NULL,
    priority character varying(20),
    status character varying(20),
    assigned_technician character varying(100),
    CONSTRAINT maintenancetasks_priority_check CHECK (((priority)::text = ANY ((ARRAY['low'::character varying, 'medium'::character varying, 'high'::character varying])::text[]))),
    CONSTRAINT maintenancetasks_status_check CHECK (((status)::text = ANY ((ARRAY['scheduled'::character varying, 'Scheduled'::character varying, 'in_progress'::character varying, 'completed'::character varying, 'cancelled'::character varying])::text[])))
);


--
-- Name: node; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.node (
    node_id uuid DEFAULT gen_random_uuid() NOT NULL,
    machine_id uuid,
    mac_address text NOT NULL,
    status text,
    tags text[],
    last_seen timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    created_by text,
    node_type text,
    reporting_interval interval
);


--
-- Name: shift_machine_production; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shift_machine_production (
    machine_id uuid NOT NULL,
    machine_name character varying(255) NOT NULL,
    production_date date NOT NULL,
    shift character varying(50) NOT NULL,
    units_produced integer DEFAULT 0,
    downtime_minutes integer DEFAULT 0,
    uptime_percentage double precision,
    efficiency_percentage double precision,
    notes text
);


--
-- Name: temperature_sensor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.temperature_sensor (
    temperature_sensor_id uuid DEFAULT gen_random_uuid() NOT NULL,
    node_id uuid NOT NULL,
    status text,
    temperature_threshold_min double precision,
    temperature_threshold_max double precision
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    user_email text NOT NULL,
    password text NOT NULL,
    v text,
    token text,
    user_type text,
    super_user boolean DEFAULT false,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    is_validated boolean DEFAULT false,
    created_by uuid,
    CONSTRAINT users_user_type_check CHECK ((user_type = ANY (ARRAY['admin'::text, 'standard'::text, 'guest'::text])))
);


--
-- Name: vibration_inference_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vibration_inference_data (
    _id integer NOT NULL,
    machine_id uuid NOT NULL,
    vibration double precision NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    __v integer DEFAULT 0,
    rssi integer
);


--
-- Name: vibration_inference_data__id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vibration_inference_data__id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vibration_inference_data__id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vibration_inference_data__id_seq OWNED BY public.vibration_inference_data._id;


--
-- Name: work_orders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.work_orders (
    id uuid NOT NULL,
    page_no integer,
    priority integer,
    company_name character varying,
    work_order_no character varying,
    week_no integer,
    week_of date,
    equipment_id character varying,
    equipment_description text,
    category character varying,
    building character varying,
    floor character varying,
    room character varying,
    location_description text,
    emergency_contact character varying,
    special_instructions text,
    shop_vendor character varying,
    department_name character varying,
    employee_name character varying,
    task_no character varying,
    work_description text,
    frequency character varying,
    work_performed_by character varying,
    completion_date date,
    standard_hours numeric(5,2),
    overtime_hours numeric(5,2),
    machine_id uuid,
    part_numbers jsonb,
    materials_used jsonb
);


--
-- Name: anomalies id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomalies ALTER COLUMN id SET DEFAULT nextval('public.anomalies_id_seq'::regclass);


--
-- Name: anomaly_detections id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomaly_detections ALTER COLUMN id SET DEFAULT nextval('public.anomaly_detections_id_seq'::regclass);


--
-- Name: database_conn id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.database_conn ALTER COLUMN id SET DEFAULT nextval('public.database_conn_id_seq'::regclass);


--
-- Name: inference_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inference_data ALTER COLUMN id SET DEFAULT nextval('public.inference_data_id_seq'::regclass);


--
-- Name: inference_data_multi id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inference_data_multi ALTER COLUMN id SET DEFAULT nextval('public.inference_data_multi_id_seq'::regclass);


--
-- Name: machine_vision_analysis id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_vision_analysis ALTER COLUMN id SET DEFAULT nextval('public.machine_vision_analysis_id_seq'::regclass);


--
-- Name: vibration_inference_data _id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vibration_inference_data ALTER COLUMN _id SET DEFAULT nextval('public.vibration_inference_data__id_seq'::regclass);


--
-- Name: anomalies anomalies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomalies
    ADD CONSTRAINT anomalies_pkey PRIMARY KEY (id);


--
-- Name: anomaly_detections anomaly_detections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomaly_detections
    ADD CONSTRAINT anomaly_detections_pkey PRIMARY KEY (id);


--
-- Name: critical_health_machine critical_health_machine_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.critical_health_machine
    ADD CONSTRAINT critical_health_machine_pkey PRIMARY KEY (id);


--
-- Name: current_sensor current_sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.current_sensor
    ADD CONSTRAINT current_sensor_pkey PRIMARY KEY (current_sensor_id);


--
-- Name: database_conn database_conn_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.database_conn
    ADD CONSTRAINT database_conn_pkey PRIMARY KEY (id);


--
-- Name: humidity_sensor humidity_sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.humidity_sensor
    ADD CONSTRAINT humidity_sensor_pkey PRIMARY KEY (humidity_sensor_id);


--
-- Name: inference_data_multi inference_data_multi_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inference_data_multi
    ADD CONSTRAINT inference_data_multi_pkey PRIMARY KEY (id);


--
-- Name: inference_data inference_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inference_data
    ADD CONSTRAINT inference_data_pkey PRIMARY KEY (id);


--
-- Name: lab lab_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lab
    ADD CONSTRAINT lab_pkey PRIMARY KEY (lab_id);


--
-- Name: lab_user lab_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lab_user
    ADD CONSTRAINT lab_user_pkey PRIMARY KEY (lab_id, user_id);


--
-- Name: machine_anomaly_screenshots machine_anomaly_screenshots_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_anomaly_screenshots
    ADD CONSTRAINT machine_anomaly_screenshots_pkey PRIMARY KEY (id);


--
-- Name: machine_current_log machine_current_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_current_log
    ADD CONSTRAINT machine_current_log_pkey PRIMARY KEY (mac, created_at);


--
-- Name: machine_energy_consumption machine_energy_consumption_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_energy_consumption
    ADD CONSTRAINT machine_energy_consumption_pkey PRIMARY KEY (id);


--
-- Name: machine_issue_history machine_issue_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_issue_history
    ADD CONSTRAINT machine_issue_history_pkey PRIMARY KEY (id);


--
-- Name: machine_parts_inventory machine_parts_inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_parts_inventory
    ADD CONSTRAINT machine_parts_inventory_pkey PRIMARY KEY (id);


--
-- Name: machine_parts machine_parts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_parts
    ADD CONSTRAINT machine_parts_pkey PRIMARY KEY (part_id);


--
-- Name: machine_performance_benchmarks machine_performance_benchmarks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_performance_benchmarks
    ADD CONSTRAINT machine_performance_benchmarks_pkey PRIMARY KEY (id);


--
-- Name: machine machine_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine
    ADD CONSTRAINT machine_pkey PRIMARY KEY (machine_id);


--
-- Name: machine_troubleshooting machine_troubleshooting_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_troubleshooting
    ADD CONSTRAINT machine_troubleshooting_pkey PRIMARY KEY (id);


--
-- Name: machine_vision_analysis machine_vision_analysis_machine_id_image_path_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_vision_analysis
    ADD CONSTRAINT machine_vision_analysis_machine_id_image_path_key UNIQUE (machine_id, image_path);


--
-- Name: machine_vision_analysis machine_vision_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_vision_analysis
    ADD CONSTRAINT machine_vision_analysis_pkey PRIMARY KEY (id);


--
-- Name: maintenance_procedures maintenance_procedures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_procedures
    ADD CONSTRAINT maintenance_procedures_pkey PRIMARY KEY (id);


--
-- Name: maintenance_task maintenancetasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT maintenancetasks_pkey PRIMARY KEY (id);


--
-- Name: node node_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.node
    ADD CONSTRAINT node_pkey PRIMARY KEY (node_id);


--
-- Name: shift_machine_production pk_shift_machine_production; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shift_machine_production
    ADD CONSTRAINT pk_shift_machine_production PRIMARY KEY (machine_id, production_date, shift);


--
-- Name: temperature_sensor temperature_sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.temperature_sensor
    ADD CONSTRAINT temperature_sensor_pkey PRIMARY KEY (temperature_sensor_id);


--
-- Name: machine_anomaly_screenshots unique_machine_sensor_screenshot; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_anomaly_screenshots
    ADD CONSTRAINT unique_machine_sensor_screenshot UNIQUE (machine_id, sensor_type);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_user_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_email_key UNIQUE (user_email);


--
-- Name: vibration_inference_data vibration_inference_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vibration_inference_data
    ADD CONSTRAINT vibration_inference_data_pkey PRIMARY KEY (_id);


--
-- Name: work_orders work_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.work_orders
    ADD CONSTRAINT work_orders_pkey PRIMARY KEY (id);


--
-- Name: idx_anomalies_mac_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomalies_mac_id ON public.anomalies USING btree (mac_id);


--
-- Name: idx_anomalies_machine_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomalies_machine_id ON public.anomalies USING btree (machine_id);


--
-- Name: idx_anomalies_run_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomalies_run_id ON public.anomalies USING btree (run_id);


--
-- Name: idx_anomalies_timestamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomalies_timestamp ON public.anomalies USING btree (start_timestamp, end_timestamp);


--
-- Name: idx_anomaly_detections_mac_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomaly_detections_mac_id ON public.anomaly_detections USING btree (mac_id);


--
-- Name: idx_anomaly_detections_machine_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomaly_detections_machine_id ON public.anomaly_detections USING btree (machine_id);


--
-- Name: idx_anomaly_detections_run_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomaly_detections_run_id ON public.anomaly_detections USING btree (run_id);


--
-- Name: idx_anomaly_detections_timestamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_anomaly_detections_timestamp ON public.anomaly_detections USING btree (detection_timestamp);


--
-- Name: idx_benchmarks_machine; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_benchmarks_machine ON public.machine_performance_benchmarks USING btree (machine_id, parameter_name);


--
-- Name: idx_energy_machine_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_energy_machine_date ON public.machine_energy_consumption USING btree (machine_id, measurement_date);


--
-- Name: idx_energy_period; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_energy_period ON public.machine_energy_consumption USING btree (measurement_period);


--
-- Name: idx_issues_machine; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_issues_machine ON public.machine_issue_history USING btree (machine_id, status);


--
-- Name: idx_machine_anomaly_screenshots_analysis_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_machine_anomaly_screenshots_analysis_id ON public.machine_anomaly_screenshots USING btree (analysis_id);


--
-- Name: idx_machine_anomaly_screenshots_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_machine_anomaly_screenshots_created_at ON public.machine_anomaly_screenshots USING btree (created_at);


--
-- Name: idx_machine_anomaly_screenshots_machine_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_machine_anomaly_screenshots_machine_id ON public.machine_anomaly_screenshots USING btree (machine_id);


--
-- Name: idx_machine_anomaly_screenshots_sensor_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_machine_anomaly_screenshots_sensor_type ON public.machine_anomaly_screenshots USING btree (sensor_type);


--
-- Name: idx_machine_vision_analysis_image_path; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_machine_vision_analysis_image_path ON public.machine_vision_analysis USING btree (image_path);


--
-- Name: idx_machine_vision_analysis_machine_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_machine_vision_analysis_machine_id ON public.machine_vision_analysis USING btree (machine_id);


--
-- Name: idx_parts_machine; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_parts_machine ON public.machine_parts_inventory USING btree (machine_id, is_critical);


--
-- Name: idx_procedures_machine; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_procedures_machine ON public.maintenance_procedures USING btree (machine_id, procedure_type);


--
-- Name: idx_troubleshooting_machine; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_troubleshooting_machine ON public.machine_troubleshooting USING btree (machine_id, issue_type);


--
-- Name: machine_current_log_created_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX machine_current_log_created_at_idx ON public.machine_current_log USING btree (created_at DESC);


--
-- Name: machine_anomaly_screenshots trigger_update_machine_anomaly_screenshots_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_update_machine_anomaly_screenshots_updated_at BEFORE UPDATE ON public.machine_anomaly_screenshots FOR EACH ROW EXECUTE FUNCTION public.update_machine_anomaly_screenshots_updated_at();


--
-- Name: machine_current_log ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.machine_current_log FOR EACH ROW EXECUTE FUNCTION _timescaledb_functions.insert_blocker();


--
-- Name: critical_health_machine critical_health_machine_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.critical_health_machine
    ADD CONSTRAINT critical_health_machine_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id);


--
-- Name: current_sensor current_sensor_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.current_sensor
    ADD CONSTRAINT current_sensor_node_id_fkey FOREIGN KEY (node_id) REFERENCES public.node(node_id) ON DELETE CASCADE;


--
-- Name: inference_data fk_machine; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inference_data
    ADD CONSTRAINT fk_machine FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id);


--
-- Name: maintenance_task fk_machine; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT fk_machine FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id) ON DELETE CASCADE;


--
-- Name: vibration_inference_data fk_machine_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vibration_inference_data
    ADD CONSTRAINT fk_machine_1 FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id) ON DELETE CASCADE;


--
-- Name: machine_anomaly_screenshots fk_machine_anomaly_screenshots_analysis_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_anomaly_screenshots
    ADD CONSTRAINT fk_machine_anomaly_screenshots_analysis_id FOREIGN KEY (analysis_id) REFERENCES public.machine_vision_analysis(id) ON DELETE SET NULL;


--
-- Name: machine_anomaly_screenshots fk_machine_anomaly_screenshots_machine_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_anomaly_screenshots
    ADD CONSTRAINT fk_machine_anomaly_screenshots_machine_id FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id) ON DELETE CASCADE;


--
-- Name: inference_data_multi fk_machine_multi; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inference_data_multi
    ADD CONSTRAINT fk_machine_multi FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id);


--
-- Name: shift_machine_production fk_shift_machine_production_machine; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shift_machine_production
    ADD CONSTRAINT fk_shift_machine_production_machine FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: humidity_sensor humidity_sensor_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.humidity_sensor
    ADD CONSTRAINT humidity_sensor_node_id_fkey FOREIGN KEY (node_id) REFERENCES public.node(node_id) ON DELETE CASCADE;


--
-- Name: lab_user lab_user_lab_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lab_user
    ADD CONSTRAINT lab_user_lab_id_fkey FOREIGN KEY (lab_id) REFERENCES public.lab(lab_id) ON DELETE CASCADE;


--
-- Name: lab_user lab_user_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lab_user
    ADD CONSTRAINT lab_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: machine machine_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine
    ADD CONSTRAINT machine_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: machine_energy_consumption machine_energy_consumption_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_energy_consumption
    ADD CONSTRAINT machine_energy_consumption_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id);


--
-- Name: machine machine_lab_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine
    ADD CONSTRAINT machine_lab_id_fkey FOREIGN KEY (lab_id) REFERENCES public.lab(lab_id) ON DELETE CASCADE;


--
-- Name: machine_parts machine_parts_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_parts
    ADD CONSTRAINT machine_parts_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id) ON DELETE CASCADE;


--
-- Name: machine machine_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine
    ADD CONSTRAINT machine_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(id);


--
-- Name: node node_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.node
    ADD CONSTRAINT node_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(machine_id) ON DELETE CASCADE;


--
-- Name: temperature_sensor temperature_sensor_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.temperature_sensor
    ADD CONSTRAINT temperature_sensor_node_id_fkey FOREIGN KEY (node_id) REFERENCES public.node(node_id) ON DELETE CASCADE;


--
-- Name: users users_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

