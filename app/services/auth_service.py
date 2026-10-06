from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
from app.config import settings
from app.database import db
from bson import ObjectId


class AuthService:
    """
    Authentication and JWT token management.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    @staticmethod
    def create_access_token(user_id: str, expires_in_hours: int = 24) -> str:
        """Create a JWT access token."""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def register_user(email: str, password: str, full_name: str, phone: str) -> dict:
        """
        Register a new user.
        """
        # Check if user exists
        existing_user = db["users"].find_one({"email": email.lower()})
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = AuthService.hash_password(password)

        user_data = {
            "email": email.lower(),
            "password_hash": hashed_password,
            "full_name": full_name,
            "phone": phone,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "trusted_contacts": [],
            "is_active": True,
        }

        result = db["users"].insert_one(user_data)
        user_id = str(result.inserted_id)

        return {
            "user_id": user_id,
            "email": user_data["email"],
            "full_name": user_data["full_name"],
            "phone": user_data["phone"],
            "created_at": user_data["created_at"],
        }

    @staticmethod
    def login_user(email: str, password: str) -> dict:
        """
        Authenticate a user and return access token.
        """
        user = db["users"].find_one({"email": email.lower()})
        if not user:
            raise ValueError("Invalid email or password")

        if not AuthService.verify_password(password, user["password_hash"]):
            raise ValueError("Invalid email or password")

        if not user.get("is_active"):
            raise ValueError("User account is inactive")

        access_token = AuthService.create_access_token(str(user["_id"]))

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "user_id": str(user["_id"]),
                "email": user["email"],
                "full_name": user["full_name"],
                "phone": user["phone"],
                "created_at": user["created_at"],
            },
        }

    @staticmethod
    def get_user(user_id: str) -> dict:
        """
        Get user profile by ID.
        """
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("User not found")

        return {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "phone": user["phone"],
            "created_at": user["created_at"],
            "trusted_contacts": user.get("trusted_contacts", []),
        }

    @staticmethod
    def add_trusted_contact(user_id: str, name: str, phone: str, email: str = None, relationship: str = "friend") -> dict:
        """
        Add a trusted contact for emergency alerts.
        """
        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "relationship": relationship,
            "added_at": datetime.utcnow(),
        }

        db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"trusted_contacts": contact}},
        )

        return contact

    @staticmethod
    def get_trusted_contacts(user_id: str) -> list:
        """
        Get all trusted contacts for a user.
        """
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("User not found")

        return user.get("trusted_contacts", [])
