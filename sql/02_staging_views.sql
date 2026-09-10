-- ============================================================================
-- Script: 02_staging_views.sql
-- Description: Staging transformation view to clean data types, standardize
--              status flags, and handle nulls for vaccine survey analytics.
-- ============================================================================

USE DATABASE PHARMACY_DB;
USE SCHEMA ANALYTICS;

-- Staging View over Raw Landing Table
CREATE OR REPLACE VIEW PHARMACY_DB.ANALYTICS.STG_VACCINE_APPOINTMENTS AS
WITH raw_data AS (
    SELECT * FROM PHARMACY_DB.ANALYTICS.RAW_VACCINE_APPOINTMENTS
)
SELECT 
    -- Primary Keys & Identifiers
    TRIM(appointment_id)                           AS appointment_id,
    TRIM(patient_id)                               AS patient_id,
    TRIM(store_id)                                 AS store_id,
    TRIM(channel)                                  AS channel,
    
    -- Date and Time Conversions
    TRY_CAST(appointment_date AS TIMESTAMP_NTZ)    AS appointment_datetime,
    DATE(TRY_CAST(appointment_date AS TIMESTAMP_NTZ)) AS appointment_date,
    
    -- Status and Flags
    COALESCE(reminder_sent, FALSE)                  AS reminder_sent,
    UPPER(TRIM(status))                            AS status,
    
    -- Unstructured Feedback
    COALESCE(TRIM(survey_feedback), 'No feedback provided') AS survey_feedback

FROM raw_data;

-- Quick validation check
SELECT 
    status,
    COUNT(*) AS appointment_count,
    COUNT(CASE WHEN reminder_sent THEN 1 END) AS reminders_sent_count
FROM PHARMACY_DB.ANALYTICS.STG_VACCINE_APPOINTMENTS
GROUP BY 1;
