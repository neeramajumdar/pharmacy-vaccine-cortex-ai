
  
  create view "ticket_analytics"."main"."stg_support_tickets__dbt_tmp" as (
    WITH raw_data AS (
    SELECT * FROM read_csv_auto('C:/Users/neera/support_ticket_pipeline/raw_support_tickets.csv')
)
SELECT 
    ticket_id,
    customer_id,
    account_tier,
    CAST(created_at AS TIMESTAMP) AS created_at,
    CAST(resolved_at AS TIMESTAMP) AS resolved_at,
    ticket_subject,
    customer_feedback
FROM raw_data
  );
