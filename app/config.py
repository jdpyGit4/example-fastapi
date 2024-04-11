from pydantic_settings import BaseSettings #(111)

# 113.) This is from 111
# 114.) So we clear out all the examples. And we're going to create one for all of the database related
#   stuff. NOTE: "database_name" - so this is the database within Pstgres that we're connecting to.
#   And we may be wondering why the port is set to a string but the reason why it's going to be set to
#   string is because if we actually take a look at our database connection, it just goes into a URL.
#   So we don't actually ever need to have it be an "integer". We need just to make sure that it's
#   a valid port number and then convert it back to a string. But that seems a little unnecessary at
#   this point. Then there's a secret key for our JSON Web Tokens. And we've got the algorithm for
#   signing our token, and also our access_token_expire_minutes. So if we save all of these, we could
#   get a bunch of errors because all of these have not been set. At this point, we could technically,
#   whether we're on a Windows or Mac, set these on our machine and get everything to work. But this
#   is an acceptable thing to do because that's a lot of work. And we want to simplify things. So what
#   we can actually do is within our FastAPI directory, we're going to create a new file called .ENV.
#   So this is kind of standard convention but this file is going to contain all of our environment
#   variables so we can set it much easier just by having a file do all of the work. So in production
#   we're not going to use this ".env" because on production we're going to actually set it on our 
#   machine (115). But in development, it's perfectly okay to just set everything in here. And so what
#   we're going to do is we're going to take all of those environment variables that we define below
#   to our "config.py"
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


# 116.) And now we have to tell Pydantic to actually import it from our ".env" file.
#   And the way to do it is inside the "Settings" class, and well create a class call "Config". And
#   under this class it will be the path of our ".env" file. See how easy it is to work
#   with environment variables, especially when we're allowed to set it on a file, so
#   that we don;t have to worry about setting it either in the terminal or on a Windows Machine
#   having to go through the GUI to do that. But one thing to keep in mind is that we never want to
#   check this ".env" file into Git. Because this has all the credentials for our development
#   environment, may be we don't want those to get out. And there's no need to ever check it into Git.
#   So if we create a Git ignore file, it would just ".gitignore" (117). We want to make sure that we
#   put in ".env". And we'll come back to the ".gitignore" file when we start working with Git in this
#   course. But we also want to make sure we remove anything with "__pycache__", "venv", ".env"
    class Config:
        env_file = ".env"

# 113.) This is from 112. So we're just importing this instance from the class that we created.
#   And so once again, it's able to perform the validation and it's going to report an error with
#   the path variable. So having it its own file is going to make things a little bit easier,
#   because then we could just go to the "config.py" file. And we'll know exactly, where to look for
#   all of our environment variables and all the configs related to our application. The last thing
#   we want to do, let's go head and actually figure out what environment variables we want to use moving
#   forward, and actually set this up. So we're going to clear out all that are under "Settings" Class (114)
settings = Settings()
