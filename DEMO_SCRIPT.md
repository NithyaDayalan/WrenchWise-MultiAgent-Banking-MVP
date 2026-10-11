# 5–10 minute demo video script

## 0:00–0:45 — Introduction
"Hi, this is my simulated real-time banking architecture MVP. It demonstrates a supervisor that routes requests to Customer/Banking, Risk/Fraud, and Credit/Loan agents. All records are fictional."

## 0:45–1:45 — Architecture
Show the interface and explain:
- Streamlit is the UI.
- The Supervisor class classifies the request and routes to agents.
- Each agent calls local simulated tools/data.
- The response layer uses deterministic grounded output by default, with optional Gemini wording.
- The execution trace makes the routing visible.

## 1:45–2:45 — Account balance
Select customer C1001 and ask "What is my account balance?"
Show the answer and expand the Customer / Banking Agent result.

## 2:45–3:45 — Transactions and risk
Ask "Are there any suspicious transactions?"
Show the Risk/Fraud Agent's flagged transactions and explain that each flag has a reason and is not a confirmed fraud finding.

## 3:45–4:45 — Loan eligibility
Ask "Am I eligible for a personal loan?"
Explain the sample score and debt-to-income rule are illustrative only.

## 4:45–5:30 — EMI
Ask "Calculate EMI for a ₹500000 loan at 12% for 3 years." Show the monthly estimate.

## 5:30–6:30 — Multi-agent request
Ask "Check my balance and identify suspicious transactions."
Show that the Supervisor invokes both the Customer and Risk/Fraud agents and aggregates their results.

## 6:30–7:00 — Close
Summarize what is implemented, limitations, and possible next steps such as structured LLM routing, database persistence, tests, and stricter governance controls.
