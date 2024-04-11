# 87.) Importing from jose.
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# 96.) This is for the "Depends()"" that's in (95). We'll pass in an OAuth2 schemes inside "Depends".
#   And so we pass in the '/login' route in the "tokenUrl=". FastAPI understands that those routes 
#   require a token that should be obtained by hitting the /login endpoint with valid credentials. 
#   This way, the tokenUrl parameter not only informs the client about where to obtain the token but also integrates with FastAPI's security and documentation systems to provide a clear and secure way to handle user authentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# 88.) There's going to be three things/pieces of information for our token. There's three pieces of information.
#   But there's three other things about the token that we need to provide. So we're going to need the secret key which is the
#   special key that was mentioned before which ultimately handles verifying the data integrity of our token, which resides on our
#   server only. So we're going to have provide that secret key, and we're also need to provide the algorithm that we want to use.
#   We're going to be using HS256. And then we're going to need to provide one other thing, which is the expiration time
#   of the token. If we just give a plain token, without an expiration date that means that users logged in forever.
#   And there's no application that just lets a user log in forever. So we're going to provide an expiration time so that we can
#   dictate exactly how long a user should be logged in after they actually perform a login operation.
#   NOTE: SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES are from the documentation (OAuth2 Scopes)
# 119.) So if we go to our "oath2.py" file, we can now change these credentials below for our JWT into environment variables. So first, let's import "settings" from our "config.py" file.
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" --Because of 119
# ALGORITHM = "HS256" --Because of 119
# ACCESS_TOKEN_EXPIRE_MINUTES = 30 --Because of 119
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

#89.) We're going to define our access token. Remember, the access token is going to have a payload. So whatever data we want to
#   encode into the token, we have to provide that. So we're going to pass that in as a variable called data. And this is going
#   to be of type dict. And what we're going to do is we're actually going to make a copy of this "data" because we don't want
#   to actually change it, and we're going to manipulate a few things. And we don't want to accidentally change the original data.
#   So we're going to say "data.copy", and this will be stored in a new variable which will be "to_encode". So this is all the data
#   that we're going to encode into our JWT Token. Then we're going to create the expiration field. To actually do this, there's
#   a couple of things. First of all, right now we have it set to 30 minutes. And so what we need to do is to provide the time of 30
#   minutes from now. So we have to provide the time that it's going to expire in. So we have to grab the current time and then add
#   30k minutes. And so anytime we're working with dates and times, we have to import the "datetime" library.
#   NOTE: On the line, to_encode.update({"exp": expire}) - So we're just adding that extra property into all of that data that we want to
#       encode into our JWT. And so now our JWT will tell us when it's going to expire, 
#   NOTE: and what we're going to do is we're calling
#       JWT coming from "jose" library. And we're creating this method "jwt.encode()", and this will actually going to create JWT
#       token. And we'll say the first property is everything that we want to put into the payload.
#       The second one is going to be the secret key, and the signature and then we have to specify the algorithm which will be
#       "algorithm=ALGORITHM". And let's store this method "jwt.encode()" in a variable "encoded_jwt".
#   NOTE:Finally, we just have to return the "encoded_jwt". Then we go back to our specific path operation which is 
#       "@router.post('/login')" inside our "auth.py" file and import this "oauth2.py" to our "auth.py". 
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# 94.) Then we have to create a function to verify the access token. So let's create the function and it's going to just be called verify access token. And what we're going to do
#   is we're going to pass in a token, which is going to be a string. And we're also going to pass in the specific credentials exception. So we're going to pass in what our exception
#   should be if the credentials don't match, or there's some issue with the token. So we'll just store this in a variable "credentials_exception". And so here, we're going to access
#   the JWT library. And we'll say "jwt.decode" this is to decode our JWT Token, and here, we're going to pass in a couple things. First of all, the token, then we have to pass in
#   the secret key, so that we can decode it, and then we have to pass in the algorithm that's used.
#   NOTE: Obviously, it's not a good idea/practice to store the secret key within our actual code. In the later section, we're going to turn these into environemt variables so that
#       it's not hard coded into our code. And we're going to store this in payload in a variable called "payload". So this will just store all of our payload data. And to extract
#       data, what we can do is we can say "payload.get", then we have to get the specific field that put in. So if we go back to my "auth.py" file in our routers, and we take a
#       look at our data, we can see that we have a field called "user_ID". And that's going to get the ID of the user. And this will be stored in a variable called "id" and should be
#       of type "string". If there's no id, then we're going to raise a credentials exception. So whatever exception we provided into this function, it's going to raise that.
#       token_data = schemas.TokenData(id=id) - the id is the id that we extracted from the "payload.get", and also, this line will going to validate if it matches our specific token schema.
#       Now, if we look at our schema for the TokenData, it's literally one thing. And we made it optional. So we shouldn't make it optional, but we'll come back to fixing this in
#       a bit. But this is just going to ensure that all the data we pass in the token is actually there. And so that's why we're using a schema for that. However, for one actual variable,
#       we don't actually need to do that, especially since we're checking to see if it exists right here. But it's good to always make sure so in the future, if we do add extra fields, we
#       can also validate the schema here. Now, we're almost done with this function. However, there's one little issue, because we can run into an error in any one of these lines. And so
#       so anytime we're working with code that can error, we want to do "try except" block. (95) Next thing we have to do is define one last function and it's called "get_current_user".
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception
        
    return token_data
    
# 95.) Next thing we have to do is define one last function and it's called "get_current_user". Ultimately, the purpose of this is that we can pass as a dependency into any one of our path operations.
#   And when we do that, it's going to take the token from the request automatically, then extract the ID for us. It's going to verify that the token is correct by calling the "verify_access_token".
#   And then it's going to extract the ID. And then if we want to, we can have it automatically fetch the user from the database and then add it into as a parameter into our path operation function.
#   So from (96), we have to pass in the "oauth2_scheme" in the "Depends" as our dependencies. Then under this function, we have to define our credentials exception that we're going to pass into the
#   "verify_access_token" function. So when the credential is wrong, or there's some kind of issue with the JWT token, what exception should we raise? So here, we're just going to say HTTPException().
#   Finally, we return the "verify_access_token" function and pass in the "token" and the credentials_exception
#   NOTE: Just to quickly recap. Because we know we did a lot, and some of it may be confusing. But what's going to happen is anytime we have a specific endpoint that should be protected, and what
#       that means is that the user needs to be logged in to use it. What we're going to do is, for example, let's say that user who want to be able to create a post, they need to be logged in.
#       What we can do is we can just add in an extra depedency into the path operation function. So we can say, on our "def create_posts" function from the "post.py",NOTE: we have to pass in the
#       "get_current_user: int = Depends(oath2.get_current_user)" - so we have the variable "get_current_user" which would return an int, and then we'll say this equals and then we pass in a dependency.
#       So we'll say depends on "oauth2.get_current_user". So this is going to add a dependency which is going to be that function that we created called "get_current_user"
#       So anytime anyone wants to access a resource that requires them to be logged in, we're going to expect that they provide an access token. And then we provide this dependency, which is going to
#       call this function "get_current_user", and then we pass in the token that comes from the request, we're going to then run this "verify_access_token" function. In this case, then it's going to 
#       provide all of the logic for verifying that the token is okay, and that there's no errors. If there are no errors, then we go ahead and return nothing essentially. And that means that they were
#       successfully able to be authenticated. If we do return some kind of error, with the credentials_exception, then they're going toget that appropriate 401 response back.
#       So that's how our login works. But there are a couple of different components that are involved.
# 98.) So, the author will show us how we can do that in this lesson. So, keep in mind, we get the token_data back, which is going to be nothing more than an ID. And what we’re going to do is first of all, 
#   we need access to our database so that we can fetch the users. So we’re going to import the “database.py” in the “oauth.py”file. And within this function "get_current_user()", we can pass in the other
#   dependencies so that we can actually get access to the db or "database" object. And then we have to import Session from SQL Alchemy. So now, we can make a request to a database and what we're going to
#   do here is first of all, we'll no longer going to return "verify_access_token" function directly. And we're going to say "token = verify_access_token(token,credentials_exception)". And since we have
#   access to the token, what we can do now is we can say "db.query(models.User).filter(models.User.id == token.id).first()" - and let's import models. So now we can query a specific user based on their ID
#   and it just needs to match the ID that the token is associated with, and let's store it to this "user" variable, and return the "user". So on our "post.py", let's change the name of the variable that
#   is holding the dependency that returns user's id which is "user_id" (This will be 99) and change it to "current_user" since it's storing a user data now. So the variable name will be changed to
#   "current_user". And after testing it, it now also successfully prints the email associated with its own token. So that's ultimately why this function exists. Because normally here, this is where we
#   query our database to grab the user and then we return the user. And then whatever we return there on the "post.py" file's operations is ultimately what allows any of our other routes to get whatever
#   we're returning. Since we're returning a user, we're going to store it as a variable called "current_user".
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    # return verify_access_token(token, credentials_exception) --Because of 98

    return user