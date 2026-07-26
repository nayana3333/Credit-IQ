import math
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def to_decimal(value, default="0"):
    try:
        if value is None or value == "":
            return Decimal(default)
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid number.")


def money(value):
    return float(to_decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def clamp(value, low, high):
    return max(low, min(high, value))


def loan_months(principal, annual_rate, emi):
    principal = float(principal)
    annual_rate = float(annual_rate)
    emi = float(emi)
    if principal <= 0 or emi <= 0:
        return None
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate <= 0:
        return math.ceil(principal / emi)
    monthly_interest = principal * monthly_rate
    if emi <= monthly_interest:
        return None
    months = -math.log(1 - (principal * monthly_rate / emi)) / math.log(1 + monthly_rate)
    return math.ceil(months)


def emi_for_loan(principal, annual_rate, months):
    principal = float(principal)
    annual_rate = float(annual_rate)
    months = int(months)
    if principal <= 0 or months <= 0:
        return None
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate <= 0:
        return money(principal / months)
    emi = principal * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
    return money(emi)


def amortization_schedule(principal, annual_rate, months, max_rows=120):
    emi = emi_for_loan(principal, annual_rate, months)
    if emi is None:
        return []
    balance = float(principal)
    monthly_rate = float(annual_rate) / 100 / 12
    rows = []
    row_count = int(months) if max_rows is None else min(int(months), max_rows)
    for month in range(1, row_count + 1):
        interest = balance * monthly_rate
        principal_paid = min(emi - interest, balance)
        if principal_paid <= 0:
            break
        balance = max(balance - principal_paid, 0)
        rows.append(
            {
                "month": month,
                "emi": money(emi),
                "principal": money(principal_paid),
                "interest": money(interest),
                "balance": money(balance),
            }
        )
        if balance <= 0:
            break
    return rows
