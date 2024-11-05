#hashing
from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"])

def hashing(password:str):
    return pwd_context.hash(password)

def comparehash(plain_password,hash_password):
    return pwd_context.verify(plain_password,hash_password)
    
