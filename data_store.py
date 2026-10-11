customers = {
    "C1001": {
        "name": "Aarav Sharma", "account_type": "Savings", "account_number_masked": "XXXXXX1042",
        "balance": 82500.75, "monthly_income": 65000, "credit_score": 742,
        "existing_monthly_debt": 8500
    },
    "C1002": {
        "name": "Meera Krishnan", "account_type": "Salary", "account_number_masked": "XXXXXX8871",
        "balance": 24350.00, "monthly_income": 42000, "credit_score": 628,
        "existing_monthly_debt": 22000
    },
    "C1003": {
        "name": "Kabir Iyer", "account_type": "Savings", "account_number_masked": "XXXXXX3096",
        "balance": 196400.20, "monthly_income": 110000, "credit_score": 790,
        "existing_monthly_debt": 12000
    }
}

transactions = [
    {"id": "TX001", "customer_id": "C1001", "date": "2026-10-10 09:20", "merchant": "Coffee House", "amount": 320, "location": "Chennai", "status": "SUCCESS"},
    {"id": "TX002", "customer_id": "C1001", "date": "2026-10-10 12:10", "merchant": "Grocery Mart", "amount": 2450, "location": "Chennai", "status": "SUCCESS"},
    {"id": "TX003", "customer_id": "C1001", "date": "2026-10-10 18:40", "merchant": "Electronics Hub", "amount": 48500, "location": "Singapore", "status": "SUCCESS"},
    {"id": "TX004", "customer_id": "C1001", "date": "2026-10-10 18:42", "merchant": "Online Wallet", "amount": 42500, "location": "Online", "status": "DECLINED"},
    {"id": "TX005", "customer_id": "C1002", "date": "2026-10-09 10:00", "merchant": "Metro Travel", "amount": 180, "location": "Chennai", "status": "SUCCESS"},
    {"id": "TX006", "customer_id": "C1002", "date": "2026-10-09 15:45", "merchant": "Luxury Store", "amount": 52000, "location": "Dubai", "status": "SUCCESS"},
    {"id": "TX007", "customer_id": "C1003", "date": "2026-10-08 11:30", "merchant": "Book Shop", "amount": 850, "location": "Bengaluru", "status": "SUCCESS"},
    {"id": "TX008", "customer_id": "C1003", "date": "2026-10-08 17:00", "merchant": "Travel Portal", "amount": 64000, "location": "Online", "status": "SUCCESS"},
]

loans = {
    "C1001": [{"type": "Education loan", "outstanding_inr": 120000}],
    "C1002": [{"type": "Personal loan", "outstanding_inr": 85000}],
    "C1003": []
}
