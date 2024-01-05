import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Connect to SQLite database
conn = sqlite3.connect('shiptivity.db')
cursor = conn.cursor()

# Your SQL query
sql_query = '''
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
'''

# Execute your SQL query to fetch the data
cursor.execute(sql_query)
result = cursor.fetchall()

# Extract data for plotting
card_names = [row[1] for row in result]
status_changes_count = [row[2] for row in result]

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)

# Function to update the graph for animation
def update(frame):
    ax.clear()
    start_index = frame
    end_index = start_index + 20
    plt.bar(card_names[start_index:end_index], status_changes_count[start_index:end_index], color='skyblue')
    plt.xlabel('Card')
    plt.ylabel('Number of Status Changes')
    plt.title('Number of Status Changes by Card')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.6)

# Animate the graph
animation = FuncAnimation(fig, update, frames=len(card_names)-20, interval=500)

# Save the animation as a GIF using Pillow
animation.save('status_changes_by_card_scrollable.gif', writer='pillow', fps=2)

# Show the plot (optional)
plt.show()

# Close the database connection
conn.close()
