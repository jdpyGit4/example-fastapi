from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# 46.) NOTE: This is from the main.py file.
# class Post(BaseModel): # I didn't notice when this one got removed???
#     title: str
#     content: str
#     published: bool = True

# 47.) We're going to restructure this a little bit which is the class from 46. Remember, these are regular Python classes. And so we get all of the abilities that we have
#   when it comes to inheritance, and when it comes to working with these classes. So what we're going to do is, we could define a couple things, we could have one for
#   create post. And then this is going to have all of the fields that we need from the user when it comes to creating post. 
#   And in this case, there wouldn't be a default value for published just like this bool = True.
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool

# 48.) We also ned to handle updating posts. And so we could create another model for that. On this case, we could call it UpdatePost. And when it comes to the fields that
#   we use for an update post, it would be the same exact thing. And in this case, there wouldn't be a default value for published. Because we want them to explicitly provide
#   each column. And so at this point, we could then have two different classes for each specific request. And that's perfectly valid use case because when it comes to creating,
#   they should provide a certain amount of fields. And then updating it might be completely different. Because let's say in our application, we wanted to make it so that
#   the user can't ever update a post, they can only update one property. And that's the published, so they can just change whether it's published or not. We could remove
#   this title: str and content: str. And this is going to make it so that the user isn't allowed to provide any other fields. They can only pass the published field.
#   So that's why we would want to create different models for each of the different requests. But what the author would like to do instead of having one for create_post,
#   one for update_post and then one for the response, what we're going to do is we're actually going to delete all of these which are the 47 and 48
# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool
    
# 49.) We're going to create a class called PostBase(Basemodel). So this is just a regular class, we can just copy all of these fields. And then we can extend that class
#   NOTE: 51 to 52.) And that way, we can just piggyback off of this PostBase model, and then just create brand-new models based off of this.
#       So what we're going to do is going into our main.py file
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# 50.) We can take that PostBase class, and we can extend say: class PostCreate(PostBase) - extending the PostBase. And so it's going to by default automatically inherit all
#   of these fields. And so we can just say, for creating, we can just say pass, which means it's just going to accept whatever post bases. So PostCreate is essentially the
#   same thing as post base. We can create a brand-new one...
class PostCreate(PostBase):
    pass

# 65.) This class is for our response_model so that we won't be sending back the user's password after they registered. So we create a class UserOut(). And so this is going to
#   be the shape of our model when we send back the user to the client that requested and it is going to extend BaseModel as well. And here, we're going to send out a couple
#   of things. So there's going to be an ID, and the user should know his/her ID and email. And then we'll just leave out the password because we won't ever send it back.
#   But just like we did with the Post model, remember, this is going to be a SQL Alchemy model that we get. And we need Pydantic to convert it to a regular Pydantic Model.
#   So we need this configuration which is class Config: from_attributes = True. So on the path operation of our create_user, we can set the response model as the "UserOut".
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        from_attributes = True


# 51.) We can create a brand-new one called class PostUpdate(PostBase) - extend PostBase. And we can say for updating, we can pass in whatever specific fields we want to
#   add in as well. But it gives us flexibility because we can make use of inheritance. So for now, we're going to remove PostUpdate, and we're just going to keep it as
#   PostCreate. Because updating and creating is going to be fundamentally the same.
# class PostUpdate(PostBase): --Because of 50 and that statement at the end of 51

# 55.) Now, let’s actually define the what the response should look like. And we do that with our schemas, we do that with our Pydantic Model for creating posts,
#   which happens to just inherit from PostBase(BaseModel). So PostCreate(PostBase is just saying that we expect the title), we expect the content, published as optional
#   and if you don't provide then it's True. And so we already know how to work with that, let's create a brand-new class for the response. So, this handles the direction
#   of the user sending data to us which is the PostCreate(PostBase). So, we can create a brand-new class, we can call this PostResponse because it represents the response
#   or we can just call it Post. And then we're going to extend BaseModel because all of our Pydantic Models have to extend BaseModel. And then we have to do is we have to
#   specify all of the fields that we want in the response. And to actually define the Response Model, under a specific request, we'll start off with create request or
#   create_posts function on the main.py file. And then within the decorator, we just pass in another field. And this is called ResponseModel.
# 57.) So after tested out on the Postman, now it only returns the title, content, published. (Check 56)
# 58.) We know if we go to our Postgres database, we do have an ID field and a create_at field. So if we want to add those under class Post(BaseModel) and if
#   our front end wants those as well, we can add those. On the created_at field, what we can do better is to import "from datetime import datetime". And so now we can
#   say that the time, the created_at is going to be of type datetime. And so this is an extra little bit of validation to make sure that what we send back is an actual
#   valid datetime, and just make sure that we import it on this file: "from datetime import datetime"
#   NOTE: So now after adding those field, we now get the ID and the create_at as well. So this how we ultimately define the data that we send back, we can specify exactly
#   the fields we want. And that way, we can ensure we don't unnecessarily send data that shouldn't be getting sent. And we can do this with anything, we can just send back
#   the ID if we really wanted to. There's a lot of flexibility and a lot of power when it comes to defining our responses just like we had when it comes to defining our
#   requests. NOTE: And with APIs, always make sure we explicitly define the exact data we want to receive, and the exact data we want to send back to the client.
# 59.) NOTE: Before we move any further after #58, we'll see that there's a lot of duplication above. Because that Post model for the response, it needs title, content, and published
#   and then we're just adding ID and created_at. As the author said, when it comes to a real application, we're going to have so many more fields, so many more columns, and it
#   would be such a pain to have to repeat both of them. And that's why we ultimately created this class PostBase(BaseModel) because we can extend the PostBase class.
#   And what that's going to do is to cause us to inherit the title, content, and published fields because they're already defined in there. And so we can just remove that.
#   And so then we can just specify the ID and create_at, and then it's going to inherit the other three from the previous class which is PostBase(BaseModel)
#   So this is really no different than working with any other model in Python. We get access to all of the usual features like inheritance, so we can help reduce the amount
#   of code that we actually write. So from here, we update all of the other path operations as well.
# 101.) So we can add the owner_id at the "PostBase", "PostCreate", etc. But the first thing that we have to think about is, when we create a post, should we be passing in owner_id?
#   Answer: 100% absolutely could do that. And that actually does kind of make sense. So in that case, if we didn't want it to be available or require it for creating post, then we would
#   add it under "PostCreate" here as well. Or we could just add it under "PostBase" so that both of them inherit it. However, what we're going to do is we're actually not going to require
#   the user to provide the owner_id. Instead, what we're actually going to do is we're going to let the logic of our route to actually just grab the ID from the token, and then use that
#   as the field. So we don't actually need the user to pass that into the body. So we're not going to use that field or apply that field to either one of these classes, we're just going
#   to do it for "Post" class which is the one that's responsible for sending the post out. So we'll add a column here, and we'll call it owner_id. And now it successfully reflects on the
#   body.
#   NOTE: If we go to "Create Posts" real quick, and we create a post, we get a crash. So there's an issue with creatuing a post. And we're sure we can guess exactly what it is.
#       Take a look at the error when we try to create a post. It says that there's some kind of SQL error, and it says there's a null value in column owner_id. And that makes sense.
#       So we'll actually tackle this in the next video.
# 107.) After adding an "owner" property, we need to update our schema for "Post" class. We're now going to return a "User". And so here, what we would do is we would just add another
#   property called "owner". And then here, it would instead of returning an int or a string or anything like that, we can actually return a Pydantic model. So we can say we want to return
#   a "USER", but it looks like we don't have a user class, we have "UserOut" class. And then we "UserCreate" class. So which one do we actually want to return?
#   Answer: Probably "UserOut" because that's why we're returning and with the "UserCreate", it's for creating a user. And we notice that we get an error actually here, and that's because
#   this "UserOut" hasn't been defined at this point in the code. So we have to read python top down. And so "UserOut" is actually defined all the way down here. So if we wanted this to
#   work, we would have to move all of the user stuff up a level. And now the "UserOut" on the "owner" property doesn't have any error. And so now it automatically fetch the owner, and now 
#   it successfully return the information of of the users not just their ID but also their email and the date when their account was created at, we may not want that. But for now, this makes
#   sense, we could create anothe class to kind of narrow down the exact fields that we specifically wanted for this situation but for now it's good enough. These are all the information
#   that we want actually returned. So this is perfect. It's going to do this for every post. And if we try to get one post, it's also going to return that specific owner. Then it succesfully
#   return the owner of that post. NOTE: In reality, to get this functionality, once again, all we have to do was just create this "relationship" which is inserted on our "models.py" under
#   "Post" class which is this "owner = relationship("User")". And so once SQL Alchemy understands the relationship, it's going to fetch that piece of information for you from the user model.

# class Post(BaseModel): --Because of 59
class Post(PostBase):
    id: int
    # title: str --Because of 59
    # content: str --Because of 59
    # published: bool --Because of 59
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        # 57.) NOTE: "orm_mode" has been renamed to "from_attributes"
        from_attributes = True

# 128.) We'll create a new schema. We can call this as "PostOut()" and it's going to extend PostBase - "PostOut(PostBase)". And what we're going to is to try to match
#   the response that we have if we don't apply the response_model=List[schemas.Post]. We need to have something that will represent the post object just as this result below.
#   And then we're going to have a field called "votes" which is going to be an integer. So here, we have somthing called "Post" and make sure to capitalize it because
#   our query for some reason returns it with the capital "P". So we want to reference that "Post" class above and store it under "Post" from this class PostOut(PostBase).
#   And then we expect something called "votes", which is going to be se to an integer. So let's try this out and let's get back to our "post.py" and to the "get_posts" router.
#   And apply the new schema "PostOut". So after testing this new schema, it was not successful. There are issues related to the title, content, etc. So the title and the content
#   are missing for both. So what did we do wrong here, this should have fixed our issue. So let's try adding this class Config even without the class Config it still properly working.
# {
#         "Post": {
#             "title": "Powerpuff Girls",
#             "published": true,
#             "id": 19,
#             "owner_id": 16,
#             "content": "Mojojojo",
#             "created_at": "2024-04-03T20:51:24.984934+08:00"
#         },
#         "votes": 0
#     }
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

# 63.) So just like we did posts, NOTE: we're going to create a brand-new schema for create_user on the schemas.py file. And we can call this UserCreate().
#   So there's going to be an email field, which is going to be a string as well as password field which is going to be of a type string. And when it comes to validating
#   the user, it's going to check to make sure that an email is provided and a password is provided. However, we can get a little bit granular than that. If we actually
#   go to the Pydantic documentation, we also have field called email string. But this is going to validate that the email property is a valid email. However, we need to have
#   the email validator library installed. But that should automatically have already been installed for us when we installed FastAPI with the all flag. 
#   So from the Pydantic library we're going to import email string which is this line : "from pydantic import EmailStr". So now, our "email" field is going to be an "EmailStr"
#   that's going to ensure that this is a valid email and not just some random text. Then back in our main.py file.
class UserCreate(BaseModel):
    email: EmailStr
    password: str



# 82.) Will create schemas for the login operation
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# 92) And so we’re going to do class Token(). So we can also set up a schema for the token data.
class Token(BaseModel):
    access_token: str
    token_type: str

# 93.) So we can also set up a schema for the token data, so that the data we embedded into our access token, so we can say "class TokenData". So we embedded id, and as of now,
#   let's set it as "Optional". And in our "oauth2.py", we created an access token function which is "def create_access_token", and (94) then we have to create a function to verify
#   the access token. So let's create the function
# 97.) Just changed the type of the id from str to int. And now it successfully created a post
class TokenData(BaseModel):
    # id: Optional[str] = None
    # id: str
    id: Optional[int] = None


# 123.) From 121. Now, there's going to be a couple things that we have to pass in. So since we expect the user to provide some data in the body, it usually means we want to define
#   a schema just so that we can ensure users/they send us the exact information. So let's setup our schema for voting. We'll create a class called "Vote" in our "schemas.py" file.
#   So the first field should be a post_id, which is going to be a type "int". And we're going to have a direction which is going to be an integer as well. So it's either zero "0"
#   or one "1". However, the author would like to be able to validate to ensure that it's only zero "0" or one "1". The author couldn't exactly figure out if there's a way to do that
#   in Pydantic. But one thing we can do is we can use "conint". So we'll import that from Pydantic automatically. And we can say "conint(le=)" which means "less than or equal to one".
#   So anything less than one is going to be allowed. The only problem with this is that allows for negative numbers but that's okay. And let's import our schema now.
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore
