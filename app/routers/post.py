from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

# 73.) Last error that we see is that we don't have access to the app object. And so our instinct is to go to our main.py file and then import this "app = FastAPI()"
#   NOTE: And that's not exactly correct. Instead what we're going to do is we're going to make use of the routers that was mentioned earlier. And so from the FastAPI
#   library, we're going to import something called APIRouter. So, we'll say "router = APIRouter()". So we're basically creating a router object. And then what
#   we can do is we can replace the keyword "app" on our decorators because we don't have access to that in this file. And we just use the word "router".
# 76.) NOTE: But keep in mind that our API is very simple. Other APIs could have very long, complex routes that may not look as simple as ours. They could have multiple things 
#   and then having to kind of copy and paste all of that every single route can seem little unnecessary. And so anytime we’re working with routers, what we can actually do 
#   is we can pass in a parameter or method into the APIRouter function. And so, what we can say is prefix. And we're going to say that since every single route in this file
#   always starts with "/posts", we can say prefix = "/posts". And so now, anytime we see a "/post", we can just remove that from our route or decorator and just leave the
#   slash "/". And then when it gets to "/posts/{id}", this is where it gets a little tricky. But once again, we just remove everything but a slash "/". And so what this is saying
#   is that we're going to take "/posts" and append it with the ID "{id}". So nothing actually changes. It's just simpler way to do things so that we don't have to write "/posts"
#   everywhere. (This will be copy and paste in the user.py also which will be # 77)
# 78.) We're restructuring our FastAPI's interactive documentation by SwaggerUI through our routers. So, now we're adding a specific group name using "tags" to group the post operations
#   into one. This will be copied to "user.py" which will be # 79.
#   
router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

# 108.) And in this case, we've got our path operation of retrieving all posts. And what we want to do is, we want to let the user be able to kind of filter down on the post that they
#   want to see. And the first thing that we're going to do is we're actually going to allow them to specify how many posts they want to retrieve altogether. So we want to give them
#   the option to say, "Hey, we want 10 posts, or maybe we want 100 posts or maybe we want 50 posts", we should allow the user to define that. NOTE: And so to allow a query parameter,
#   we could just go into our path operation function and just pass in another argument. So we're going to do "question mark", then we give it the name of the query parameter. So this
#   is the key essentially, and we're going to call this limit. So this is going to limit the number of posts they get. And this is going to be of type int and the default value is 10.
#   And now, what we're going to do is we're going to print out limit. So the author will show us how to actually send that query parameter. So let's go to our "Get Posts" or getting aall
#   posts in Postman. And so to send a query parameter, it's very easy, we just type in a question mark, then we grab the name of the "query parameter" which is "limit". And then we set
#   it equal to whatever value we want to be - {{URL}}posts?limit=3, so if we want to get a limit of three, then hit send nothing should have changed in our code since we just want to print
#   the limit of our query to test if it runs successfully in the Postman. NOTE: So that's how we access query parameters in FastAPI. It's pretty simple, we just pass it in as another
#   argument into our path operation function. But let's actually set up our query so that it now takes into account the limit. And with SQL Alchemy, anytime we want to perform another
#   operation, we usually have a built-in method. So we're going to remove this ".all()" for now. And so if we want to limit the number of results, we just do ".method()" and then let's
#   see what methods we have at our disposal. Since we're looking for something that limits something, let's maybe check to see if there is a limit method and there is ".limit()"
#   then pass in our "limit" variable and then append the ".all()" again at the end. Then after testing, it responded correctly and successfully to our request with query parameters.
#   NOTE: What we want to do now is allow the user to skip results. So it grabbed depending on however Postgres has decided to return which is on the default, it's 10 posts, then
#   it grabbed the first 10 based off of some criteria. And if we actually take a look at our Postman, it probably not sorting right now based off of any specific field. We may want to
#   specify that. But what we're going to do is we're going to actually set the limit equal to two. And so we'll get the first two, however, Postgres determines what are the first two
#   it should send, so we get two. But let's say we want to skip over a couple of them, maybe we want to skip the first two, maybe we want to skip these two. Well, we want to be able to
#   send another query parameter called skip, so that we can specify how many we want to skip. And if we want to send more than one query parameter, we just do the "&" keyword, and then
#   we provide the next key-value pair. So it would be like skip equals two. So we're going to provide another argument into the function. And we'll call this "skip" and it's going to be
#   an integer. And the default is going to be zero because we don't want to skip anything by default. And to add this to our query, we use the keyword offset. So after testing it,
#   it allows us to skip over post. And so that's ultimately how we're going to implement "pagination" on the front end because the front end should be able to skip based off of what
#   page they're on. So if each page returns 20 results, and we want to go page 2, then we want to skip 20 results. If we want to go page 3, we would skip 40 results. 
# 109.) Now, the last query parameter we want to setup is a "search" functionality. We want the user to be able to search based off of some keywords in the title, or maybe even the content, 
#   depending on how we want to implement searching. For now, we're just going to say we'll be able search based off of the title. And the way that the search will work is we'll have another
#   and - "&" and we'll say "search" equals "some random text". And so once again, we're going to provide another argument called "search". And this is going to be of type string. However,
#   we can't exactly give a default search. So we're going to say this is "Optional" and we should import "Optional" from fastapi or typing. And this is going to give us an optional query
#   parameter. And so what we're going to do here, let's say filter and to filter this is like how we filtered based off of a specific "user_id" or a specific post "id". We can say
#   .filter(models.Post.title.contains(search)) - and we can use a method called "contains" and inside it, we're passing in the "search" keyword. So this will allow us to provide some kind
#   string, and it'll just search for the entire title of post. And we'll see if the search keywords are anywhere in the post title. It doesn't have to match completely, it just has has to
#   be somehwere in the post. So this will give us a little bit of flexibility so that we don't have to match the exact name of the post, we can just provide some keywords like "hot dogs" or
#   "beaches" or whatever. And it should be able to just see if it's contained in there.
# 127.) And so we're going to kind of just take this step by step and see how we can slowly build out this query, so that we can actually performa a join. And we take a look at the current
#   query, what we can do is just ignore all of the filter stuff first. And so really, the meat of this query is just "db.query()" and then we pass the model, and that's going to get every
#   single post that we have in this table. And then we perform all of these filters to kind of drill down. So we're going to start off with the same thing, and we're going to save this new
#   query as "results". So with this line "results = db.query(models.Post)" we just want to actually see the raw SQL that's generating. And now we can do a print results, and we can see that
#   it printed the raw SQL. So the next thing we want to do is we want to actually start to perform the "join". So we want to "join" on the votes table. And to perform join with SQL alchemy
#   we can just say "join" and then we have to specify the table we want to join, so this is going to be the "models.Vote". And the second thing is what is going to be the column that we
#   perform a "JOIN ON". So in this case, we can see that we're performing a "join" on "posts.id" and "votes.post_id", and we're going to do the same thing here. Now the thing about this 
#   "join" is, by default, with SQL Alchemy, this is going to be a "left inner join". And the word "inner" is going to be a little bit new for us. And it's because there's two different types
#   of "LEFT JOINS", we've got "LEFT INNER" and we have "LEFT OUTER". And just know that if we ignore the keyword, it's going to by default be an OUTER in raw SQL. So what we want is an 
#   "OUTER JOIN". However, SQL Alchemy by default, uses "INNER JOINS". So to actually set this as an "OUTER JOIN", we have to pass one more thing, which is going to be "isouter=True", so
#   this is going to make this a "LEFT OUTER JOIN". So let's going to save this again, and let's take a look at our query or send something through Postman. So after testing it, and seeing the
#   SQL command on the terminal, it's now more likely the raw SQL Command through pgAdmin. So we're almost there. And the next thing we have to do is we have to "GROUP BY posts.id". And then
#   we have to perform the "COUNT ON votes.post_id". And so we can just do a ".group_by()", and then specify a the column ".group_by(models.Post.id)". And then we have to get the "COUNT". But
#   first of all, we have to import a function. So what we're going to do is "from SQL Alchemy import func", and this is going to give us access to functions like count. So we're going to say
#   "func.count()" and specify the column that we want to count "func.count(models.Vote.post_id)". And let's save this and test. And so if we look the query on the terminal it looks the same as
#   command we use on the pgAdmin, so we have "SELECT posts" and all of the posts table columns, and then we get to "COUNT" and so this is going to perform the count. However, we're naming it as
#   "count_1" and we don't want that. So we want to name this something that we will understand. So maybe something like "Votes". So we have to figure out a way to rename this column. And if we
#   want to rename this column, we just say ".label("...")" - and the name that we want to give that column, so we're going to call this "votes". So after testing, we can now see that the column
#   is called "votes". So this is exactly what we want. This is the exact query that we generated in pgAdmin manually, we're just doing it through SQL Alchemy. And what we're going to do is, let's
#   actually perform the query, so let's do ".all()" and we don't need the print anymore. And let's return results instead of posts. So now if we send a query, it's giving us a whole bunch of errors.
#   And if we scroll to the top of the errors, we can see that these are all Pydantic validations. And so it's saying that, "Hey, there's no title, there's no content, there's no ID, there's no owner ID",
#   so all of these fields seem to be missing. And why exactly is that? Answer: Let's take a look at the response model, so the validation is happening because we use this "response_model = List[schemas.Post]"
#   NOTE: And so if we go to "schemas.py", and we find our "Post" class, we can see that it expects an ID, created_at, owner_id, owner, and all of that good stuff. And it's saying that non of these have
#   been set. So it looks like there's something wrong with our query. But just to make this a little bit simpler, what we're going to do is we're actually going to remove the response_model.
#   So we're going to just comment out that and copy that line but remove the "response_mode" because we want to see the default and we're not actually performing any validation. So let's save and test.
#   So it won't work with "return results" only but we can use this line so that it will run successfully and returns the data that we expect, the line: "return list ( map (lambda x : x._mapping, results) )"
#   NOTE: So if we take a look at the query before we setup the "joins" with the "response_model" on it, so the Pydantic expects those field from the "schemas.Post". So it expects to get an object with
#   a field of title, content, published, id and so on. However, after we used "join", something odd happens, we have a field called "Post". And that breaks everything because it doesn't expect the ID,
#   the published, the owner to be under this dictionary. And that's why it's throwing all of these errors. So how exactly do we fix this? Answer: What we're going to do is we're actually going to go
#   to our "schemas.py" file and we'll create a new shcema (this will be 128), so we're applying the PostOut for our response_model.
# 129.) What we're going to do now is to insert our filter that we apply on "posts" to the "results". So the first "posts" will be comment out and rename the "results" to "posts"
#   
# @router.get("/", response_model = List[schemas.Post]) --Because of 127
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    print(limit)

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() --Because of 129.
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    # return results
    return list ( map (lambda x : x._mapping, posts) )

# 96.) So we're importing the "oauth2" from "oauth.py", the purpose of this is we're going to add it in as an extra dependency. And this dependency is the "get_current_user" function
#   that we defined in our "oauth.py" file. So all this is saying is that this function is now going to be a dependency. So this is what forces the users to be logged in before
#   they can actually create a post. And so when this function is called, whenever they hit this endpoint "/login", the first thing that we're going to do is we're going to call
#   this function "get_current_user". All this function does is really just call the "verify_access_token" and passing in the token which comes from the user. And so it takes
#   the token, we first decode the token, we extract the ID from the payload. And if there's no ID, we throw an error. And then on the "verify_access_token", we can see we validate
#   the schema, and then ultimately return the token_data which is the user_id (as for now). So we're going to return the ID, which then gets returned by the "get_current_user" function.
#   And then in our "create_posts" function which is here inside the "post.py", we're going to return the ID and store it in a vaiable called "user_id". And so then we can ultimately
#   access the user_id by just calling "print(user_id)". So let's go ahead and try this on Postman. So when we try creating a post, the result is unsuccessful and returns "Not Authenticated".
#   So by putting that extra dependency, we have ensured that the user has to be authenticated before they can use this post / "create_posts" function.
#   NOTE: Now, how dow we actually provide the token so that we can actually use the create post? Answer: Well, first of all, let's get a token. So we're going to go to the loginuser,
#   then hit send, and get a brand new token. And then we want to go to "create_post". And then we want to go to the "headers", and then create a "header". 
#   So let's type "Authorization" which will be the key, and then the column is going to be called as "Bearer" because it's a Bearer type token then space and we connect it with our access_token.
#   **NOTE: Created some minor changes on 97, and now, it successfully created a post after verifying our token.
# 103.) We're now in our "create_post" path operation. And so right here, nowhere in this code that we are actually providing a user_id or owner_id into this "new_post" that we're creating.
#   We're just grabbing the post, which comes from "PostCreate" schema. And if we look at that schema, we can see that we don't provide an owner_id. And we're not going to actually pass the owner_id
#   into the body, what we're going to do is whoever is logged in and creating the post should automatically be the owner. If you're logged into Twitter, and we post something, Twitter knows that we're
#   the one creating the post. So whatever ID is associated with our account, it's going to set that automatically. So we shouldn't have to pass that in the body. We should automatically retrieveit from
#   our authentication status. So within "post", we can see that we have the "current_user". And so we should be able to get the "current_user" or user_id. So if we print(current_user.id) then we
#   successfully print the user id on the console which is supposed to be the owner of the "new_post" after logging in. So we could just take id and add that into the "new_post" object. And so we're
#   creating the new_post right there where reference "models.Post" and we're just spreading out the schema that we got from the body. And so to actually add the id property, it's very easy.
#   All we have to do is, just say "owner_id=current_user.id" - so we're just grabbing that from the "get_current_user" function. So after setting it, it now successfully include and connected the id
#   on the new_post indicating its ownership of that created post.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # NOTE: Create request - Creating a post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()             
    db.refresh(new_post)    
    return new_post

# 130.) If we go to the “Get One Post” on our Postman, we can see that we do not actually get the “votes” count for that. So to apply the changes, we’re going to have to perform the same exact 
#   join that we did on “get_posts”. Keep in mind we have to return PostOut instead of the "Post" that we have last time. Because with this new Pydantic/Schema we're also including the "votes".
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first() --Because of 130.

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        
    return post

# 104.) No user should be able to come in and delete one of our posts, that doesn’t make sense. So, let’s implement the logic for setting up a quick little just if statement just to 
#   check, “Hey, is the person that’s logged in trying to delete a post that he owns?” If he doesn’t, then we’re going to return an error. And so right now, if we take a look at our 
#   “delete_post” path operation function, we query the “post” the he/she’s trying to delete. And we check to see if there’s no post, then we send a 404 that’s expected. But if we did 
#   find a post, the next check is just going to be another simple “if-statement”. And we're going to say if post.owner_id != get_current_user.id, so these two things have to match
#   for the user to be able to delete it. If they don't match, then we're going to send another HTTP exception. And that same "if-statement" or check can be used for updating posts
#   as well, because this is the same exact logic. Let's copy this "if-statement" to the "update_post" function/path operation
#   NOTE: So we tested the "delete_post" by deleting a post that wasn't created by the user who's currently login, and when
#       ran it, it returned "Internal Server Error" instead of raising an HTTPException. So we changed some lines here, the "post" becomes "post_query" to indicate that line is only
#       querying. Then the "post" will be the variable to hold the "post_query.first()" object. So now, it runs successfully, it raises an exception if
#       another account is trying to delete someone's posts. And it also run smoothly, when we try to delete a posts that was created by the owner and raise HTTPException successfully.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id) # NOTE: We define the query here.

    post = post_query.first() #NOTE: We'll then find this post.

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    post_query.delete(synchronize_session=False) #NOTE: Then we grab the original query and then we just going to append a delete function.
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) 

# 105.) This is from #104. And that same "if-statement" or check can be used for updating posts as well, because this is the same exact logic. 
#   Let's copy this "if-statement" to the "update_post" function/path operation. So let's test the changes we made both for "delete_post"
#   "update_post" function. So we tested the "delete_post" by deleting a post that wasn't created by the user who's currently login, and when
#   ran it, it returned "Internal Server Error" instead of raising an HTTPException. So now, it runs successfully, it raises an exception if
#   another account is trying to update someone's posts. And it also run smoothly, when we try to update a posts that was created by the owner 
#   and raise HTTPException successfully.
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db : Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
  
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    post_query.update({**updated_post.dict()}, synchronize_session=False)

    db.commit()

    return post_query.first()
