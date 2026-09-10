WITH staging AS (
    SELECT * FROM {{ ref('stg_support_tickets') }}
)
SELECT 
    ticket_id,
    customer_id,
    account_tier,
    created_at,
    resolved_at,
    date_diff('hour', created_at, resolved_at) AS resolution_time_hours,
    CASE 
        WHEN date_diff('hour', created_at, resolved_at) > 24 THEN TRUE 
        ELSE FALSE 
    END AS is_sla_breached,
    ticket_subject,
    customer_feedback
FROM staging