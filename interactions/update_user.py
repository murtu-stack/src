from models.user import User
from fastapi import HTTPException
from passlib.context import CryptContext

def update_user(user_id: int, request: dict):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user details
    for key, value in request.items():
        if hasattr(user, key):
            setattr(user, key, value)

    try:
        user.save()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))