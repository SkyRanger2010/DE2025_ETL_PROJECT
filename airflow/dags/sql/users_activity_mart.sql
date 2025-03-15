DROP TABLE IF EXISTS mart.user_activity_mart;
CREATE TABLE mart.user_activity_mart AS
SELECT
    s.user_id,
    COUNT(s.session_id) AS total_sessions,
    TO_CHAR(MIN(s.start_time), 'DD-MM-YYYY HH24:MI') AS first_session_start_time,
    TO_CHAR(MAX(s.end_time), 'DD-MM-YYYY HH24:MI') AS last_session_end_time,
    ROUND(AVG(EXTRACT(EPOCH FROM (s.end_time - s.start_time)) / 60),2) AS avg_session_duration_minutes,
    ROUND(SUM(EXTRACT(EPOCH FROM (s.end_time - s.start_time)) / 60), 2) AS total_session_duration_minutes,
    COUNT(DISTINCT q.query_id) AS search_queries_count,
    COUNT(DISTINCT t.ticket_id) AS support_tickets_count,
    COUNT(DISTINCT ur.recommended_product) AS recommended_products_count
FROM source.user_sessions s
LEFT JOIN source.search_queries q ON s.user_id = q.user_id
LEFT JOIN source.support_tickets t ON s.user_id = t.user_id
LEFT JOIN source.user_recommendations ur ON s.user_id = ur.user_id
GROUP BY s.user_id;

-- Создание индекса для ускорения поиска по user_id
CREATE INDEX idx_user_activity_mart_user_id ON mart.user_activity_mart (user_id);

