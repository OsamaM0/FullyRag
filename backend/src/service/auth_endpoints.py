"""
Authentication endpoints for secure user login and token management.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr

from db_manager import DatabaseManager
from security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()
db_manager = DatabaseManager()


# Pydantic Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    email: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    user_id: str
    email: str
    message: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: str
    email: str


# Dependency to get current user from token
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """
    Dependency to extract and verify the current user from JWT token.
    """
    token = credentials.credentials
    payload = verify_token(token, token_type="access")

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return {"user_id": user_id, "email": payload.get("email")}


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user.

    Args:
        request: Registration data with email and password

    Returns:
        User information and success message
    """
    # Check if user already exists
    existing_user = db_manager.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Hash the password
    hashed_password = hash_password(request.password)

    # Create user in database
    try:
        user = db_manager.create_user(email=request.email, hashed_password=hashed_password)

        return RegisterResponse(
            user_id=str(user.id),
            email=user.email,
            message="User registered successfully",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}",
        )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Login and receive access and refresh tokens.

    Args:
        request: Login credentials

    Returns:
        JWT tokens and user information
    """
    # Get user from database
    user = db_manager.get_user_by_email(request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "email": user.email})

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=str(user.id),
        email=user.email,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(request: RefreshRequest):
    """
    Refresh an access token using a refresh token.

    Args:
        request: Refresh token

    Returns:
        New access token
    """
    payload = verify_token(request.refresh_token, token_type="refresh")

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = payload.get("sub")
    email = payload.get("email")

    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    # Create new access token
    access_token = create_access_token(data={"sub": user_id, "email": email})

    return RefreshResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Get current user information from token.

    Returns:
        Current user details
    """
    return UserResponse(user_id=current_user["user_id"], email=current_user["email"])


@router.post("/logout")
async def logout(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Logout endpoint (token invalidation should be handled client-side).

    Returns:
        Success message
    """
    # In a production system, you might want to blacklist the token
    # For now, client-side token removal is sufficient
    return {"message": "Logged out successfully"}
