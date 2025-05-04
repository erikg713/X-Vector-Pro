import re

def validate_email(email):
    """Validate the format of an email address."""
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, email):
        return True
    return False

def validate_password(password):
    """Validate the strength of a password."""
    # Password must be at least 8 characters long, contain at least one number, one uppercase letter, and one special character
    password_regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.match(password_regex, password):
        return True
    return False

def validate_ip_address(ip):
    """Validate an IPv4 address format."""
    ip_regex = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(ip_regex, ip):
        return True
    return False

def validate_url(url):
    """Validate a URL format."""
    url_regex = r"^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}(/[\w-]*)*$"
    if re.match(url_regex, url):
        return True
    return False

def validate_username(username):
    """Validate the format of a username."""
    # Username must be between 3-20 characters and can contain letters, numbers, and underscores
    username_regex = r"^[a-zA-Z0-9_]{3,20}$"
    if re.match(username_regex, username):
        return True
    return False

def validate_phone_number(phone):
    """Validate a phone number format."""
    phone_regex = r"^\+?[\d\s\-]{7,15}$"
    if re.match(phone_regex, phone):
        return True
    return False

def validate_date(date):
    """Validate a date in the format YYYY-MM-DD."""
    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(date_regex, date):
        return True
    return False
