from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv("../../.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_alert(anomalies: list, dataset_info: dict) -> str:
    """Use LLM to generate human-readable alert"""

    if not anomalies:
        return "No anomalies detected in the dataset."

    # Build context for LLM
    anomaly_summary = []
    for a in anomalies[:5]:  # Top 5 anomalies
        if a["type"] == "zscore":
            anomaly_summary.append(
                f"- Column '{a['column']}': value {a['value']} "
                f"is {a['z_score']} standard deviations from mean ({a['mean']})"
            )
        else:
            anomaly_summary.append(
                f"- Column '{a['column']}': value {a['value']} "
                f"is outside normal range [{a['lower_bound']}, {a['upper_bound']}]"
            )

    prompt = f"""You are a data analyst AI. Analyze these anomalies and write a clear, 
concise executive alert (3-4 sentences max).

Dataset: {dataset_info.get('name', 'Business Dataset')}
Rows analyzed: {dataset_info.get('rows', 'Unknown')}
Total anomalies found: {len(anomalies)}

Anomalies detected:
{chr(10).join(anomaly_summary)}

Write a professional alert message explaining what was found and what action might be needed.
Be specific about the data issues found."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional data analyst writing executive alerts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.3
    )

    return response.choices[0].message.content

def generate_ml_insight(ml_results: dict) -> str:
    """Generate insight about ML model results"""

    prompt = f"""You are a data science AI. Summarize these AutoML results in 2-3 sentences 
for a business executive. Focus on what the best model means for the business.

Problem type: {ml_results.get('problem_type', 'classification')}
Best model: {ml_results.get('best_model', 'Unknown')}
Best score: {ml_results.get('best_score', 0)}
Target column: {ml_results.get('target_column', 'Unknown')}

Write a clear, jargon-free business summary."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a data science expert explaining ML results to business executives."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.3
    )

    return response.choices[0].message.content
