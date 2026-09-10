-- ============================================================================
-- Script: 03_fact_cortex_enrichment.sql
-- Description: Materializes enriched fact table using CTEs and native Snowflake
--              Cortex LLM functions for text classification & sentiment analysis.
-- ============================================================================

USE DATABASE PHARMACY_DB;
USE SCHEMA ANALYTICS;

-- Enriched Fact Table with Snowflake Cortex AI Integration
CREATE OR REPLACE TABLE PHARMACY_DB.ANALYTICS.FCT_VACCINE_ENRICHED AS
SELECT 
    appointment_id,
    patient_id,
    store_id,
    channel,
    appointment_datetime,
    appointment_date,
    reminder_sent,
    status,
    
    -- Operational Indicators
    CASE WHEN status = 'NO-SHOW' THEN TRUE ELSE FALSE END AS is_noshow,
    CASE WHEN channel = 'Pop-up Clinic' THEN TRUE ELSE FALSE END AS is_popup_clinic,
    
    survey_feedback,
    
    -- 1. Snowflake Cortex Sentiment Analysis (-1.0 to +1.0 scale)
    SNOWFLAKE.CORTEX.SENTIMENT(survey_feedback) AS feedback_sentiment_score,
    
    -- 2. Snowflake Cortex Zero-Shot Classification for Operational Bottlenecks
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        survey_feedback, 
        [
            'Lack of Reminder', 
            'Transportation Issue', 
            'Convenient Access', 
            'General Positive'
        ]
    ):label::STRING AS root_cause_category

FROM PHARMACY_DB.ANALYTICS.STG_VACCINE_APPOINTMENTS;

-- Verify Cortex AI Enrichments
SELECT 
    root_cause_category,
    COUNT(*) AS total_feedback_comments,
    ROUND(AVG(feedback_sentiment_score), 2) AS avg_sentiment_score,
    COUNT(CASE WHEN is_noshow THEN 1 END) AS noshow_count
FROM PHARMACY_DB.ANALYTICS.FCT_VACCINE_ENRICHED
GROUP BY 1
ORDER BY total_feedback_comments DESC;
