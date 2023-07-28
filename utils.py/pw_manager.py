from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)