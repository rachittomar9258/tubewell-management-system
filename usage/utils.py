from django.db.models import Sum
from usage.models import UsageRecord
from payments.models import Payment
import requests

FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"


def send_fast2sms(owner, phone_number, message):
    """
    Fast2SMS ke through SMS bhejta hai. Success par True return karta hai.
    """
    if not owner.fast2sms_api_key:
        return False

    try:
        headers = {"authorization": owner.fast2sms_api_key}
        params = {
            "route": "q",          # Quick SMS route
            "message": message,
            "numbers": phone_number,
        }
        response = requests.get(FAST2SMS_URL, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get("return", False)   # Fast2SMS success par "return": true bhejta hai
        return False
    except requests.RequestException:
        return False


def notify_user(owner, phone_number, message):
    """Existing function — ab Fast2SMS se bhejega."""
    return send_fast2sms(owner, phone_number, message)


def calculate_balance(owner, renter, tubewell):
    # ... existing logic, waisa hi rehne do
    ...


def calculate_balance(owner, renter, tubewell):
    """
    Renter ka is tubewell (aur is owner) ke against balance nikalta hai.
    Balance = Total usage amount - Total confirmed payments
    """
    total_usage = UsageRecord.objects.filter(
        tubewell=tubewell, used_by=renter, status='completed', is_self_use=False
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_paid = Payment.objects.filter(
        tubewell=tubewell, paid_by=renter, paid_to=owner, status='success'
    ).aggregate(total=Sum('amount'))['total'] or 0

    return total_usage - total_paid

def send_fast2sms(owner, phone_number, message):
    if not owner.fast2sms_api_key:
        print("DEBUG: API key khaali hai")
        return False

    try:
        headers = {"authorization": owner.fast2sms_api_key}
        params = {
            "route": "q",
            "message": message,
            "numbers": phone_number,
        }
        response = requests.get(FAST2SMS_URL, headers=headers, params=params, timeout=10)

        print("DEBUG status code:", response.status_code)
        print("DEBUG response body:", response.text)

        if response.status_code == 200:
            data = response.json()
            return data.get("return", False)
        return False
    except requests.RequestException as e:
        print("DEBUG exception:", e)
        return False
