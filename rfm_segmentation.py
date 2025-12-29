import pandas as pd
from sqlalchemy import create_engine

# MySQL connection
engine = create_engine(
    "mysql+mysqlconnector://root:Bharati%4007@localhost:3306/consumer360"
)

# Load RFM base data
df = pd.read_sql("SELECT * FROM customer_rfm_base", engine)

# -----------------------------
# RFM SCORING
# -----------------------------

# Recency: lower is better → reverse labels
df["recency_score"] = pd.qcut(df["recency"], 5, labels=[5,4,3,2,1])

# Frequency: higher is better
df["frequency_score"] = pd.qcut(df["frequency"], 5, labels=[1,2,3,4,5])

# Monetary: higher is better
df["monetary_score"] = pd.qcut(df["monetary"], 5, labels=[1,2,3,4,5])

# Convert to int
df[["recency_score","frequency_score","monetary_score"]] = \
df[["recency_score","frequency_score","monetary_score"]].astype(int)

# -----------------------------
# RFM SEGMENTATION
# -----------------------------

df["rfm_score"] = (
    df["recency_score"] +
    df["frequency_score"] +
    df["monetary_score"]
)

def segment(score):
    if score >= 13:
        return "Champion"
    elif score >= 9:
        return "Loyal"
    elif score >= 6:
        return "At Risk"
    else:
        return "Hibernating"

df["segment"] = df["rfm_score"].apply(segment)

# Save output
df.to_csv("rfm_segmented_output.csv", index=False)

print("✅ RFM segmentation completed successfully")
