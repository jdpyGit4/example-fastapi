from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2 #110
from psycopg2.extras import RealDictCursor #110
import time #110
from .config import settings

# 26.) NOTE: It’s already set up in the “database.py”. Just for now, we want to assume that it’s more of just a cut and paste job. The only thing that really
#   matters that we’re going to be changing is to be that Postgres URL. But everything else for pretty much every project, we can just copy and paste to this entire code
#   And now within our database.py file, that's all we have to do.

# 22.) So, this is the format of a connection string that we have to pass into SQL Alchemy
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>' -- This is an example
# NOTE:  It's never good to hardcode the values below somewhere in our code because now you've got our password stored in our code and it's going to get checked into GitHUb,
#   and then anyone can see it. So this is bad practice. However we will change this in the future.

# 118.) So we have to make sure we actually update that to use the environment variables. So we're going to change this to be an "f" string. Everthing still works. So we
#   access to our database and it's now working just fine. But there's a few other things that we want to update. And keep in mind, if we're using Postgres driver to actually
#   connect and make queries, then we would just update it here with the "settings.whatever_properties_necessary".
#   NOTE: So if we go to our "oath2.py" file, we can now change those credentials for our JWT into environment variables (this will be 119).
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:diamondback@localhost/fastapi' --Because of 118
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# 23.) We have to create an engine. So the engine is what's responsible for SQl Alchemy to connect to a Postgres database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 24.) However, when we actually want to talk to the SQL database, we have to make use of a session. NOTE: Keep in mind when we're creating or use the "create_engine" function,
#   so, if we're using a SQLite database, we have to pass in this option as the second paramater : "connect_args={"check_same_thread": False}"
#   So, this is the full line: engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) - This is something that's exclusive to SQLite, because
#   it's just running in memory. We don't need to do this for Postgres, and we don't need to do it for any other SQL based database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 25.) So, we have to define our base class. And so all of the models that we define to actually create our tables in Postgres, they're going to be extending this base class.
Base = declarative_base()

# 29.) NOTE: So if we go back to our documentation, the last thing that we have to do is we have to create this dependency.
#   The purpose of this is that the "session" object is kind of what's responsible for talking with the databases. And so we create this function where we actually get a connection
#   to our database, or get a session to our database. And so everytime we get a request, we're going to get a session, we're going to be able to send SQL statements to it.
#   And then after that request is don, we'll then close it out. And it's more efficient doing it like this, by having one little function, and we could just keep calling this
#   function every time we get a request to any of our API endpoints.
# 30.) NOTE: So now that we got our dependency to actually get that session, for all of our path operations, where we want to perform some sort of operation on the database.
#   What we're going to do is with inside the path operation function, we're going to pass in another parameter. It's going to be "db: Session = Depends(get_db)".
#   Keep in mind that it's going to create that session to our database so that we can perform some operations and then close it once that request is done. And then we can repeat
#   that process for every single one of our path operations. Or anytime we send a request to any API endpoint, we're going to have this being passed into the path operation
#   function so that we can create that connection and then close it out.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 110.) Cleaning the "main.py" file so we transferred this code that will connect our code to our database using raw SQL Command. So here we imported psycopg2 and also the time.
#   To avoid the errors. And comment all of the lines because we're not going to use it anymore.
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='diamondback', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() # Going to be used in executing SQL statements
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)