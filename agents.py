import re
from math import pow

class CustomerAgent:
    name = "Customer / Banking Agent"

    def __init__(self, customers, transactions):
        self.customers = customers
        self.transactions = transactions

    def run(self, customer_id, intent):
        customer = self.customers[customer_id]
        if intent == "transactions":
            txs = [t for t in self.transactions if t["customer_id"] == customer_id]
            return {"customer_id": customer_id, "recent_transactions": txs[-6:]}
        return {
            "customer_id": customer_id,
            "name": customer["name"],
            "account_type": customer["account_type"],
            "account_number_masked": customer["account_number_masked"],
            "balance_inr": customer["balance"],
        }

class RiskFraudAgent:
    name = "Risk / Fraud Agent"

    def __init__(self, transactions):
        self.transactions = transactions

    def run(self, customer_id):
        txs = [t for t in self.transactions if t["customer_id"] == customer_id]
        flagged = []
        for t in txs:
            reasons = []
            if t["amount"] >= 40000:
                reasons.append("high transaction amount (₹40,000 or more)")
            if t["location"] not in ("Chennai", "Bengaluru", "Mumbai", "Online"):
                reasons.append("unusual location for this demo profile")
            if t["status"] == "DECLINED":
                reasons.append("transaction was declined")
            if reasons:
                flagged.append({"transaction_id": t["id"], "amount_inr": t["amount"],
                                "merchant": t["merchant"], "location": t["location"],
                                "status": t["status"], "reasons": reasons})
        return {
            "transactions_reviewed": len(txs),
            "flagged_count": len(flagged),
            "flagged_transactions": flagged,
            "method": "Transparent demo rules; flags indicate review candidates, not confirmed fraud."
        }

class CreditLoanAgent:
    name = "Credit / Loan Agent"

    def __init__(self, customers, loans):
        self.customers = customers
        self.loans = loans

    def run(self, customer_id, intent, question=""):
        customer = self.customers[customer_id]
        if intent == "emi":
            amount_match = re.search(r"(?:₹|rs\.?|inr)?\s*([0-9][0-9,]*)\s*(?:rupees|loan)?", question.lower())
            amount = int(amount_match.group(1).replace(",", "")) if amount_match else 500000
            rate_match = re.search(r"(\d+(?:\.\d+)?)\s*%", question)
            rate = float(rate_match.group(1)) if rate_match else 12.0
            year_match = re.search(r"(\d+)\s*(?:years?|yrs?)", question.lower())
            years = int(year_match.group(1)) if year_match else 3
            months = max(1, years * 12)
            monthly_rate = rate / 1200
            emi = amount / months if monthly_rate == 0 else amount * monthly_rate * pow(1 + monthly_rate, months) / (pow(1 + monthly_rate, months) - 1)
            return {"loan_amount_inr": amount, "annual_interest_rate_percent": rate,
                    "tenure_years": years, "estimated_monthly_emi_inr": round(emi, 2),
                    "note": "Illustrative EMI only; fees and lender-specific terms are excluded."}
        existing = self.loans.get(customer_id, [])
        dti = customer["existing_monthly_debt"] / max(customer["monthly_income"], 1)
        eligible = customer["credit_score"] >= 650 and dti <= 0.45
        return {
            "customer_id": customer_id,
            "credit_score_simulated": customer["credit_score"],
            "monthly_income_inr": customer["monthly_income"],
            "existing_monthly_debt_inr": customer["existing_monthly_debt"],
            "debt_to_income_ratio": round(dti, 2),
            "existing_loans": existing,
            "illustrative_eligibility": "Likely eligible for further assessment" if eligible else "May require manual review",
            "reasons": ["credit score threshold: 650", "debt-to-income threshold: 45%"],
            "disclaimer": "This is a toy rule for a demo, not a lending decision."
        }

class Supervisor:
    def __init__(self, customer_agent, risk_agent, credit_agent):
        self.customer = customer_agent
        self.risk = risk_agent
        self.credit = credit_agent

    def handle(self, question, customer_id):
        q = question.lower()
        results, trace = {}, ["Supervisor received the user request."]
        wants_balance = any(x in q for x in ["balance", "account", "customer profile", "account information"])
        wants_transactions = any(x in q for x in ["transaction", "recent activity", "payment history"])
        wants_fraud = any(x in q for x in ["fraud", "suspicious", "unusual transaction", "risk"])
        wants_loan = any(x in q for x in ["loan", "eligible", "eligibility", "credit score"])
        wants_emi = any(x in q for x in ["emi", "monthly payment", "monthly installment"])

        if not any([wants_balance, wants_transactions, wants_fraud, wants_loan, wants_emi]):
            wants_balance = True
            trace.append("No specific intent matched; defaulted to account summary.")

        if wants_balance:
            results[CustomerAgent.name + " — Account"] = self.customer.run(customer_id, "balance")
            trace.append("Routed account/profile request to Customer / Banking Agent → simulated account tool.")
        if wants_transactions:
            results[CustomerAgent.name + " — Transactions"] = self.customer.run(customer_id, "transactions")
            trace.append("Routed transaction-history request to Customer / Banking Agent → simulated transaction tool.")
        if wants_fraud:
            results[RiskFraudAgent.name] = self.risk.run(customer_id)
            trace.append("Routed risk request to Risk / Fraud Agent → rule-based transaction analysis.")
        if wants_loan or wants_emi:
            results[CreditLoanAgent.name] = self.credit.run(customer_id, "emi" if wants_emi else "eligibility", question)
            trace.append("Routed credit request to Credit / Loan Agent → simulated loan tool.")
        if len(results) > 1:
            trace.append("Supervisor aggregated outputs from multiple agents.")
        trace.append("Returned structured results to the response layer.")
        return {"question": question, "customer_id": customer_id, "results": results, "trace": trace}
