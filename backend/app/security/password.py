"""
Password hashing using passlib/bcrypt.
"""
import bcrypt
from passlib.context import CryptContext

# Fix passlib compatibility with bcrypt >= 4.0.0
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (), {"__version__": getattr(bcrypt, "__version__", "4.0.0")})

_orig_hashpw = bcrypt.hashpw


def _patched_hashpw(password, salt):
    if len(password) > 72:
        password = password[:72]
    return _orig_hashpw(password, salt)


bcrypt.hashpw = _patched_hashpw

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)



def hash_password(plain_password: str) -> str:
    # Truncate to 72 bytes to satisfy bcrypt maximum input length limit
    pwd_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.hash(pwd_bytes.decode("utf-8", errors="ignore"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(pwd_bytes.decode("utf-8", errors="ignore"), hashed_password)

