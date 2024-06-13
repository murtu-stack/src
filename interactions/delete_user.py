from fastapi import HTTPException
from models.user import User

def delete_user(user_id: int):
    try:
        user = User.get_or_none(User.id == user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.delete_instance()
        return {"detail": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
