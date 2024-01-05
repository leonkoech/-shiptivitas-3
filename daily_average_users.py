import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('shiptivity.db')
cursor = conn.cursor()

sql_query = '''
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
'''

# Execute your SQL query to fetch the data
cursor.execute(sql_query)
result = cursor.fetchall()

# Print the result to check if the query is returning data
print(result)

# Extract data for plotting
dates = [row[0] for row in result]
avg_users_before = [row[1] for row in result]
avg_users_after = [row[2] for row in result]
# Plotting
plt.figure(figsize=(10, 6))

# Plot every nth date, e.g., every 7th date
n = 7
plt.plot(dates[::n], avg_users_before[::n], label='Before Feature Change', marker='o')
plt.plot(dates[::n], avg_users_after[::n], label='After Feature Change', marker='o')

plt.xlabel('Date')
plt.ylabel('Average Users')
plt.title('Daily Average Users Before and After Feature Change')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.tight_layout()

# Save the plot as an image
plt.savefig('daily_average_users.png')

# Show the plot (optional)
plt.show()

# Close the database connection
conn.close()
