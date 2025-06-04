from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from src.config.jwt import create_access_token, get_current_user
from src.models.user import User
from src.schemas.auth import LoginRequest, LoginResponse, Token, UserResponse
from src.config.database.database import get_db
from sqlalchemy.orm import Session

from src.schemas.userCreate import UserCreate


router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

@router_auth.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token({"sub": user.email})
    user_response = UserResponse.from_orm(user)
    return {"access_token": token, "token_type": "bearer", "user": user_response}



@router_auth.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já cadastrado",
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return user

@router_auth.get(
    "/verify-token",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"detail": "Token válido"},
        401: {"detail": "Token inválido ou expirado"},
    }
)
def is_valid_token(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)