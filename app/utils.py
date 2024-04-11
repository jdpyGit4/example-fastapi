from passlib.context import CryptContext # 67 This is from the main.py and got transferred in this new file

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #67 This is from the main.py and got transferred in this ne file

# 69.) And then we're going to define a function that we can call. We're going to call this function as "hash()", and it's going to take a password, which
#   is going to be of type string. And all it's going to is it's going to return "pwd_context.hash(password)" of whatever the password the user passes in.
#   And this way, we really extract and place all of the hashing logic into one file or one function. So we don't have to import all of those above into other files.
#   And then in our main.py file, we can import this "utils.py" file.
def hash(password: str):
    return pwd_context.hash(password)

# 83.) We're going to create a new function, that's going to be responsible for comparing the two hashes, or actually, 
#   it's going to take in the raw password, the password attempt, it's going to hash it for us,
#   and then it's going to compare it to the hash in the database.
#   plain_password - which is the password the user is trying to attempt, and then the hash password - which comes from the database.
#   And all we have to do is just return. And then we can reference the "pwd_content", so if we want to hash a password we just call the ".hash" method.
#   However, it's also got an another method for us which is verify. So it's going to perform all this logic for us. So we just pass in the plain password
#   and then we pass in the hash password. And it's going to figure out the rest.
#   NOTE: We might be thinking, what is the point of such a tiny function? Why don't we just include it it in our "auth.py"?
#       Answer: We 100% could because it's really two lines of code, it doesn't really make sense to store it in another file. However, then we also
#       have to import all of the "bcrypt" code. So we're just keeping all of the "bcrypt" logic in one file just makes things a little bit easier to manage.
#       But in our "auth.py" file we can import "utils" now. And we're going to run the "utils.verify"
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)