============================================================================
-- Script: 01_snowsight_setup.sql
-- Description: Environment setup, DDL for raw tables, internal stage setup,
--              and data loading for Retail Pharmacy Vaccine CX Analytics.
-- ============================================================================

-- 1. Create Virtual Warehouse (if it does not exist)
CREATE WAREHOUSE IF NOT EXISTS PHARMACY_WH
    WITH 
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Virtual warehouse for pharmacy analytics workload';

USE WAREHOUSE PHARMACY_WH;

-- 2. Create Database and Schema Structure
CREATE DATABASE IF NOT EXISTS PHARMACY_DB;
CREATE SCHEMA IF NOT EXISTS PHARMACY_DB.ANALYTICS;

USE DATABASE PHARMACY_DB;
USE SCHEMA ANALYTICS;

-- 3. Create Raw Landing Table for Ingestion
CREATE OR REPLACE TABLE PHARMACY_DB.ANALYTICS.RAW_VACCINE_APPOINTMENTS (
    appointment_id    VARCHAR(50),
    patient_id        VARCHAR(50),
    store_id          VARCHAR(50),
    channel           VARCHAR(50),
    appointment_date  VARCHAR(50),
    reminder_sent     BOOLEAN,
    status            VARCHAR(20),
    survey_feedback   TEXT
);

-- 4. Create Internal File Stage for CSV Ingestion
CREATE OR REPLACE STAGE PHARMACY_DB.ANALYTICS.PHARMACY_CSV_STAGE
    FILE_FORMAT = (
        TYPE = 'CSV'
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        NULL_IF = ('NULL', 'null', '')
        EMPTY_FIELD_AS_NULL = TRUE
    )
    COMMENT = 'Internal stage for uploading synthetic vaccine survey CSVs';

-- ============================================================================
-- NOTE ON DATA LOADING:
-- Upload your 'raw_pharmacy_vaccine_data.csv' file into PHARMACY_CSV_STAGE 
-- using Snowsight (Data > Databases > PHARMACY_DB > ANALYTICS > Stages > Upload Files)
-- or via SnowSQL CLI (`PUT file://raw_pharmacy_vaccine_data.csv @PHARMACY_CSV_STAGE;`).
-- ============================================================================

-- 5. Copy Ingested Data from Internal Stage to Raw Landing Table
COPY INTO PHARMACY_DB.ANALYTICS.RAW_VACCINE_APPOINTMENTS
FROM @PHARMACY_DB.ANALYTICS.PHARMACY_CSV_STAGE/raw_pharmacy_vaccine_data.csv
FILE_FORMAT = (
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
)
ON_ERROR = 'CONTINUE';

-- 6. Verify Load Results
SELECT 
    COUNT(*) AS total_raw_records,
    COUNT(DISTINCT appointment_id) AS unique_appointments
FROM PHARMACY_DB.ANALYTICS.RAW_VACCINE_APPOINTMENTS;
