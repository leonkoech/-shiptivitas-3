-- TYPE YOUR SQL QUERY BELOW

-- PART 1: Create a SQL query that maps out the daily average users before and after the feature change
-- Calculate daily average users before feature change
WITH user_activity_before_feature_change AS (
   SELECT 
        user_id, 
        COUNT(DISTINCT strftime('%Y-%m-%d', login_timestamp, 'unixepoch')) AS active_days_before_feature_change 
    FROM login_history 
    WHERE login_timestamp < strftime('%s', '2018-06-02') 
    GROUP BY user_id
)

, user_activity_after_feature_change AS (
    SELECT
        user_id,
        COUNT(DISTINCT strftime('%Y-%m-%d', login_timestamp, 'unixepoch')) AS active_days_after_feature_change
    FROM login_history
    WHERE login_timestamp >= strftime('%s', '2018-06-02')
    GROUP BY user_id
)

, daily_average_users AS (
    SELECT
        u.id AS user_id,
        COALESCE(active_days_before_feature_change, 0) AS active_days_before,
        COALESCE(active_days_after_feature_change, 0) AS active_days_after
    FROM user u
    LEFT JOIN user_activity_before_feature_change b ON u.id = b.user_id
    LEFT JOIN user_activity_after_feature_change a ON u.id = a.user_id
)

SELECT
    strftime('%Y-%m-%d', l.login_timestamp, 'unixepoch') AS date,
    AVG(d.active_days_before) AS avg_users_before,
    AVG(d.active_days_after) AS avg_users_after
FROM login_history l
JOIN daily_average_users d ON l.user_id = d.user_id
WHERE strftime('%Y-%m-%d', l.login_timestamp, 'unixepoch') IS NOT NULL
GROUP BY date;

-- PART 2: Create a SQL query that indicates the number of status changes by card

SELECT
    c.id AS cardID,
    c.name AS card_name,
    COUNT(*) AS status_changes_count
FROM
    card_change_history ch
JOIN
    card c ON ch.cardID = c.id
GROUP BY
    ch.cardID, c.name;
