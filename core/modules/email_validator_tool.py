from email_validator import validate_email, EmailNotValidError

def validate(target_email):
    try:
        valid = validate_email(target_email)
        print(f"Valid: {valid.email}")
    except EmailNotValidError as e:
        print(f"Invalid: {e}")

if __name__ == "__main__":
    email = input("Enter email: ")
    validate(email)
