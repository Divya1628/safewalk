from fastapi import APIRouter, HTTPException, Depends, Header
from app.schemas import UserRegister, UserLogin, TokenResponse, TrustedContact, UserResponse
from app.services.auth_service import AuthService
from typing import Optional

router = APIRouter()


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Dependency to extract and verify JWT token from Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = parts[1]
    payload = AuthService.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload.get("user_id")


@router.post("/register", response_model=TokenResponse)
def register(payload: UserRegister):
    """
    Register a new user.
    """
    try:
        user = AuthService.register_user(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            phone=payload.phone,
        )
        token = AuthService.create_access_token(user["user_id"])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    """
    Login a user and return access token.
    """
    try:
        result = AuthService.login_user(
            email=payload.email,
            password=payload.password,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


@router.get("/me", response_model=UserResponse)
def get_profile(user_id: str = Depends(get_current_user)):
    """
    Get current user profile.
    """
    try:
        user = AuthService.get_user(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/trusted-contacts")
def add_trusted_contact(payload: TrustedContact, user_id: str = Depends(get_current_user)):
    """
    Add a trusted contact for emergency alerts.
    """
    try:
        contact = AuthService.add_trusted_contact(
            user_id=user_id,
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            relationship=payload.relationship,
        )
        return {"message": "Contact added", "contact": contact}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/trusted-contacts")
def get_trusted_contacts(user_id: str = Depends(get_current_user)):
    """
    Get all trusted contacts.
    """
    try:
        contacts = AuthService.get_trusted_contacts(user_id)
        return {"contacts": contacts}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
