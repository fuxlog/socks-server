import re

def validate_password(password: str) -> bool:    
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,254}$"
    if re.match(pattern, password) is None:
        return False
    
    return True

def validate_username(username: str) -> bool:
    pattern = r"^[a-zA-Z0-9_]{4,254}$"
    if re.match(pattern, username) is None:
        return False
    
    return True
