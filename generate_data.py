import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

tiers = ['Enterprise', 'Mid-Market', 'Free']
feedbacks = [
    ("Unable to execute query", "Your query engine keeps throwing a timeout error on my warehouse. This is blocking our daily ETL report and our executives are furious! Fix this immediately."),
    ("Billing query regarding invoice", "Hi team, I noticed a $15 charge on my credit card this month, but I thought I was on the free tier. Could someone please clarify how billing works for extra storage?"),
    ("Feature request for dashboards", "Love the platform overall! Would be great if we could export Streamlit charts directly into PDF format for our weekly team syncs."),
    ("Database connector broken", "The Python connector keeps dropping connections every 10 minutes after the latest patch. I spent 4 hours debugging this and it ruined my afternoon."),
    ("Critical production outage", "Database locked up completely during peak business hours. Customers cannot log in. High escalation! Need immediate support tier intervention.")
]

data = []
base_time = datetime(2026, 8, 1, 9, 0, 0)

for i in range(1, 101):
    subject, text = random.choice(feedbacks)
    tier = random.choice(tiers)
    created = base_time + timedelta(hours=random.randint(1, 100))
    resolved = created + timedelta(hours=random.randint(1, 48))
    
    data.append({
        "ticket_id": f"TICK-{1000 + i}",
        "customer_id": f"CUST-{random.randint(100, 999)}",
        "account_tier": tier,
        "created_at": created.strftime("%Y-%m-%d %H:%M:%S"),
        "resolved_at": resolved.strftime("%Y-%m-%d %H:%M:%S"),
        "ticket_subject": subject,
        "customer_feedback": text
    })

df = pd.DataFrame(data)
df.to_csv("raw_support_tickets.csv", index=False)
print("Created raw_support_tickets.csv with 100 realistic ticket records!")