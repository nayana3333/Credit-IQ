SAMPLE_APPLICATION = {
    "checking_status": "A11",
    "duration": 24,
    "credit_history": "A34",
    "purpose": "A40",
    "credit_amount": 3000,
    "savings_status": "A65",
    "employment": "A73",
    "installment_rate": 2,
    "personal_status": "A93",
    "other_parties": "A101",
    "residence_since": 2,
    "property_magnitude": "A121",
    "age": 35,
    "other_payment_plans": "A143",
    "housing": "A152",
    "existing_credits": 1,
    "job": "A173",
    "num_dependents": 1,
    "own_telephone": "A192",
    "foreign_worker": "A201",
}


def test_predict_persists_loan_amount_emi_interest_rate(client, auth_headers):
    payload = {**SAMPLE_APPLICATION, "loan_amount": 5000, "emi": 250, "interest_rate": 12.5}
    res = client.post("/api/v1/ml/predict", json=payload, headers=auth_headers)
    application_id = res.get_json()["application_id"]
    assert application_id is not None

    detail = client.get(f"/api/v1/ml/applications/{application_id}", headers=auth_headers)
    data = detail.get_json()
    assert data["loan_amount"] == 5000
    assert data["emi"] == 250
    assert data["interest_rate"] == 12.5


def test_list_loans_reads_from_credit_applications(client, auth_headers):
    client.post("/api/v1/ml/predict", json=SAMPLE_APPLICATION, headers=auth_headers)
    res = client.get("/api/v1/loans", headers=auth_headers)
    assert res.status_code == 200
    loans = res.get_json()
    assert len(loans) >= 1
    assert loans[0]["credit_amount"] == SAMPLE_APPLICATION["credit_amount"]
    assert "estimated_months" in loans[0]


def test_get_loan_decision_matches_prediction(client, auth_headers):
    predict_res = client.post("/api/v1/ml/predict", json=SAMPLE_APPLICATION, headers=auth_headers)
    application_id = predict_res.get_json()["application_id"]

    res = client.get(f"/api/v1/loans/{application_id}/decision", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["application_id"] == application_id
    assert data["lr"]["model_name"] == "Logistic Regression"
    assert data["rf"]["model_name"] == "Random Forest"
    assert data["input_summary"]["credit_amount"] == SAMPLE_APPLICATION["credit_amount"]


def test_demo_login_seeds_credit_applications(client):
    res = client.post("/api/v1/auth/demo")
    assert res.status_code == 200
    token = res.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    apps_res = client.get("/api/v1/ml/applications", headers=headers)
    assert apps_res.status_code == 200
    applications = apps_res.get_json()
    assert len(applications) == 2
    assert all(item["final_decision"] in ("approved", "rejected") for item in applications)

    dashboard_res = client.get("/api/v1/dashboard", headers=headers)
    assert dashboard_res.status_code == 200
    assert dashboard_res.get_json()["total_applications"] == 2
