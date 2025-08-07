import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("D:/ml_project.db")  # Update path if needed
cursor = conn.cursor()

# Define red flag rules
risky_countries = ['Panama', 'Cayman Islands', 'British Virgin Islands']
high_risk_amount = 10000

# Fetch risky client IDs
cursor.execute("""
    SELECT client_id FROM clients
    WHERE risk_profile = 'High'
    OR pep_status = 'Yes'
    OR offshore = 'Yes'
""")
risky_client_ids = [row[0] for row in cursor.fetchall()]

# Fetch all transactions
cursor.execute("SELECT transaction_id, client_id, amount, country FROM transactions")
transactions = cursor.fetchall()

# Clear previous flags
cursor.execute("UPDATE transactions SET suspicious = 'No', red_flag_reason = NULL")

# Process transactions
for txn_id, client_id, amount, country in transactions:
    reasons = []

    if client_id in risky_client_ids:
        reasons.append("Client Risk")

    if country in risky_countries:
        reasons.append("Risky Country")

    if amount > high_risk_amount:
        reasons.append("High Amount")

    if reasons:
        red_flag = ", ".join(reasons)
        cursor.execute("""
            UPDATE transactions
            SET suspicious = 'Yes',
                red_flag_reason = ?
            WHERE transaction_id = ?
        """, (red_flag, txn_id))

# Commit changes
conn.commit()

# Print flagged transactions
print("Suspicious Transactions:")
cursor.execute("""
    SELECT t.transaction_id, c.first_name || ' ' || c.last_name AS client_name, 
           t.amount, t.country, t.suspicious, t.red_flag_reason
    FROM transactions t
    JOIN clients c ON t.client_id = c.client_id
    WHERE t.suspicious = 'Yes'
""")
for row in cursor.fetchall():
    print(row)

# Close connection
conn.close()




