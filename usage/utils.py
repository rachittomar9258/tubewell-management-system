def notify_user(phone_number, message):
    """
    Dummy SMS function for development.
    Baad me isko real SMS gateway (Fast2SMS/MSG91) se replace karenge.
    """
    print(f"[SMS to {phone_number}]: {message}")
    return True