import random
import string

def random_username(length: int = 10) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def random_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def random_firstname(length: int = 8) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))