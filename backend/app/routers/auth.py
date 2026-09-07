from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.errors import commit_or_conflict
from app.models import User
from app.schemas.auth import TokenOut, UserLogin, UserOut, UserRegister
from app.security import create_access_token, hash_password, verify_password

router = APIRouter()


def _issue_token(user: User) -> TokenOut:
    return TokenOut(access_token=create_access_token(user.user_id, user.role))


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(body: UserRegister, db: Session = Depends(get_db)):
    """First account becomes admin so you can log in on an empty database."""
    user_count = db.scalar(select(func.count()).select_from(User)) or 0
    role = "admin" if user_count == 0 else "cashier"

    try:
        password_hash = hash_password(body.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    user = User(
        username=body.username,
        email=str(body.email),
        password_hash=password_hash,
        role=role,
    )
    db.add(user)
    commit_or_conflict(db, "Username or email already exists")
    db.refresh(user)
    return user


def _authenticate(db: Session, username: str, password: str) -> User:
    user = db.scalar(
        select(User).where(or_(User.username == username, User.email == username))
    )
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return user


@router.post("/login", response_model=TokenOut)
def login_json(body: UserLogin, db: Session = Depends(get_db)):
    """JSON login for React: { "username": "...", "password": "..." }."""
    user = _authenticate(db, body.username, body.password)
    return _issue_token(user)


@router.post("/token", response_model=TokenOut)
def login_form(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Form login so Swagger's Authorize button works."""
    user = _authenticate(db, form.username, form.password)
    return _issue_token(user)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
