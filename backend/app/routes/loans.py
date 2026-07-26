import json

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..finance import amortization_schedule, loan_months, money
from ..models import CreditApplication

loans_bp = Blueprint("loans", __name__)


def _loan_payload(item):
    loan_amount = item.loan_amount if item.loan_amount is not None else item.credit_amount
    interest_rate = item.interest_rate or 0
    emi = item.emi or 0
    months = loan_months(loan_amount, interest_rate, emi)
    schedule = amortization_schedule(loan_amount, interest_rate, months, max_rows=None) if months else []
    interest = money(sum(row["interest"] for row in schedule)) if schedule else None
    return {
        "id": item.id,
        "loan_amount": loan_amount,
        "credit_amount": item.credit_amount,
        "duration": item.duration,
        "purpose": item.purpose,
        "age": item.age,
        "employment": item.employment,
        "status": item.final_decision or "pending",
        "created_at": item.created_at.isoformat(),
        "emi": emi,
        "interest_rate": interest_rate,
        "estimated_months": months,
        "estimated_interest": interest,
        "estimated_total_payable": money(loan_amount + interest) if interest is not None else None,
    }


@loans_bp.get("")
@jwt_required()
def list_loans():
    user_id = int(get_jwt_identity())
    items = CreditApplication.query.filter_by(user_id=user_id).order_by(CreditApplication.id.desc()).all()
    return jsonify([_loan_payload(item) for item in items])


@loans_bp.get("/<int:loan_id>/decision")
@jwt_required()
def get_loan_decision(loan_id):
    user_id = int(get_jwt_identity())
    item = CreditApplication.query.filter_by(id=loan_id, user_id=user_id).first_or_404()
    input_summary = {
        "checking_status": item.checking_status,
        "duration": item.duration,
        "credit_history": item.credit_history,
        "purpose": item.purpose,
        "credit_amount": item.credit_amount,
        "savings_status": item.savings_status,
        "employment": item.employment,
        "installment_rate": item.installment_rate,
        "personal_status": item.personal_status,
        "other_parties": item.other_parties,
        "residence_since": item.residence_since,
        "property_magnitude": item.property_magnitude,
        "age": item.age,
        "other_payment_plans": item.other_payment_plans,
        "housing": item.housing,
        "existing_credits": item.existing_credits,
        "job": item.job,
        "num_dependents": item.num_dependents,
        "own_telephone": item.own_telephone,
        "foreign_worker": item.foreign_worker,
    }
    return jsonify(
        {
            "loan": _loan_payload(item),
            "lr": {
                "decision": item.lr_decision,
                "confidence": item.lr_confidence,
                "good_probability": item.lr_good_prob,
                "bad_probability": item.lr_bad_prob,
                "shap_reasons": json.loads(item.lr_shap_reasons or "[]"),
                "model_name": "Logistic Regression",
            },
            "rf": {
                "decision": item.rf_decision,
                "confidence": item.rf_confidence,
                "good_probability": item.rf_good_prob,
                "bad_probability": item.rf_bad_prob,
                "shap_reasons": json.loads(item.rf_shap_reasons or "[]"),
                "model_name": "Random Forest",
            },
            "final_decision": item.final_decision,
            "consensus": item.consensus,
            "input_summary": input_summary,
            "application_id": item.id,
            "created_at": item.created_at.isoformat(),
        }
    )
