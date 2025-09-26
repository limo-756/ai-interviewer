from email_validator import validate_email, EmailNotValidError


def is_email_valid(email: str) -> bool:
    if email is None or type(email) != str:
        return False
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_password_valid(password: str) -> bool:
    if password is None or type(password) != str:
        return False
    return password is not None and len(password) >= 8
