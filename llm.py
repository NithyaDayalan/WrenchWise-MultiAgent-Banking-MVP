import json

def natural_language_response(question, result, api_key=""):
    """
    Optional Gemini response layer. If no key is supplied or the API call fails,
    a deterministic answer is generated from tool results so the MVP still works.
    """
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = (
                "You are a careful banking demo assistant. Answer using ONLY the JSON data below. "
                "Never invent account values. Clearly say this is simulated data. Do not claim a flagged "
                "transaction is confirmed fraud. Keep the answer concise.\n\n"
                f"User question: {question}\nTool results JSON: {json.dumps(result['results'], ensure_ascii=False)}"
            )
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            if response.text:
                return response.text
        except Exception as exc:
            fallback = deterministic_answer(result)
            return fallback + f"\n\n(LLM unavailable; deterministic fallback used: {type(exc).__name__})"
    return deterministic_answer(result)

def deterministic_answer(result):
    lines = ["Here is what I found in the simulated banking system:"]
    for name, payload in result["results"].items():
        if "Account" in name:
            lines.append(f"- {payload['name']} has a {payload['account_type']} account ending {payload['account_number_masked'][-4:]}, with balance ₹{payload['balance_inr']:,.2f}.")
        elif "Transactions" in name:
            txs = payload["recent_transactions"]
            lines.append(f"- Found {len(txs)} recent transaction(s).")
            for t in txs:
                lines.append(f"  • {t['date']}: {t['merchant']} — ₹{t['amount']:,.2f} ({t['status']}, {t['location']}).")
        elif "Risk" in name:
            lines.append(f"- Risk agent reviewed {payload['transactions_reviewed']} transactions and flagged {payload['flagged_count']} for review.")
            for t in payload["flagged_transactions"]:
                lines.append(f"  • {t['transaction_id']} at {t['merchant']} for ₹{t['amount_inr']:,.2f}: {'; '.join(t['reasons'])}.")
            lines.append("  These are rule-based review flags, not confirmed fraud.")
        elif "Credit" in name and "estimated_monthly_emi_inr" in payload:
            lines.append(f"- Estimated EMI: ₹{payload['estimated_monthly_emi_inr']:,.2f}/month for ₹{payload['loan_amount_inr']:,.0f} over {payload['tenure_years']} year(s) at {payload['annual_interest_rate_percent']}% annual interest.")
        elif "Credit" in name:
            lines.append(f"- Illustrative loan assessment: {payload['illustrative_eligibility']}. Credit score {payload['credit_score_simulated']}; debt-to-income ratio {payload['debt_to_income_ratio']:.0%}.")
    lines.append("Note: This application uses fictional data and simplified rules; results are not financial advice.")
    return "\n".join(lines)
