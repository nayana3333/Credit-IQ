from datetime import datetime

from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class CreditApplication(db.Model):
    __tablename__ = "credit_applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    checking_status = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    credit_history = db.Column(db.String(120), nullable=False)
    purpose = db.Column(db.String(80), nullable=False)
    credit_amount = db.Column(db.Float, nullable=False)
    savings_status = db.Column(db.String(80), nullable=False)
    employment = db.Column(db.String(80), nullable=False)
    installment_rate = db.Column(db.Integer, nullable=False)
    personal_status = db.Column(db.String(80), nullable=False)
    other_parties = db.Column(db.String(80), nullable=False)
    residence_since = db.Column(db.Integer, nullable=False)
    property_magnitude = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    other_payment_plans = db.Column(db.String(80), nullable=False)
    housing = db.Column(db.String(80), nullable=False)
    existing_credits = db.Column(db.Integer, nullable=False)
    job = db.Column(db.String(80), nullable=False)
    num_dependents = db.Column(db.Integer, nullable=False)
    own_telephone = db.Column(db.String(40), nullable=False)
    foreign_worker = db.Column(db.String(40), nullable=False)
    loan_amount = db.Column(db.Float, nullable=True)
    emi = db.Column(db.Float, nullable=True, default=0)
    interest_rate = db.Column(db.Float, nullable=True, default=0)
    lr_decision = db.Column(db.String(20), nullable=True)
    lr_confidence = db.Column(db.Float, nullable=True)
    lr_good_prob = db.Column(db.Float, nullable=True)
    lr_bad_prob = db.Column(db.Float, nullable=True)
    rf_decision = db.Column(db.String(20), nullable=True)
    rf_confidence = db.Column(db.Float, nullable=True)
    rf_good_prob = db.Column(db.Float, nullable=True)
    rf_bad_prob = db.Column(db.Float, nullable=True)
    final_decision = db.Column(db.String(20), nullable=True)
    consensus = db.Column(db.Boolean, default=False)
    lr_shap_reasons = db.Column(db.Text, nullable=True)
    rf_shap_reasons = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
