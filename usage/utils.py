from django.db.models import Sum
from usage.models import UsageRecord
from payments.models import Payment


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


def notify_user(phone_number, message):
    """
    Dummy SMS function for development.
    Baad me isko real SMS gateway (Fast2SMS/MSG91) se replace karenge.
    """
    print(f"[SMS to {phone_number}]: {message}")
    return True