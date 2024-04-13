# from typing import Optional, List # NOTE: After 71, Transferred to routers>post.py # NOTE: Because of 110 and this line is not utilized anymore in this file
from fastapi import FastAPI # NOTE: After 71, Transferred to routers>user.py # NOTE: Because of 110 and removing esponse, status, HTTPException, Depends 
# from fastapi.params import Body # NOTE: Because of 110 and this line is not utilized anymore in this file
# from pydantic import BaseModel # NOTE: Because of 110 and this line is not utilized anymore in this file
# from passlib.context import CryptContext #67 --Got transferred to "utils.py"
# from random import randrange # NOTE: Because of 110 and this line is not utilized anymore in this file
# import psycopg2 --Because the code was moved to "database.py" file (110)
# from psycopg2.extras import RealDictCursor --Because the code was moved to "database.py" file (110)
# import time # NOTE: Because of 110 and this line is not utilized anymore in this file
# from sqlalchemy.orm import Session # NOTE: After 71, Transferred to routers>user.py # NOTE: Because of 110 and this line is not utilized anymore in this file
from . import models # NOTE: After 71, Transferred to routers>user.py # NOTE: Because of 110 and removing schemas, utils
# from .database import engine, SessionLocal --- we transfer the def get_db() to the database.py 
from .database import engine # NOTE: After 71, Transferred to routers>user.py # NOTE: Because of 110 and removing get_db

# 74.) We have to go to our main.py file which is this file, and actually make use of those routers. Because you'll see that in our main.py file, there's no reference
#   to anything in here. So our API won't work if we try to run it now. So we're going to say:
# 85.) import auth (from utils.py)
from .routers import post, user, auth, vote

# from pydantic_settings import BaseSettings # 111.) This will be used for environment variables (113)Because it will be transferred to "config.py"

from .config import settings

# 151.) This is one of the requirements in configuring the CORS so that we can send request to our API even though we're on a different domain.
#   And we need to post this section "app.add_middleware()" (This will be 152 below our app=FastAPI)
from fastapi.middleware.cors import CORSMiddleware

# 111.) Just like with any other Pydantic model, we can set up a class. Let's call it "Settings" Class. And this is going to extend "BaseSettings".
#   And here, we can basically just provide a list of all of the environment variables that we need to set as properties on the class itself. And so,
#   maybe we need something called "database_password". And this needs to be a type "string" and give it a default value which is "localhost". And maybe
#   we need a "database_username" which is going to be a string and we can give it once again a default value which is "postgres". And maybe we want
#   "secret_key" and it's going to be a type string and with an arbitrary default value. And let's say these are the only environment variables that
#   need for our application to run. By setting it like this, it's going to automatically perform all of the validation for us to ensure that all of
#   these have been set. And an important thing to understand when we set environment variables, normally best practice for environment variables is to
#   do all caps with underscores. It doesn't have to be all caps, but this is just kind of standard convention. But in general, we want to do it all caps.
#   And we can see here we reference it all in lowercase. So pydantic will automatically handle all of this from a case in sensitive perspective.
#   So it doesn't matter if we capitalize this or lowercase everything, it'll take all of our environment variables and it'll convert it to lowercase
#   just to simplify everything. Then we create a variable called "settings" (112)
# class Settings(BaseSettings): -- (113) Because it will be transferred to "config.py"
#     database_password: str = "localhost" -- (113)Because it will be transferred to "config.py"
#     database_username: str = "postgres" -- (113)Because it will be transferred to "config.py"
#     secret_key: str = "234ui2340892348" -- (113)Because it will be transferred to "config.py"

# 112.) Then we create a variable called settings = Settings(). So right here, all we're doing is we're creating an instance of the settings class. And
#   And so at this point, Pydantic will read all of these environment variables. And once again, it'll look for them from a case insensitive perspective.
#   So it doesn't matter if they're capitalized or not. And then it's going to perform all of the validation, it's going to ensure that they're properly
#   a "string" and so on. And then finally, it's going to store it in a variable called "settings". So then we can access all of these variables by just
#   saying "settings.database_password" - and the name of the property so if we want to get the "database_password" we just have to write that line.
#   And so after testing and printing the "database_password", "database_username" they all return with their default value. So we haven't set our
#   system environment variables to ba any of these values. So it's going to use the default one. And like the author said, we're going to run into that
#   Windows issue where we cant exactly update it without closing everything. So we're not going to bother doing that. But what the author will do is
#   just to show us how this validation work is let's remove those default values on our "Settings" class. Let's say there's no default password. And so
#   if there's no default password, then we know, it's first going to check our system or our user environment variables to see if there's something
#   called "database_password". And since we didn't provide a default one, if there's no environment variable with that name, it's going to throw an error
#   because the whole point of this is to validate that all of the environment variables that we have are configured there. And so afer we save it, if
#   if we take a look at this, we could see that we get one validation error for "settings" which is "database_password" is missing. Alright having that
#   quick check makes our life so much easier so that we don't have to figure out which environment variable is missing, which one is not because we could
#   have 10, 20, 30, 40 of them. There's going to be a lot of them. And manageing them does become a little bit of a challenge. NOTE: Now one quick thing,
#   let's say we go to our environment variables once more. And we've got something called path. So "Path" is something the path to a specific directory.
#   And we want to access the "path" but we're going to say that this needs to be of type "int". So Pyhton is going to perform some validation, it's going
#   to read it and every environment variables always read as a "string". And then it's going to try to typecase it into an "integer". And if it failes,
#   it's going to throw an error. And so since this is clearly not an integer, then it should throw an error and after testing, that value is not a valid
#   integer. Now, for all of the settings in the environment variables, the author usually like to create a separate file to hold all of this information.
#   So under "app", we're going to create a new file called "config.py"
# settings = Settings() -- (113)Because it will be transferred to "config.py"
# print(settings.database_username) -- (113)Because it will be transferred to "config.py"


# 67.) And then what we need to do after importing this: "from passlib.context import CryptContext" is to define the setting. And so basically all we're doing is
#   we're telling "passlib" what is the default hashing algorithm or what hashing algorithm do we want to use? In this case, we want to use "bcrypt". So that's all this
#   is doing. Now, when we go to our user registration, we have to do a couple things.
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") --Got transferred to "utils.py"

# 28.) After creating the model and connecting the database, we have this method below where it creates engine. So this going to create all of our models.
#   NOTE: So we imported these commands: "from . import models" and "from .database import engine"

# 151.) **SPECIAL NOTE: This is after 150 from alembic>versions>add_phone_number.py. So moving forward, now that we have “alembic”, we no longer actually need this command.
#   This is the command that told SQL Alchemy to run the create statements so that it generated all of the tables when it first started up. But since we have "alembic" now,
#   we no longer this command. However, if we want to keep it in, it's not really going to break anything. It just depends on how we want things to work. Because if it does
#   create the tables for us, then our first "alembic" migration isn't going to have to do anything because everything is already there. But we're going to leave this
#   commented out moving forward becase we don't really need it.
# models.Base.metadata.create_all(bind=engine) --Because of 151.

app = FastAPI()

# 153.) So we're creating an empty list here inside the variable "origins". And here, we're going to provide a list of all of the domains that can talk to our API. And before
#   we fill that in, we just want to quickly talk about the other three as well. So our CORS policy...
origins = ["*"]

# 152.) This is one of the requirements in configuring the CORS so that we can send request to our API even though we're on a different domain. It will throw a little error
#   on the "origin" part and we can also delete that default value on the allow_origins and change that into an array [] for now. NOTE: But what we want to do is first of all,
#   we have to pass in the middleware and middleware is a term that's used in most web frameworks, because it's basically a function that runs before every request. So if
#   someone sends a request to our app, before it actually goes through all of those "routers" below, it'll actually go through the middleware and then our middleware can
#   perform some sort of operation. But what we want to do is, first of all, we have to specify the origins that we want to allow. So what domains should be able to talk to
#   our API? Because right now, it's no other domain, and only if it's running on the same exact domain, we are able to talk to our API. So the way we can do is we can put
#   in a list and let's called it our "origins". So our CORS policy can be pretty granular. So not only can we allow specific domains, we can also allow only specific HTTP
#   methods. So if we were building like a Public API where people can just retrieve data, we may not want to allow them to send post requests and put requests and delete
#   requests. So we could potentially just allow get requests. And then we can even allow specific headers as well. But for now, we're just going to allow all headers and
#   all methods. And we're going to just kind of drill down based off of what origins can talk to us. And so if we want Google to be able to talk to us, we can just say
#   "https://www.google.com" on the "origins" list. And so now, this CORS policy is set to allow people from google.com to talk to us. And so if we go back to google.com,
#   and we hit up this command again on the console: fetch('http://localhost:8000/').then(res => res.json()).then(console.log), then we'll see that we do successfully get
#   a response back and there's no CORS error. And also we added YouTube as well. Lastly, we're going to set our "origins" as wild card ["*"] and this means it's going to
#   to be access through any domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4.) We're going to define a class, and it's going to represent what a post should look like. So, we're just calling this "post". And this class is going to extend BaseModel.
#   And then here, we pass in the different properties for our post which are the 'title' and the 'content'.
# 5.) Now let's say that we want to assign a property that's optional. Like what if we want it to make it so that the front end can either choose to send some piece of data
#   or not send a piece of data. For example we want the user to be able to define if a "post" should be published or not, well, we can create a field called "published" and set
#   as a "Boolean"/"bool"
#   So, on this "published" property, we can say if the user doesn't provide us a value, then we can give it a default value. So, here we'll say "True". And so, if the user doesn't
#   provide "published", then it's going to default to "True". If it does provide published, then whatever value the user give it, that's what we're going to use it as. So if there's
#   no published on the body of our API then once the user post and we fetch the "published" property from their post, what we'll get is the default value which is "True".
# 6.) Now, let's say we wanted to create another field. However, instead of giving it a default value if it's not sent, we want it to default to None. So we want it completely
#   optional, and we're not going to store any value. And if the user doesn't provide it, what we can do is let's say the field is a rating, let's say the user can give each
#   post a "rating". So, this property is going to be a fully optional field. And if the user doesn't provide it, then it's going default to a value of None.
#   NOTE: And so that's what's awesome about, now we can ensure that our front end is send the exact data that we expect by using these pydantic models.
#       So moving forward in this course,  we are going to really make use of pydantic models to ensure that the schemas are not only receiving data from the front end, but also
#       sending data back which is all matching up with our organized shcema
#   46.) NOTE: This Schema or Pydantic Model will be transferred to the schemas.py
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    # rating: Optional[int] = None # So for now this will be removed since this was just for demonstration purposes.

# 16.) So after successfully install this "pip install psycopg2" on our terminal, we're going to set up our connection. A connection on to a database can fail, or maybe the database
#   is unreachable, maybe the database is down. There's a lot of things that could cause issues with us being able to connect to it, we could put in wrong passwords or something like
#   that. So anytime we have some kind of code within Python that could potentially fail, we're going to use the "try" statement.
#   NOTE: This library is a little bit weird. So when we actually make a query to retrieve a bunch of rows from the database, it doesn't include the column names but it just gives
#   us the values of the columns. So we need to pass in an extra field to get the column names so we need to import this : "from psycopg2.extras import RealDictCursor".
#   NOTE: But just as a quick test, we're going to change our password here from ####### to ########1. So, this will result to failure in connecting the Database and it
#   printed out the error, and then it just keeps going through the rest of our code. So then it starts up our FastAPI server. But at this point, our application is not going to work
#   because the Postgres database connection failed. So really, our application, our API, our web server can't do anything until we get a connection to our database. So just having
#   it fail, and then kind of gracefull handling that error doesn't do anything, we need to wait for that connection to actually go through before we do anything else. Or then at
#   this point, there's really no point in having our server up and running if we can't access our database. So what we're going to do is to set up a while loop.
#   On the while loop, we imported time to make delays in executing the connection if ever it will fail
#########################NOTE: This was Moved to the "database.py" file (This is after 109)##############################
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='########', password='########', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() # Going to be used in executing SQL statements
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)
#########################NOTE: This was Moved to the "database.py" file (This is after 109)##############################

# 7.) Save the posts in memory. So, we just have to create a variable, just globally that's going to store all of our posts. So, it's going to be an array. This array is going
#   to contain a whole bunch of post objects. And what each post is going to be is essentially a dictionary. And the dictionary is going to look like this: 
#   [{"title": "title of post 1", "content": "content of post 1"}]
#   NOTE: And then what we'll also do is like, anytime we save a piece of information within a database, the databse is going to create a unique identifier and ID. Now since
#       we're not working with databases, there's no ID, however, it's going to create issues. Because when it comes to working with CRUD based API is we need to be able to fetch
#       data and update data based off of the ID of a specific post. So we do need to still have an ID so that we can uniquely reference any single item within this array.
#       so we're going to have another field called ID. And then its just going to have'some random integer, and it's just got to be unique. So, this is what our post is going to
#       look like. And we're going to just store it in this array. We're going to have a multiple posts. And we're going to keep this one hard coded because every time we change our 
#       code, and hit Save and Refresh, it's going to clear this out. Because, remember, this is just stored in memory. So every time our application restarts, we're going to lose
#       that data. Just to keep things simple, we're going to hardcode another entry.
#   NOTE: Now that we actually have some place to store our post, we can actually test out our get post functionalitiy which is  @app.get("/posts")
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}] # NOTE: Because of 110 and this line is not utilized anymore in this file

# 10.) We're just going to create a simple function. And it's going to be called find_post. So we'll pass in an ID in this function to retrieve the post.
#   And we'll iterate over the my_posts. 
########################### NOTE: Because of 110 and this line is not utilized anymore in this file#########################
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

        
# 14.) Define a function about deleting a post. So, we're passing in the ID that we're interested in. Then we're going to iterate over the array, but we're also going to grab
#   the specific index as we iterate over it and we do that by using enumerate. So, we'll get the access to the individual post that we're iterating over as well as the index.
#   So this will return the index of that post/dicttionary with that specific ID. So we can call this function at # 13
########################### NOTE: Because of 110 and this line is not utilized anymore in this file#########################
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


# 75.) And so above this route which is the "@app.get("/")", we're going to say we're going to grab the "app" object. This is once again, our FastAPI object that we kind of
#   do everything with. We're going to say, include router. And then we'll grab the "post.router". So we imported "post" which is the "post.py" and we're importing the "router"
#   object. And so what we've basically done here is when we get an HTTP request and before we had all of our path operations in here, instead, what's going to happen is we go
#   down the list like we normally do. And so as we go down our list, this is our first app object that we reference. And in that "post.router", it just says, we want to include
#   everything our "post.router". And so the request will then go into the "post.py", and it's going to take a look at all of those routes. And it's going to see if it's
#   a match. And if it finds a match, it's going to respond like it normally does. So that's how we break out our code into separate files, we use the router objects. And we can do
#   the same thing with the "user.py". And so once again, all we're doing is we're just grabbing the "router" object from the "user.py" file. And that's essentially going to
#   import all of the specific routes.
# 86.) NOTE: router for auth has been used here
# 125.) NOTE: router for vote has been used here
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

        
#1.) The code below is a path operation and based on the documentation for Fast API this refers to as a path operation

# This the decorator: @app.get("/"). This decorator will help this code act as an API. This decorator turns into an actual path operation, so that someone who wants to use our
#   API can hit this endpoint. 
#       - "app" : We just have to specify the "@" symbol, and that's how we clarify that this is going to be a decorator. Then we reference our Fast API instance. 
#       - ".get": And then we have a couple of different options. So here, what we pass in is the HTTP method that the user should use.
#       So this is a "get" method, which means that we have to send a get request to our API. But we can use plenty of different HTTP methods. (Check the other HTTP Methods)
#       - ("/") : So, this is the root path. This is basically the path after the specific domain name of our API. So if we take a look at our URL, our we server is hosted
#       on this specific URL: 127.0.0.1. So, if we go on this page, the URL and the path in this case is just slash. So it's just equivalent of just hitting directly the enter
#       on the search bar where our URL/page is inserted, or putting a slash, which doesn't change anything. Whether there's slash or not, it's basically going to take us to
#       the same URL.
#       
@app.get("/")
# This is the function. On this function there's an "async" keyword, technically, this is optional. This keyword is only needed if you're going to be performing
#   some sort of asynchronous tasks, so something that takes a certain amount of time. So things like, you know making an API call, things like talking to the 
#   database. If we want to do that asynchronously, then we do have to pass in the "async" keyword. Ex: "async def root():". But right now we'll just use a
#   regular function.
def root():
    # So moving forward, in a development environment, only when we're in a development environment, we're going to pass in "--reload". When we go to production, we don't need that,
    #   we're not going to be setting it up because we're not going to be changing our code in a production environment.
    return {"message": "Hello World!!!!!!!!"}

# 31.) We're going to create another route, or another path operation just for testing purposes because we don't want to mess up any of our other code.
#   On this test, however, we don't have a session or depends in this case. So we're going to import those: froms sqlalchemy.orm import Session and from fastapi import Depends
# 32.) NOTE: Last thing that we're going to do is to delete our "posts" table from Postgres.
# 33.) NOTE: So after saving all of the codes and running it, it now creates a table on the fastapi database because of the "models.py"
# 37.) NOTE: Testing this test route to run our first query. And then afterwards, we can go ahead and delete this. And then we can update all of our pre existing path operations.
#   And so, anytime we want to perform any kind of database operation with SQL Alchemy within FastAPI, we want to make sure that we pass it as a parameter into our path operation
#   function. So we just call db, so we're saving it inside a variable called db. Then we're just calling the session object. And we're calling the "get_db" function within Depends.
#   So this makes it a dependency. If we already forgot what that is, just go to our database.py, we can see that it's this function.
# 39. To make a query, we're going to access that database object "db" which is getting passed in to our function. And we need to pat on the query method and we need to pass in
#   the specific model in the query method which is our Post mode or "models.Post". And from here, what we can do is to query all of our posts, so we just do ".all()". This will
#   grab every single entry within the post table
# @app.get("/sqlalchemy") --53.) NOTE: removing this for now, because we don't this right now. This was used during our testing with the SQL Alchemy
# def test_posts(db: Session = Depends(get_db)): --53.) NOTE: removing this for now, because we don't this right now. This was used during our testing with the SQL Alchemy

#     posts = db.query(models.Post).all() --53.) NOTE: removing this for now, because we don't this right now. This was used during our testing with the SQL Alchemy
#     return {"data": posts} --53.) NOTE: removing this for now, because we don't this right now. This was used during our testing with the SQL Alchemy

# 2.) New path operation. This one represents retrieving a bunch of social media posts from our application. So in this case, we know, there's two things that we need. So the first
#   thing is our function, our path operation function. The name of the path operation function will be "get_posts" since we're going to be retrieving a bunch of posts.
# We have to pass in our decorator, like we did before which is "@app.get()".So, we used the "get" HTTP method since we want to retrieve data.
# NOTE: There's one thing to know, and it's about how Fast API works is that when anytime we send a request to our API server, it's going to actually go down the list of all of our
#   path operations. And then it's going to find the first match, and as soon as it finds the first match, it's going to stop running our code. This case is when both of our path
#   are the same for example: If the URL on the decorator of "def root()" and "def get_posts()" are the same, then if we try to run our server and search this URL ("/"), we get the
#   return value of the "def root()". This happens because the "def root()" happens to be listed on top of that function where they both have the same URL.
#   17.) Using cursor.execute() to actually make a query
# 40.) NOTE: We commented out the regular raw SQL command because we want to use ORM to make requests and retrieve data from database.
#   NOTE: Anytime we want to work with the database always remember, we have to pass this: "db: Session = Depends(get_db)" in to the path operation function. So this going to make it
#       a dependency. And you'll see by doing it like this, it'll make testing a lot easier.
# 60.) NOTE: This after 59 where we inserted all the response_model on each of the decorators. But when it comes the getting all posts operation, there's an error.
#   So what it exactly is happening because we are returning a list of posts? And it's trying to shape that into on individual post. We got a list of posts, we should be sending
#   back a list of our schemas.Post. So how do we do that? Can we just put a bracket or some like that, will that work? --No, it didn't solve the error.
#   So how can we specify we want a list of posts? Answer: Well, we have to import something from the "typing" library. So we have an "Optional" from typing library and
#   we can also import "List". So now, after applying the "List" to our response_model = List[schemas.Post], the path operation function successfully retrieve and respond the data back
# #   to the user/front-end/client
# @app.get("/posts", response_model = List[schemas.Post]) # NOTE: Get request - Getting/Retrieving all the Posts  # NOTE: After 71, Transferred to routers>post.py
# def get_posts(db: Session = Depends(get_db)): # NOTE: After 71, Transferred to routers>post.py
    # cursor.execute("""SELECT * FROM posts""") --Because of 40
    # posts = cursor.fetchall() --Because of 40
    # print(posts) --Because of 40
    # posts = db.query(models.Post).all() # This is the if we're fetching data through ORM # NOTE: After 71, Transferred to routers>post.py
    # return {"data": "This is your posts"} -- before, We're updating this to return my_posts
    # return {"data": my_posts} # What's going to happen is Fast API is great because if we pass in an array like this, it'll automatically serialize it or convert into JSON Format
    # return {"data": posts} # We're returning the fetched data from our PostgreSQL
    # return posts # 54.) Only returning the posts # NOTE: After 71, Transferred to routers>post.py

# 3.) New path operation. This one represents creating a post.
# Question: On using the "post" requst, how do we extract the data that we sent in the body? How do we retrieve that body data?
#   Answer: What we can do is within our path operation function, we can just assign it som variable. So, what variable do we want to store all that body data, we can pick any name
#       we want.
#       def create_posts(payload: dict = Body()) -- What this "Body" is going to do is, it's going to extract all of the fields from the body. It's basically convert it to a 
#       Python dictionary. And it's going to store it inside a variable named "payload". This "Body" is imported "from fastapi.params import Body"
# So, we're changing the return value from "return {'message': 'Successfully created posts}" to "return {'post': f'title{payload['title']}}". This is for us to experiment and
#   visualize how the code run if we return the the Body or send the data back that we created on our API server
# NOTE: This code below not only send data from/in the "Body" within a Postman request, we're also able to extract that data and send it right back to the user. Now in a real
#   application, we would take the data, and then we would normally store that data inside our database so that we can create a new post stored in the database. And then now anytime
#   the user tries to retrieve the post, we can fetch that data from the database (as of now on this part we don't have a database set up just yet.)
# We imported the "pydantic" (for our schema). So if we go here on our "create_posts" path operation, utlimately what we want to do is to tell the front-end what a "post" or
#   new "post" should look like, what data do we expect?
#   ANSWER: So, let's figure out what data we want for a specific post request: So two things that we want which are the title, which is going to have a string essentially. And
#       then we want the content, which is the content of the post, which is going to be some sort of string. And so we expect the user to send both of those things. And then
#       we don't really want anything else. We don't the user to send any other piece of data, we just want these two things. But we can put in any other pieces of data we want such
#       as including the category of the post, the number of vote/likes, it can also be a Boolean that kind of represents: "is this a published post? or do you want this to be
#       saved as a draft?" But as of now we just have to stick to "Tile and Content"
# def create_posts(post:Post) - So what's going to happen is, because we pass this into our path operation "def create_posts(post:Post)", Fast API automatically going to
#   validate the data that it receives from the client based off of this model "class Post(BaseModel):". So, it's going to check, saying, "Hey, does it have title? 
#   If so, is it a string? If the title doesn't exist, or if it's not a string, and maybe we pass an integer, then it's going to throw an error. It's also going to check for us
#   if contents are available. If it's available, it's going to make sure that it's a string. And if contents are not available, or if it's not a string, then its going to throw
#   an error." So, it's doing all of the validation for us and it's defining the schema of what it should look like for the front end, what kind of data should the front end send
#   to us.
#   NOTE: When we actually kind of extra that data and save it into "post", it actually stores it as a pydantic model. So, it's a specific pydantic model, and each pydantic
#       model has a method called dot dict or ".dict". So if we print post below, what we can do is if we ever need to convert our pydantic model to a dictionary, all we have
#       to do is write the name of the variable which is "post" then put method ".dict()" at the end which is like this "post.dict()". So after we hit send on the Postman,
#       for us to visualize the 2 situation where "post" is printed as it is as a pydantic model where it shows out the different properties from the model 
#       and the other one is converted the "post" to dictionary. And we can send back a dictionary if we want to, so we do return "data":post
# @app.post("/createposts") -- before, the Path/URL on this is replace because it's not following the best practice
# @app.post("/posts") -- If we take a look at our code, we can see that for our create post path function, we're not actually doing anything with the data, we're not actually saving the post anywhere
#   right now. We just print it out and then send it back to the user. So that's not how a real application would work. And so what we want to do is we want to start saving
#   these posts, we want to start turning this into a real fully functioning application. NOTE: Now ideally, we're going to save this within a database, because that's how any
#   application works. We want to take a post, we want to save it in database so that we can persist that data. However, we're not quite ready to handle working with the database.
#   NOTE: So what we're going to do is going to save the posts in memory. So, we just have to create a variable, just globally that's going to store all of our posts. Check #7
# 8.) Let's update our create post path operation function so that we can retrieve the "title" and "content" from our front end and then create a brand new post and store it within
#    our my_posts array. So how do we do that?
#       Answer: We already know that we can retrieve our post by referencing this post variable which is "post" because this will take our schema which we defined with pydantic.
#           It's going to store it within "post". And so this is still going to be a pydantic model. However, our array is going to be an array of dictionaries. So we have to
#           convert that to dictionaries. And we already know that we can convert any pydantic model to a dictionary by doing ".dict()"
# 12.) We should send 201 status code after creating an entity. How do we change what the default status code is for a specific path operation?
#   Answer: Inside the decorator, we need to pass in another option which will be status_code=status.HTTP_201_CREATED
# 41.) NOTE: We commented out the regular raw SQL command because we want to use ORM to make requests in the database which is to create a post for this specific operation.
#   NOTE: Anytime we want to work with the database always remember, we have to pass this: "db: Session = Depends(get_db)" in to the path operation function. So this going to make it
#       a dependency. And you'll see by doing it like this, it'll make testing a lot easier.
#   NOTE: So first of all, we have to make sure we import that "models.py", so we can access "models.Post" in this case to access that specific model.
#   NOTE: And then we have to pass in the properties of the brand-new post that we want to create. And so what are the properties? So we need the title, content and the published
#       And that's all going to be derived from the request that we get, which is going to be stored in the "post" object. So we can reference all of those fields.
#   NOTE: So let's create a new post through Postman
# 42.) NOTE: So the create_post operation function is successfully working. There's one thing we'd like to change. So our model from models.py has only a couple of fields,
#       and the user only has to really pass in 2 to 3 fields which is title, content and published. It's not a big of a deal. Imagine if we have a model with 50 fields, and
#       there's no limitation. We can put many fields as we want. Well, then things are going to get a little bit more difficult. Because we have to extract all the fields from our
#       schema and then we have to kind of pass it in. So we have to say, title=post.title, content=post.content, published=post.published. And now, if we have 50 fields, we're
#       going have to do that 50 times. And there' actually a much easier way to do it. And the way to do this is, we have access to the post object which is a pydantic model.
#       So it's going to ensure that it mathces the schema that we set. We want to say "post.dict()" and after requesting to the postman, this will print a post in dictionary format
#       on our Terminal. However, we need to be able to automatically take that dictionary and convert it to as our model format from models.py, instead of having
#       'title': 'welcome to funland', it's going to be title=post.title... So how do we do that? Answer: All we have to do is unpack the dictionary. 
#       NOTE: By doing this print(**post.dict()) and it's going to put it into this exact same format "title=post.title, content=post.content, published=post.published"
#       so that format will be removed and will be replaced by this "**post.dict()". And this should ultimately do the exact same thing. Except now if we go back to our database
#       or our model from models.py and add an extra fields, then it's going to automatically unpack all of those fields for us. So we don't have to manually type it out.
# 56.) ***SPECIAL NOTE: After inserting response_model=schemas.Post in the decorator, and when the author execute its code, it got an error which says, "value is not a 
#   valid dict (type=type_error.dict)". But when I test the create_posts there's no problem. But on the tutorial, as per author, it's look like Pydantic is saying that,
#   when we try to send the response, the data we got back was not a valid dictionary. And because Pydantic class works with dictionary, it takes a dictionary and then converts
#   it to that specific model. So what exactly happened here? Why is this causing an error? Answer: If we look at the documentation, and if we go under SQL relational database,
#   it says that for our models, our pydantic models, we have to add this extra "class config: orm_mode = True". Pydantic's orm_mode will tell the Pydantic model to read the
#   data even if it's not a dict/dictionary. And that's because when we make this query new_post, this is actually not a dictionary, it's a SQL alchemy model. So, Pydantic
#   has no idea what to do with the SQL Alchemy model. So, we have to tell it to actually convert this SQL Alchemy model to be a Pydantic Model.
# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # NOTE: Create request - Creating a post # NOTE: After 71, Transferred to routers>post.py
# def create_posts(payload: dict = Body()): -- before
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): # Instead of extracting the payload, we're going to reference that 'Post' Pydantic Model, and we're going to save this as a variable 'post' # NOTE: After 71, Transferred to routers>post.py
    # print(payload) --before
    # print(post) # This is what we can and print on our terminal "print(post.published)" , "print(post.title)", "print(post.content)"
    # print(post.dict()) ---This line will not be used for now as we try to retrieve our data from PostgreSQL (because of # 18)
    # We are appending a new post to our my_posts and for our newly created posts that will be appended we'll use randrange to generate a random id. So this is going to ensure
    #   that every entry is unique for development purposes.
    #   NOTE: We'll append that to the array. And then here's the thing when it comes to how a usual API works is that when a front end sends the data to create a new post, after
    #       we create the post stored in our database, we should send back the newly created post, including the brand new ID. So let's send that back, so in this case, we're going
    #       to send back this return {"data": post_dict} because this is going to be the brand new post that we add to our specific posts array.
    # post_dict = post.dict() ---This line will not be used for now as we try to retrieve our data from PostgreSQL (because of # 18)
    # post_dict['id'] = randrange(0, 1000000) ---This line will not be used for now as we try to retrieve our data from PostgreSQL (because of # 18)
    # my_posts.append(post_dict) ---This line will not be used for now as we try to retrieve our data from PostgreSQL (because of # 18)
    # return {"message": "Successfully created posts"} --before
    # return {"post": f"title: {payload['title']} content: {payload['content']}"} -- before , for now we just use {"data" : "post"}
    # return {"data": "post"} --before
    # return {"data": post} # Here we are returning the data:post as dictionary on our Postman console -- before
    # return {"data": post_dict} ---This line will not be used for now as we try to retrieve our data from PostgreSQL (because of # 18)
    
    # 18.) NOTE: Working on inserting a new post into our database. Note the %s are just variables/placeholders and then the values we want to pass into that will be passed into
    # the next parantheses as the second parameter into the execute method.
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)) #This line prevents from SQL injection --Because of 41
    # new_post = cursor.fetchone() --Because of 41
    # conn.commit() # This will push the changes out or making the brand-new post reflecting on the database. --Because of 41
    
    # new_post = models.Post(**post.dict()) # NOTE: After 71, Transferred to routers>post.py
    # db.add(new_post)        # These 3 lines fixed the issue. Becuase after creating a post through Postman the new_post doesn't reflect in the database. # NOTE: After 71, Transferred to routers>post.py
    # db.commit()             # These 3 lines fixed the issue. Becuase after creating a post through Postman the new_post doesn't reflect in the database. # NOTE: After 71, Transferred to routers>post.py
    # db.refresh(new_post)    # These 3 lines fixed the issue. Becuase after creating a post through Postman the new_post doesn't reflect in the database. # NOTE: After 71, Transferred to routers>post.py
    # return {"data": new_post} # This will return the value to the user or front end
    # return new_post # 54.) Only returning the new_post # NOTE: After 71, Transferred to routers>post.py

# 9.) The next function we want to implement is retrieving one individual post. So keep in mind this is singular since we'll be retrieving individual post.
#   The decorator is going to /posts/{id} because the user is going to provide us the ID of the specific post that they're interested in. And so that's going to get embedded in the
#       URL. So they'll send a get request to /posts/{id}. So if they want to see the information for post one, then they'll pass in a value of one. And what this is actually
#       referred to the proper terminology for this is that this is called a path parameter. So this ID Field represents a path parameter. And so what we can do is Fast API will
#       automatically extract this ID. And then we can pass it right into our function.
#   So we're testing it on the Postman. So it looks like we successfully able to extract the ID, the path parameter that was passed into the specific URL that the user sent
#       a request to. So we now have access to that point, we can just find whichever entry in my_posts has that specific ID.
#   NOTE: Now we have to implement the logic for actually getting that post. And so there's many different ways of doing this. And this is probably not the best way of doing this.
#       There's more better ways of grabbing the information. However, keep in mind the code is going to be changed later on once we start working with the database. At this point
#       is just basic Python logic. And we do want to keep in mind that this may not be the best practice or the best way of retrieving an individual post. We're just going to create
#       a simple function. And it's going to be called find_post check #10
#   NOTE: Keep in mind that anytime we have a path parameter, it's always going to be returned as a string, even if it represents an integer or a number. We always have to manually
#       convert it ourselves.
#   NOTE: If we input a path parameter that is a string, then it will return an Internal Error on the Postman console since we're trying to convert an actual string to an integer.
#       Instead of sending back a nice built-in response, we just get an internal server error. And the user has no idea what exactly is wrong. So we want to provide a feedback.
#       So how can we perform some kind of validation to ensure that whatever data that's passed into this path parameter can actually be properly converted to an integer?
#       Answer: We can perform validation with Fast API. For ID, what we can do is we can say we wan this to be an integer. (id; int) - So what's going to do is first of all 
#       it will validate that it can be converted to an integer. And then it'll automatically convert it to an integer for us. So we no longer have to convert this ourselves.
#   NOTE: So this is our 3rd function within our CRUD App. So we just got two more, we got to handle updating and deleting posts.
#   We need to manipulate the respond that we're getting after retrieving an ID that has not been there instead of getting response of {"post_detail": null}.
#       So, we're importing Response -- from fastapi import FastAPI, Response, this the hardcoded way of notifying our error:
#           response.status_code = status.HTTP_404_NOT_FOUND
#           return {"message": f"post with id: {id} was not found"}
#       We can also raise an HTTP Exception
#   NOTE: 19.) Getting an individual post from the Postgres database or from the table under fastapi database.
#   43.) NOTE: Handle querying for an individual post. So, we will comment out the regular raw SQL Command because we want to use ORM to make requests in the database which is to
#       retrieve an individual post from the database. So the filter on the line db.quert(models.post).filter(models.Post.id == id) is equivalent to WHERE
# @app.get("/posts/{id}", response_model=schemas.Post) # NOTE: Get Individual Post request # NOTE: After 71, Transferred to routers>post.py
# def get_post(id: int, db: Session = Depends(get_db)): # NOTE: After 71, Transferred to routers>post.py
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id))) # NOTE: We need to convert the id which is an integer into string after passing in the execute --Because of 43
    # post = cursor.fetchone() --Because of 43
    # print(id) 
    # post = find_post(id) --- This will be removed because we're fetching data from PostgreSQL
    # post = db.query(models.Post).filter(models.Post.id == id).first() # NOTE: After 71, Transferred to routers>post.py
    # print(post)
    # if not post: # NOTE: After 71, Transferred to routers>post.py
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found") # NOTE: After 71, Transferred to routers>post.py
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    # return {"post_detail": f"Here is post {id}."} --before
    # return {"post_detail": post} --Because of #54
    # return post # 54.) Only returning the post # NOTE: After 71, Transferred to routers>post.py

# 11.) NOTE: Example situation where we can get an error. The path parameter that we just apply in this route coincides with the ("/posts/{id}") since the variable latest could be
#   treated as the {id} and it does technically match on it once we "get" request. It then tries to perform validation on ID which is in this case, it's going to end up
#   being latest. And then it's going to throw an error because latest can't be converted to an integer. So this is the example of where order matters. To solve this issue, what
#   we want to do is to move this function before the path operation function @app.get("/posts/{id}")
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

# 13.) Deleting a post request. Then let's create a new request on the Postman. Then change the default status_code.
#   NOTE: We get an error after we inputted an ID that has not been on the array or my_posts. So we get an 500 error because None type object cannot be interpreted as an integer.
#       So since we tried to grab the index from this find_index_post, it's going to return nothing because there's no post that has an ID of 5, and then we try to pop with an
#       index of non that creates an error. So, we're putting a simple If-Statement scenario below.
#   NOTE: 20.) Deleting a post from our database using the PostgreSQL
#   44.) NOTE: Deleting an individual post. So, we will comment out the regular raw SQL Command because we want to use ORM to make requests in the database which is to
#       delete some post.
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # NOTE: After 71, Transferred to routers>post.py
# def delete_post(id: int, db: Session = Depends(get_db)): # NOTE: After 71, Transferred to routers>post.py
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id))) --Because of 44
    # deleted_post = cursor.fetchone() --Because of 44
    # conn.commit() --Because of 44

    # index = find_index_post(id) --- This will be removed because of #20

    # if index == None: --- This will be removed because of #20

    # post = db.query(models.Post).filter(models.Post.id == id) # NOTE: After 71, Transferred to routers>post.py

    # if deleted_post == None: --Because of 44
    # if post.first() == None: # NOTE: After 71, Transferred to routers>post.py
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.") # NOTE: After 71, Transferred to routers>post.py
    
    # post.delete(synchronize_session=False) # So this is going to delete the post, but remember to actually changes, we have to do db.commit() # NOTE: After 71, Transferred to routers>post.py
    # db.commit() # NOTE: After 71, Transferred to routers>post.py

    # my_posts.pop(index) --- This will be removed because of #20, executing SQL commands to delete a post
    # return {'message': 'post was successfully deleted'} -- since there'll be no content after deleting the post then it will not return any value
    # return Response(status_code=status.HTTP_204_NO_CONTENT) # Still no data comes back after this change because we requested a delete request # NOTE: After 71, Transferred to routers>post.py

# 15.) Making Update Post request. So we're just going to copy the URL from the delete post because it will follow the same structure
#   So, we're going to pass the ID of the post that we want to update. Since we're updating a post, we need our front end or in this case, Postman,
#   to actually send the data that we want to update with. So since we're working with posts, which has a simple structure, we just have title, content, published, rating (will be removed later)
#   So, we can go to our "Body" (on the Postman), and go to "raw" then choose JSON format. This is just like when we're trying to create a post
#       we just have to pass that data in the "Body".
#   This update request is going to update the title. NOTE: We're going to use "put" method. So with "put" method, we have to actually pass in the data for all of the fields.
#       So, we want to pass in what the final post will look like after we update it. We don't want just to pass in the fields that we want to update.
#       For example: On post 1 we have the title and then we have the content. So, if we wanted to update just the title, we would make sure that we pass
#       the content as well. So let's copy the properties of post 1 on the Postman
#   NOTE: Because we're receiving data from the front end, just like we did for creating post, we want to make sure that it adheres to a very strict structure.
#       So we want to use our schema again, so that the front end can't just send whatever it wants to. Now we can create new model called "class UpdatePost". Then
#       Then we can pass in all the fields that we expect. However, it's going to be the same as the "class Post" because we expect the title, content and any other fields depending on what we
#       want. In this case, it's going to be a post and there's no need to create a new schema or structure we can just use the pre existing schema.
#   NOTE: What we're going to do now since the request successfully executed is we need to find the index of that post with this specific ID the same thing on what we did delete function.
#       This is to notify us a correct and specific error instead of a default response.
#   NOTE: *** That's going to wrap up all of our CRUD Operations. So we can see that building out an API, building out our CRUD functionality  is fairly straightforward within FastAPI
#   NOTE: 21.) Updating a post on the PostgreSQL database
# 45.) NOTE: Updating an individual post. So, we will comment out the regular raw SQL Command because we want to use ORM to make requests in the database which is to
#       update post.
# @app.put("/posts/{id}", response_model=schemas.Post) # NOTE: After 71, Transferred to routers>post.py
# def update_post(id: int, updated_post: schemas.PostCreate, db : Session = Depends(get_db)): # NOTE: After 71, Transferred to routers>post.py
    # print(post)

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id))) --Because of 45
    # updated_post = cursor.fetchone() --Because of 45
    # conn.commit() --Because of 45

    # index = find_index_post(id) --- This will be removed because of #21

    # post_query = db.query(models.Post).filter(models.Post.id == id) # NOTE: After 71, Transferred to routers>post.py

    # post = post_query.first() # NOTE: After 71, Transferred to routers>post.py
    # if index == None: --- This will be removed because of #21
    # if updated_post == None: --Because of 45
    # if post == None: # NOTE: After 71, Transferred to routers>post.py
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.") # NOTE: After 71, Transferred to routers>post.py
                            
    # post_dict = post.dict() # This is going to take the data we received from our front end, which is stored in post. And it's going to convert it to a dictionary -- Because of #21
    # post_dict['id'] = id # So we're going to se the ID inside this new dictionary to be that ID. -- Because of #21
    # my_posts[index] = post_dict # We're going to pass in the index of this specific post we want to update -- Because of #21
    # return {'message': 'updated post'} # The message is hardcoded --before
    # return {'data': post_dict} -- This will be removed because of # 21

    # post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False) --one of the ways of updating a post
    # post_query.update({**updated_post.dict()}, synchronize_session=False) # NOTE: After 71, Transferred to routers>post.py

    # db.commit() # NOTE: After 71, Transferred to routers>post.py
    # return {'data': post_query.first()} --Because of # 54
    # return post_query.first() # 54.) Only returning the post # NOTE: After 71, Transferred to routers>post.py

# Special NOTE: 4. (This is from word)	We’re going to make one slight change to how we structure our code. And what we want to do is instead of just having our main file within our base project 
    # directory, we want to actually create a folder called “app”. So, that’s going to store all of our application specific code, and then put that main file in there. 
    # But we do have to change a couple of things to make sure that it doesn’t actually break anything. NOTE: Python has a concept of packages, and a package is nothing more 
    # than a fancy name for a folder. However, for something to properly act as a package, Python requires us to create a dummy file. And this file is called “__init__”, 
    # and this is going to turn this into a proper Python package. Just know that we have to add this file, and we don’t have to put anything in the file. But anytime you 
    # create a new folder, just make sure you create a file with this exact name, and that’s going to ensure that it is in fact a Python package. So now that this is an actual 
    # Python package, we can just drag our main file into our app folder. And to run this app we just have to add the folder where the main file is located
    # which will become : uvicorn app.main:app --reload

# 62.) Just like we did with posts, we’re going to create a new path operation for creating a new user which is "create_user". And so just like we have for creating a post,
#   we're going to copy the decorator from the "create_post" function and we'll rename it. So it's going to be a post request, but it's going to be sent to the URL of users
#   because we're no longer working with posts. And keep in mind, we get to select whatever URL or path we want to use. And anytime you create something, remember,
#   the status code should always be the default 201. And we'll get rid of the response_model for now to keep things simple. Now, we're ultimately going to be using our
#   database to create a brand-new user. So let's go ahead and copy this "db" or "db : Session = Depends(get_db)" right from all of the other path operations, because
#   that's going to have to go in the function since this db instance will be the one to talk to the PostgreSQL as we execute the create_user function in our code.
#   And then anytime we want to receive data from the user because the user is going to send the email he wants to register with as well as his/her password in the body
#   of the request, it always makes sense to define a specific schema so that we can ensure that the user does provide both of those. So just like we did posts,
#   NOTE: we're going to create a brand-new schema for create_user on the schemas.py file (#63).
# 64.) So after creating 63.) class UserCreate(BaseModel), we can now use that schema on our "create_user" function which will be "schemas.UserCreate". And so the email
#   address and the password is going to be stored in an object called user, and this is going to be a pydantic object as well.
#   NOTE: If you forgot how to save data to the database or create something with SQL Alchemy, just go ahead and take a look at the create_posts function. And we can
#   essentially just copy the lines which are the db.add(new_post), db.commit(), db.refresh(new_post). And we're just going to rename a few things.
#   NOTE: On the models.User(**user.dict()), what we want to do is we want to take the user that we get back from our schema, and convert it to a dictionary and then
#   unpack that dictionary. Then we're going to add it to our database. We're going to commit it, then we're going to refresh it so we see the brand-new user.
#   And then we can go ahead and just return new_user. Then let's test it in on our Postman, so it runs successfully and added the new user in our database whic is under
#   users table (PostgreSQL). After testing our email field with random texts, so it clearly didn't pass since it's not a valid email format.
# 66.) Inserting the schemas that we set for our response_model for this path operation which is from 65) class UserOut(BaseModel). The purpose of this is to return
#   the data back to the user/client that they registered on while leaving the password out in order to avoid disclosing their password after they registered.
# 68.) NOTE: After setting up the "bcrypt" at 67, we have to do a couple of things. And so before we actually create the user, we need to actually create the hash of the
#   password. So the first thing is we're going to has the password which can be retrieve from "user.password". And so how do we exactly do that? Answer: What we can do is
#   all we have to do is reference that password context which is the pwd_context and we call the hash method, and then we just pass in the "user.password". And we can store
#   this in a variable called "hashed_password". And then we're going to do here is we're going to take the "user.password" and we're going to set that now to the new hased
#   password. So that's going to update the Pydantic User Model. And then at that point, we can just leave everything as is. So we hash the password, so we got a hash, and then
#   we stored it under "user.password", and then everything else can just be kept the same. So let's try this out. >> Then it runs successfully and the password is now secure
#   and hashed for the recent user that registered after this update. So, the hackers will onyl get access to hashed password, and they can't exactly convert it back to the
#   original password. That's the great part about hashing. It's a one way street. we hash it, we only get the final password, but we can never put it back into a function
#   to convert it back to a password. NOTE: Now, one thing we want to do is we want to extract all of the hashing logic and store it in its own function, so we're going to create
#   a new file. And we can call this "utils.py" file. This file is just going to hold a bunch of utility functions.
# 70.) So we now, applied the changes from 69
# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut) # NOTE: After 71, Transferred to routers>user.py
# def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)): # NOTE: After 71, Transferred to routers>user.py
    # hashed_password = pwd_context.hash(user.password) --Because of 69 from utils.py
    # hashed_password = utils.hash(user.password) # Changes from 69 # NOTE: After 71, Transferred to routers>user.py
    # user.password = hashed_password # NOTE: After 71, Transferred to routers>user.py
    # new_user = models.User(**user.dict()) # NOTE: After 71, Transferred to routers>user.py
    # db.add(new_user) # NOTE: After 71, Transferred to routers>user.py
    # db.commit() # NOTE: After 71, Transferred to routers>user.py
    # db.refresh(new_user) # NOTE: After 71, Transferred to routers>user.py

    # return new_user # NOTE: After 71, Transferred to routers>user.py

# 71.) We'll create a new path operation, and let's call it "get_user()". Before we do that, we also going to setup the decorator. So this is going to be a
#   "get" operation because we're going to retrieve the information about a specific user. And the specific path is "/users/{id}". SO kind of like how we did when it comes
#   to retrieving a specific post, and we're going to pass in the ID in the URL. And then we have to extract the ID, and we're going to make sure that we validate it as an integer.
#   And the next thing that we have to do is since we're going to be interacting with the database, we need our "db" or "db: Session = Depends(get_db)" right here.
#   And in our actual function, we're going to do a quick query. And because there should be only be one user with a specific ID, we're going to just grab the first one 
#   with ".first()", so we don't spend extra resources looking through the rest of our database. And we're going to store this in a variable called user.
#   NOTE: So we test it successfully. However, there's one little issue. First of all, we should not be getting the password. We never want to return the password to the user,
#   and the user already knows his/her password. So we're going to filter out that specific field which is the "password" field. Fortunately for us, if we go to our schemas,
#   we've actually defined a schema for the "UserOut". So this is going to be any information about the specific user except we're extracting out the specific password.
#   And so we can just set the response_model to be "UserOut". After testing, now the password field has been finally removed.
#   NOTE: Now that we've added a couple of path operations for users, if you take a look at our main.py file, it's starting to look a little cluttered. And we'll see that
#   we've got all of our path operations for handling CRUD operations for posts. And then you'll see that we also have all of our path operations for working with users.
#   So that's creating users, as well as retrieving a user by ID. And this is a little messy. And as we keep adding more and more path operations, it just seems almost
#   unmanageable to keep everything in a main.py file. And instead, we want to break it out and create two separate files. And one file is going to be for all of the routes
#   or path operations that work and deal with posts. And then we want a separate file that will handle all of the path operations for working with users. And it's not quite as
#   simple as just moving these path operators into different files, we do have to learn about something specific to FastAPI. ANd this is nothing unique about FastAPI,
#   we'll see that every single web framework is going to have a way to kind of accomplish this. And it usually involve something called routers. So we'll take a look at
#   routers in this section and how we can use them to actually split up all of our path operations so that we can organize our code a little bit better. And so what we're going
#   to do is we're going to create a new folder and created 2 new files inside this new folder which is called "routers". The files are post.py and user.py. So what we're going to
#   do is to copy all of those operations related to post and user to their designated .py file
# @app.get("/users/{id}", response_model=schemas.UserOut) # NOTE: After 71, Transferred to routers>user.py
# def get_user(id: int, db : Session = Depends(get_db)): # NOTE: After 71, Transferred to routers>user.py
#     user = db.query(models.User).filter(models.User.id == id).first() # NOTE: After 71, Transferred to routers>user.py
#     if not user: # NOTE: After 71, Transferred to routers>user.py
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist.") # NOTE: After 71, Transferred to routers>user.py
    
    # return user # NOTE: After 71, Transferred to routers>user.py