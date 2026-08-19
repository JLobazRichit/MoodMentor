from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str
):
    existing_user = (
        db.query(User)
        .filter(
            (User.username == username) |
            (User.email == email)
        )
        .first()
    )

    if existing_user:
        return None

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user