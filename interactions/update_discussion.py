from models.user import User
from models.discussion import Discussion
from fastapi import HTTPException
from typing import Optional

def update_discussion(discussion_id: int, user_name: str, discussion_data: dict) -> Optional[Discussion]:
    try:
        user_id =  User.select(User.id).where(User.user_name==user_name).first()
        discussion = Discussion.get_or_none(Discussion.id == discussion_id, Discussion.user == user_id)
        if not discussion:
            raise HTTPException(status_code=404, detail="Discussion not found or user not authorized to update this discussion")
        
        for key, value in discussion_data.items():
            if value is not None:
                setattr(discussion, key, value)
        
        discussion.save()
        return discussion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))