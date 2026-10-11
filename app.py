import streamlit as st
from agents import Supervisor, CustomerAgent, RiskFraudAgent, CreditLoanAgent
from data_store import customers, transactions, loans
from llm import natural_language_response

st.set_page_config(page_title="WrenchWise AI Banking", page_icon="🏦", layout="wide")

st.title("🏦 WrenchWise — Multi-Agent Banking MVP")
st.caption("Simulated banking environment • Demo data only • No real banking connection")

with st.sidebar:
    st.header("Demo customer")
    customer_ids = list(customers.keys())
    selected_id = st.selectbox("Choose customer ID", customer_ids, format_func=lambda x: f"{x} — {customers[x]['name']}")
    st.info("All balances, transactions, and loan details are fictional sample data.")
    st.markdown("**Available agents**")
    st.write("👤 Customer / Banking")
    st.write("🛡️ Risk / Fraud")
    st.write("💳 Credit / Loan")
    st.write("🧭 Supervisor / Orchestrator")
    use_llm = st.toggle("Use Gemini for final wording", value=False)
    api_key = ""
    if use_llm:
        api_key = st.text_input("Gemini API key", type="password", help="Optional. The app works without it.")

customer_agent = CustomerAgent(customers, transactions)
risk_agent = RiskFraudAgent(transactions)
credit_agent = CreditLoanAgent(customers, loans)
supervisor = Supervisor(customer_agent, risk_agent, credit_agent)

col1, col2 = st.columns([1.2, 1])
with col1:
    st.subheader("Ask the banking assistant")
    examples = [
        "What is my account balance?",
        "Show my recent transactions",
        "Are there any suspicious transactions?",
        "Am I eligible for a personal loan?",
        "Calculate EMI for a ₹500000 loan at 12% for 3 years",
        "Check my balance and identify suspicious transactions"
    ]
    chosen = st.selectbox("Try an example", ["Choose an example..."] + examples)
    question = st.text_area("Your question", value="" if chosen == "Choose an example..." else chosen,
                            placeholder="e.g., Check my balance and identify suspicious transactions", height=100)
    run = st.button("Run banking agents", type="primary", use_container_width=True)

with col2:
    st.subheader("Quick customer snapshot")
    c = customers[selected_id]
    st.metric("Available balance", f"₹{c['balance']:,.2f}")
    st.metric("Monthly income", f"₹{c['monthly_income']:,.0f}")
    st.write(f"**Customer:** {c['name']}  \n**Customer ID:** {selected_id}  \n**Credit score (simulated):** {c['credit_score']}")

if run:
    if not question.strip():
        st.warning("Enter a question or choose an example.")
    else:
        with st.spinner("Supervisor is routing your request..."):
            result = supervisor.handle(question, selected_id)
            answer = natural_language_response(question, result, api_key if use_llm else "")
        st.divider()
        st.subheader("Assistant response")
        st.write(answer)
        st.subheader("Execution trace")
        for i, event in enumerate(result["trace"], 1):
            st.write(f"{i}. {event}")
        st.subheader("Agent results")
        for agent_name, payload in result["results"].items():
            with st.expander(agent_name, expanded=True):
                st.json(payload)
        st.caption("Demo safety: outputs are based on fictional local data and simplified rules. They are not financial advice or real fraud determinations.")

st.divider()
st.subheader("Built-in demo scenarios")
scenario_cols = st.columns(3)
scenario_cols[0].markdown("**Customer / Banking**\n\nBalance and transaction history")
scenario_cols[1].markdown("**Risk / Fraud**\n\nRule-based anomaly flags with explanations")
scenario_cols[2].markdown("**Credit / Loan**\n\nIllustrative eligibility and EMI calculation")
