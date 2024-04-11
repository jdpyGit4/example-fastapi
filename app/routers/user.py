from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

# 72.) Last error that we see is that we don't have access to the app object. And so our instinct is to go to our main.py file and then import this "app = FastAPI()"
#   NOTE: And that's not exactly correct. Instead what we're going to do is we're going to make use of the routers that was mentioned earlier. And so from the FastAPI
#   library, we're going to import something called APIRouter. So, we'll say "router = APIRouter()". So we're basically creating a router object. And then what
#   we can do is we can replace the keyword "app" on our decorators because we don't have access to that in this file. And we just use the word "router". And we'll understand
#   why we do this in a bit. NOTE: And then we're going to do the same exact thing for our "post.py", so we have to get all of those imports above. We're actually going to copy
#   most of those because most of them are going to apply in the "post.py" file as well so this will be #73.
# 77.) NOTE: But keep in mind that our API is very simple. Other APIs could have very long, complex routes that may not look as simple as ours. They could have multiple things 
#   and then having to kind of copy and paste all of that every single route can seem little unnecessary. And so anytime we’re working with routers, what we can actually do 
#   is we can pass in a parameter or method into the APIRouter function. And so, what we can say is prefix. And we're going to say that since every single route in this file
#   always starts with "/posts", we can say prefix = "/posts". And so now, anytime we see a "/post", we can just remove that from our route or decorator and just leave the
#   slash "/". And then when it gets to "/posts/{id}", this is where it gets a little tricky. But once again, we just remove everything but a slash "/". And so what this is saying
#   is that we're going to take "/posts" and append it with the ID "{id}". So nothing actually changes. It's just simpler way to do things so that we don't have to write "/posts"
#   everywhere.
# 79.) We're restructuring our FastAPI's interactive documentation by SwaggerUI through our routers. So, now we're adding a specific group name using "tags" to group the post operations
#   into one.
router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist.")
    
    return user