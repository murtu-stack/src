from models.discussion import Discussion
from fastapi import  HTTPException

def increment_view_count(discussion_id):
    query = Discussion.update(view_count=Discussion.view_count + 1).where(Discussion.id == discussion_id)
    query.execute()


def get_discussion(discussion_id):
    discussion = Discussion.get_or_none(Discussion.id == discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    
    increment_view_count(discussion_id)

