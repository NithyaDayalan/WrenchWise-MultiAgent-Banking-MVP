# WrenchWise Multi-Agent Banking MVP

A small simulated banking assistant demonstrating a Supervisor/Orchestrator and three specialized agents: Customer/Banking, Risk/Fraud, and Credit/Loan.

> **Important:** All data is fictional. This is a learning/demo application, not a real banking system, a fraud determination system, or financial advice.

## Features

- Streamlit chat-like interface and customer selector
- Supervisor routes user requests to one or more specialized agents
- Simulated account and transaction tools
- Transparent rule-based transaction risk flags with explanations
- Illustrative loan eligibility check and EMI calculator
- Execution trace showing routing and aggregation
- Optional Gemini response wording; app works without an API key

## Architecture

1. **UI (`app.py`)**: captures the question and selected demo customer.
2. **Supervisor (`agents.py`)**: performs lightweight intent classification and chooses one or more agents.
3. **Specialized agents (`agents.py`)**:
   - Customer/Banking: profile, account balance, transaction history
   - Risk/Fraud: evaluates mock transactions using transparent demo rules
   - Credit/Loan: toy eligibility rule and EMI calculation
4. **Simulated data/tools (`data_store.py`)**: local fictional customer, transaction and loan records.
5. **Response layer (`llm.py`)**: deterministic response by default; optional Gemini generation grounded in tool outputs.
6. **Interface**: displays answer, execution trace and structured agent outputs.

This is a modular, rule-routed multi-agent MVP. The agents are separate components called by a supervisor; they are not autonomous services and do not access real banking systems.

## Requirements

- Python 3.10+
- Internet access only if installing dependencies or using Gemini
- Gemini API key is optional

## Run locally

### Windows

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local address printed by Streamlit, usually `http://localhost:8501`.

## Optional Gemini integration

1. Install dependencies using `pip install -r requirements.txt`.
2. In the app sidebar, enable **Use Gemini for final wording**.
3. Enter your Gemini API key in the password field.
4. The key is used for that app session only and is not saved to a file by this project.

If no key is entered, the app produces a deterministic response from agent outputs. If the LLM call fails, it falls back to deterministic output.

## Use cases to demo

1. `What is my account balance?`
2. `Show my recent transactions`
3. `Are there any suspicious transactions?`
4. `Am I eligible for a personal loan?`
5. `Calculate EMI for a ₹500000 loan at 12% for 3 years`
6. `Check my balance and identify suspicious transactions` — demonstrates multi-agent routing.

Choose different customers in the sidebar to see how outputs change.

## Risk and limitations

- Fraud flags use simple thresholds and location/status heuristics; they are not a trained fraud model.
- Loan eligibility is a toy rule based on a simulated credit score and debt-to-income ratio.
- The EMI estimate excludes fees and lender-specific conditions.
- No real money movement, payment execution, customer PII, or real banking APIs are used.
- Never commit real API keys to GitHub.

## Suggested next improvements

- Add unit tests and schema validation for tool outputs.
- Replace keyword routing with structured LLM intent classification and strict schema validation.
- Add SQLite persistence and request IDs.
- Add role-based access, audit events and explicit approval before simulated transactions.
