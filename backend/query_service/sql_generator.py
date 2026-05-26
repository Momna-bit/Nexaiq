from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv("../../.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Schema knowledge — what tables exist
SCHEMA = """
Tables available:

1. clean_data — cleaned business data uploaded by user
   Columns: org_id, dataset_id, name, age, salary, churn
   (columns vary based on uploaded CSV)

2. raw_data — raw uploaded data
   Columns: org_id, dataset_id, plus all CSV columns

3. mart_summary — summary statistics per dataset
   Columns: org_id, dataset_id, total_rows,
   total_columns, numeric_columns, null_count, columns

4. ml_models — trained ML models
   Columns: id, org_id, dataset_id, model_name,
   problem_type, best_score, target_column,
   status, created_at

5. datasets — uploaded file records
   Columns: id, org_id, filename, blob_url,
   status, row_count, created_at
"""

def generate_sql(question: str, org_id: str) -> str:
    """Convert natural language question to SQL"""

    prompt = f"""You are a SQL expert. Convert the user question to a 
PostgreSQL query.

IMPORTANT RULES:
1. Always filter by org_id = '{org_id}'
2. Only use SELECT statements — never INSERT, UPDATE, DELETE
3. Return ONLY the SQL query, nothing else
4. Use simple, readable SQL
5. Limit results to 100 rows maximum

Available schema:
{SCHEMA}

User question: {question}

SQL query:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a SQL expert. Return only valid PostgreSQL SQL queries."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # Clean up SQL — remove markdown if present
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql

def validate_sql(sql: str) -> bool:
    """Basic SQL safety check"""
    sql_upper = sql.upper()
    dangerous = ["INSERT", "UPDATE", "DELETE", "DROP",
                 "CREATE", "ALTER", "TRUNCATE"]
    for word in dangerous:
        if word in sql_upper:
            return False
    return True
