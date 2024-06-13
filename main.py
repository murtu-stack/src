
from database.create_tables import create_tables
from fastapi import FastAPI,Depends,HTTPException,Query
from typing import Optional,Dict
from fastapi.encoders import jsonable_encoder
from fastapi.encoders import jsonable_encoder
from database.db_session import db
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta,timezone
from passlib.context import CryptContext
from interactions.create_user import create_user
from database.create_tables import create_tables
from playhouse.postgres_ext import BigAutoField
from interactions.get_current_user import get_current_user
from interactions.get_login_for_access_token import login_for_access_token
from interactions.list_users import get_all_users
from typing import List
from interactions.update_user import update_user
from interactions.delete_user import delete_user
from interactions.create_discussion import create_discussion
from models.user import User
from models.discussion import Discussion
from interactions.update_discussion import update_discussion
from interactions.like_comment import like_comment
from interactions.create_comment import create_comment
from interactions.get_comment import get_comment
from interactions.update_comment import update_comment
from interactions.list_discussion import get_all_discussions
from pydantic.types import Json


SECRET_KEY = "c2c78544f5fafc0673f1d2631c755571c11452d16dedf209060575b9d77ac82a"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTE = 30

class Token(BaseModel):
    access_token: str
    token_type: str

app = FastAPI()
# create_tables()
class UserData(BaseModel):
    user_name: str 
    email: str
    password: str 
    mobile_no: int=None
    first_name: str=None
    last_name: str=None
   
class UpdateUser(BaseModel):
    user_name: str = None
    email: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    mobile_number: str = None


class DiscussionCreate(BaseModel):
    text: str
    image: str = None
    hashtags: str = None

class DiscussionUpdate(BaseModel):
    text: str = None
    image: str = None
    hashtags: List[str] = None


class CommentCreate(BaseModel):
    discussion_id: int
    text: str
    parent_id: int = None

class CommentUpdate(BaseModel):
    text: str = None
    comment_id: int

@app.post("/create_user")
def create_user_api(request: UserData):
    try:
        return create_user(request.model_dump())
    except Exception as e:
        raise
    
@app.post("/token",response_model=Token)
def login_api(request: OAuth2PasswordRequestForm = Depends()):
    return jsonable_encoder(login_for_access_token(request))
    

@app.get("/users/me/")
def read_users_me(request: UserData= Depends(get_current_user)):
    return request.model_dump()


@app.post("/users/{user_id}/update/")
async def update_user_route(user_id: int, request: UpdateUser):
    try:
        request_data = request.dict(exclude_unset=True)
        result = update_user(user_id, request_data)
        return result
    except HTTPException as e:
        raise

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: str
    first_name: str = None
    last_name: str = None
    mobile_number: int =  None

    class Config:
        orm_mode = True


@app.get("/users/")
async def show_list_of_users(
    user_name: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
    mobile_number: int = None,
):
    filters = {
        "user_name": user_name,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "mobile_number": mobile_number,
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    try:
        users = get_all_users(filters)
        return users
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving users")
    

@app.post("/users/{user_id}", response_model=dict)
async def delete_user_route(user_id: int):
    try:
        result = delete_user(user_id)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the user")
    


@app.post("/create_discussion")
def create_discussion_api(discussion: DiscussionCreate, current_user: User = Depends(get_current_user)):
    try:
        return create_discussion(current_user.get("id"), discussion.dict())
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/update_discussion")
def update_discussion_api(discussion_id: int, discussion_update: DiscussionUpdate, current_user: User = Depends(get_current_user)):
    try:
        discussion_data = discussion_update.dict(exclude_unset=True)
        updated_discussion = update_discussion(discussion_id, current_user.get("user_name"), discussion_data)
        if updated_discussion is None:
            raise HTTPException(status_code=404, detail="Discussion not found or user not authorized to update this discussion")
        return updated_discussion
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.post("/create_comment")
def create_comment_api(comment: CommentCreate, current_user: User = Depends(get_current_user)):
    user_id =  User.select(User.id).where(User.user_name==current_user.get("user_name")).first()
    return create_comment(user_id, comment.dict())

@app.get("/{comment_id}", response_model=CommentCreate)
def get_comment_api(comment_id: int):
    comment = get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@app.post("/update_comment")
def update_comment_api(comment: CommentUpdate, current_user: User = Depends(get_current_user)):
    user_id =  User.select(User.id).where(User.user_name==current_user.get("user_name")).first()
    existing_comment = get_comment(comment.comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    return update_comment(comment.comment_id, comment.dict(exclude_unset=True))

@app.delete("/{comment_id}")
def delete_comment_api(comment_id: int, current_user: User = Depends(get_current_user)):
    user_id =  User.select(User.id).where(User.user_name==current_user.get("user_name")).first()
    existing_comment = get_comment(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    from interactions.delete_comment import delete_comment
    if delete_comment(comment_id):
        return {"message": "Comment deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete comment")

@app.post("/like/{comment_id}")
def like_comment_api(comment_id: int, current_user: User = Depends(get_current_user)):
    user_id =  User.select(User.id).where(User.user_name==current_user.get("user_name")).first()
    if like_comment(user_id, comment_id):
        return {"message": "Comment liked successfully"}
    raise HTTPException(status_code=404, detail="Comment not found")


@app.post("/follow/{user_id}")
def follow_user_api(user_id: int, current_user: User = Depends(get_current_user)):
    current_user = User.select().where(User.user_name == current_user.get("user_name")).first()
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
    from interactions.follow_user import follow_user
    
    if follow_user(current_user.id, user_id):
        return {"message": "User followed successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/unfollow/{user_id}")
def unfollow_user_api(user_id: int, current_user: User = Depends(get_current_user)):
    current_user = User.select().where(User.user_name == current_user.get("user_name")).first()
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot unfollow yourself")
    from interactions.unfollow_user import unfollow_user
                            
    if unfollow_user(current_user.id, user_id):
        return {"message": "User unfollowed successfully"}
    
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/followers/{user_id}")
def get_followers_api(user_id,current_user: User = Depends(get_current_user)):
    from interactions.get_followers import get_followers
    followers = get_followers(user_id)
    if followers is not None:
        return list(followers)
    raise HTTPException(status_code=404, detail="No followers found")

@app.get("/following/{user_id}")
def get_following_api(user_id,current_user: User = Depends(get_current_user)):
    from interactions.get_following import get_following
    following = get_following(user_id)
    if following is not None:
        return list(following)
    raise HTTPException(status_code=404, detail="No following found")

@app.get("/view_disussion/{discussion_id}")
def view_discussion(discussion_id,current_user: User = Depends(get_current_user)):
    from interactions.get_disussion import get_discussion
    return get_discussion(discussion_id)


@app.get("/list_discussions")
def list_discussions(filters: Json  = {}):
    try:
        discussions = get_all_discussions(filters)
        return discussions
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
