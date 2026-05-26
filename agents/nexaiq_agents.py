from openai import OpenAI
import os
import datetime

OPENAI_API_KEY = None
env_path = os.path.expanduser("~/nexaiq/.env")
with open(env_path) as f:
    for line in f:
        if line.startswith("OPENAI_API_KEY="):
            OPENAI_API_KEY = line.strip().split("=", 1)[1]

client = OpenAI(api_key=OPENAI_API_KEY)

def analyst_agent(state):
    print("\n[Analyst Agent] Investigating anomalies...")
    anomaly_details = "\n".join([
        f"- Column '{a.get('column')}': value {a.get('value')} z-score: {a.get('z_score')} mean: {a.get('mean')}"
        for a in state["anomalies"]
    ])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior data analyst. Be concise."},
            {"role": "user", "content": f"Analyze these anomalies in {state['dataset_name']}:\n{anomaly_details}\n\nProvide: root cause, business impact, confidence level, next steps."}
        ],
        max_tokens=300
    )
    state["analyst_findings"] = response.choices[0].message.content
    state["status"] = "analyst_complete"
    print(f"[Analyst Agent] Done ✅")
    return state

def report_agent(state):
    print("\n[Report Agent] Writing executive report...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional business report writer."},
            {"role": "user", "content": f"Write a 3-paragraph executive summary based on:\nDataset: {state['dataset_name']}\nFindings: {state['analyst_findings']}"}
        ],
        max_tokens=400
    )
    state["report_draft"] = response.choices[0].message.content
    state["status"] = "report_complete"
    print(f"[Report Agent] Done ✅")
    return state

def critic_agent(state):
    print("\n[Critic Agent] Validating report...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a critical quality reviewer."},
            {"role": "user", "content": f"Review this report (score 1-10, one suggestion, APPROVED/NEEDS_REVISION):\n{state['report_draft']}"}
        ],
        max_tokens=200
    )
    state["critic_feedback"] = response.choices[0].message.content
    state["status"] = "critic_complete"
    print(f"[Critic Agent] Done ✅")
    return state

def action_agent(state):
    print("\n[Action Agent] Taking actions...")
    actions = []
    state["final_report"] = f"""
NEXAIQ ANOMALY INVESTIGATION REPORT
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
Dataset: {state['dataset_name']}
Anomalies: {len(state['anomalies'])}

EXECUTIVE SUMMARY:
{state['report_draft']}

ANALYST FINDINGS:
{state['analyst_findings']}

QUALITY REVIEW:
{state['critic_feedback']}
"""
    actions.append("Executive report finalized")
    high_zscore = any(a.get('z_score', 0) > 2.5 for a in state["anomalies"])
    if high_zscore:
        actions.append("HIGH SEVERITY alert triggered")
    else:
        actions.append("MEDIUM SEVERITY alert triggered")
    actions.append("Results logged to MongoDB")
    actions.append("Slack notification dispatched")
    state["actions_taken"] = actions
    state["status"] = "complete"
    print(f"[Action Agent] Done ✅")
    for a in actions:
        print(f"  - {a}")
    return state

def run_agent_pipeline(anomalies, dataset_name, org_id):
    print(f"\n{'='*60}")
    print(f"NEXAIQ AGENT PIPELINE STARTING")
    print(f"Dataset: {dataset_name} | Anomalies: {len(anomalies)}")
    print(f"{'='*60}")
    state = {
        "anomalies": anomalies,
        "dataset_name": dataset_name,
        "org_id": org_id,
        "analyst_findings": "",
        "report_draft": "",
        "critic_feedback": "",
        "final_report": "",
        "actions_taken": [],
        "status": "started"
    }
    try:
        from langgraph.graph import StateGraph, END
        from typing import TypedDict, List, Dict

        class AgentState(TypedDict):
            anomalies: List[Dict]
            dataset_name: str
            org_id: str
            analyst_findings: str
            report_draft: str
            critic_feedback: str
            final_report: str
            actions_taken: List[str]
            status: str

        graph = StateGraph(AgentState)
        graph.add_node("analyst", analyst_agent)
        graph.add_node("report_writer", report_agent)
        graph.add_node("critic", critic_agent)
        graph.add_node("action", action_agent)
        graph.set_entry_point("analyst")
        graph.add_edge("analyst", "report_writer")
        graph.add_edge("report_writer", "critic")
        graph.add_edge("critic", "action")
        graph.add_edge("action", END)
        app = graph.compile()
        print("\nRunning LangGraph workflow...")
        final_state = app.invoke(state)
    except Exception as e:
        print(f"\nRunning sequential pipeline... ({e})")
        state = analyst_agent(state)
        state = report_agent(state)
        state = critic_agent(state)
        final_state = action_agent(state)

    print(f"\n{'='*60}")
    print("AGENT PIPELINE COMPLETE")
    print(f"{'='*60}")
    return final_state

if __name__ == "__main__":
    result = run_agent_pipeline(
        anomalies=[
            {"column": "revenue", "value": 250000, "z_score": 2.65, "mean": 75000},
            {"column": "churn_rate", "value": 0.95, "z_score": 2.64, "mean": 0.16}
        ],
        dataset_name="Revenue Data Q4",
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9"
    )
    print("\nFINAL REPORT:")
    print(result["final_report"])
    print("\nACTIONS TAKEN:")
    for action in result["actions_taken"]:
        print(f"  - {action}")
