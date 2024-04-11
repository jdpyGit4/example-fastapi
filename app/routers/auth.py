# 80.) Before creating the new path operations for the login we're going to import few things
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

# 81.) Creating the path operations for the login. So this will be a POST request because remember, the user is going
#   to have to provide his/her credentials. Generally, when we want to send data in one direction, it's going to be a POST request.
#   NOTE: Because we're going to fetch the user from the database, we're going to have to import our database session.
#       And so from SQL Alchemy we need to import Session. And so we'll do the same thing that we did with every other path operation
#       which is inputting the "db" or "db : Session = Depends(get_db)"; additionally, we need to import the get_db function
#   NOTE: Since the user is going to be providing the login information, it makes sense to set up a schema so that
#       we can ensure that they provide the exact pieces of data that we ultimately want. This will be located on the "schemas.py" (#82)
#       And so now, we can access all the user information or the attempted login information with the user credentials variable
#       And we're going to make a request to our database, specifically, our users table to retrieve the user based off of his email.
#       Now, if there's no user with that specific email, then we're going to return an error or we're going to raise an HTTP exception.
#       After this, once we verify that we did actually get a user object, we have to verify that the passwords are equal. So this would
#       be performing that logic of hashing the password that they gave us and seeing if that it compares to the password from the database.
#   NOTE: And so what we're going to do is we're going to create a new function (83) in the "utils.py" file, that's going to be responsible
#       for comparing the two hashes, or actually, it's going to take in the raw password, the password attempt, it's going to hash it for us,
#       and then it's going to compare it to the hash in the database.
# 84.) And now we're going to use the "verify" function from the "utils.py" (from 83).
#   And on the bottom part we're going to return {"token"}. NOTE: We haven't really gone over how to do that, as of now, it's just a plain text "token".
# 90.) After creating "def create_access_token" from our "oauth2.py", we can now create an "access_token" under this path operation.
#   NOTE: We're going to pass in a dictionary which will be stored in the "data", and remember the "data" that we want to put in the payload. So
#   we've decided that we're going to put in the user ID, and pretty much nothing else. We could give it a role. We can do something else.
#   But as of now, the author just wants to encode the user ID. However, if we wanted to provide some extra information about the user, if we
#   wanted to provide the scope of different endpoints, they can access, we can put all of those information in here. And now, what we can do is
#   we're going to return the "access_token" and then we're going to tell the user what kind of token this is and this is referred to as a bearer token.
#   NOTE: The author will explain how to actually configure that on the front end. But literally in the authorization header, we just write the word
#   bearer, and then we provide the token. So after testing, it return successfully with the access token and it tell us that is a bearer token.
#   NOTE: Let's copy that access token, and search for the jwt.io. And then, let's paste into the field and it will decode for us. Remember that
#       none of these information are encrypted and anyone can see this information. But by being able to sign it, we know that no one can kind of
#       mess with it. And we can also specify an epxiration time. So we know how long this token is valid. So when our API gets it, it's going to just
#       verify that nobody touched the token. It's going to verify that, "hey, the expiration time isn't before the current time" which would mean that
#       it's already expired. At that point, it already knows the token is valid. And then we can assume that everything is good to go. 
# 91.) NOTE: We're going to make one small change when it comes to retrieving the user's credentials in our login route. Instead of passing it in the
#       body, we're going to use a built in utility in the FastAPI. So we're importing "from fastapi.security.oauth2 import OAuth2PasswordRequestForm"
#       Instead of doing the usual here with the user_credentials, we're actually going to delete this "schemas.UserLogin", and we're going to provide a dependency.
#       So we're setting up a dependency kind of like we do with the database. And so this is going to require us to retrieve the credentials.
#       And then FastAPI is automatically going to store it inside this variable called "user_credentials". However, we have to make one small change. So the
#       username when we retrieve the user's attempted credentials from that variable "user_credentials", what it's going to do is it's going to store it in a field
#       not called "email", but it's going to store it in a field called "username". So when we compare the "models.User.email", when we're querying the database,
#       we can't compare to "user_credentials.email" because there's no field called ".email". It's going to return 2 things which will be our username and password.
#       And since we don't have access to email, then we have to use ".username", and so from "user_credentials.email" to "user_credentials.username". Well, this is
#       a bad example because we have to think of it as a dictionary, but that's how it is there will be field for username and password. And so we'll just tag
#       "user_credentials.username" and just grab the "username", which in our case will happen to be the email. The OAuth2PasswordRequestForm doesn't really care
#       what the username is, it could be a username, it can be an email, it can be an id, it doesn't really matter, it's just whatever the user actually sends,
#       it's just going to store it in a field called "username." So those are all of the changes that we have to mek from our backend side.
#       NOTE: NOw, when it comes to testing things, we no longer send the credentials in the body, like we normally do in the Postman. And if we try to send this now,
#        we'll be getting an error because it says "username" is missing and this field required us to fill in and also the password. So what it's doing is it's no
#        longer expects from the "raw" which is under "Body" (Postman). Instead, it expects inside the "form-data". And now, after testing it on the "form-data",
#       it successfully returns the access_token and the token type. So those are the couple of changes that we have to make. But we'll see that it makes life a little
#       bit easier setting up that dependency and using the built in functionality of FastAPI.
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}