DROP TABLE IF EXISTS mart.support_efficiency_mart;
CREATE TABLE mart.support_efficiency_mart AS
WITH ticket_data AS (
    SELECT
        DATE(created_at) AS created_date,
        TO_CHAR(created_at, 'YYYY-MM') AS created_month,
        issue_type,
        COUNT(ticket_id) AS total_tickets,
        COUNT(*) FILTER (WHERE status = 'open') AS open_tickets,
        COUNT(*) FILTER (WHERE status = 'pending') AS pending_tickets,
        COUNT(*) FILTER (WHERE status = 'closed') AS closed_tickets,
        ROUND(AVG(EXTRACT(EPOCH FROM (updated_at - created_at)) / 60)
              FILTER (WHERE status = 'closed'), 2) AS avg_resolution_time_minutes
    FROM source.support_tickets
    GROUP BY DATE(created_at), TO_CHAR(created_at, 'YYYY-MM'), issue_type
)
SELECT
    created_date,
    created_month,
    issue_type,
    total_tickets,
    open_tickets,
    pending_tickets,
    closed_tickets,
    avg_resolution_time_minutes,
    SUM(total_tickets) OVER(PARTITION BY created_month, issue_type) AS monthly_total_tickets,
    SUM(open_tickets) OVER(PARTITION BY created_month, issue_type) AS monthly_open_tickets,
    SUM(pending_tickets) OVER(PARTITION BY created_month, issue_type) AS monthly_pending_tickets,
    SUM(closed_tickets) OVER(PARTITION BY created_month, issue_type) AS monthly_closed_tickets
FROM ticket_data
ORDER BY created_date;

-- Создание индексов для ускорения поиска по дате и типу обращения
CREATE INDEX idx_support_efficiency_created_date ON mart.support_efficiency_mart (created_date);
CREATE INDEX idx_support_efficiency_created_month ON mart.support_efficiency_mart (created_month);
CREATE INDEX idx_support_efficiency_issue_type ON mart.support_efficiency_mart (issue_type);






