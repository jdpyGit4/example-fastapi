from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

# 122.) Actually we have to import router. Let's create our router instance.
router = APIRouter(prefix="/vote", tags=['Vote'])

# 121.) And what we want to do is we’re just going to copy the import statement from one of the other routers. And we’ll setup a route but first let’s setup the decorator first.
#   And so now we can do "@router.post", and this is going to be a "post" operation because we have to send some information to the server. And the URL is just going to be
#    slash "/", so it's just going to be slash vote, then. And since we're going to create a vote, by default, we're going to send a different status code. We're going to set
#   a 201 instead of the default 200. And then we'll just define our function which we'll just call "vote". Now, there's going to be a couple things that we have to pass in. So
#   since we expect the user to provide some data in the body, it usually means we want to define a schema just so that we can ensure users/they send us the exact information.
#   So let's setup our schema for voting (123). We'll create a class called "Vote" in our "schemas.py" file.
#   NOTE: After 123. Importing our schema. And let's import our database, models, and we're going to have to require the user to be logged in before they can vote on something.
#   So let's import "oauth2".
# 124.) So here we're going to setup the schema, and we're also going to setup the database so that we can make queries. And then lastly, we'll get the current user. It looks 
#   like we have to import the Session as well. So once we get all of those dependencies, we're going to setup the logic for when the vote direction is one. So "if (vote.dir ==1),
#   so we're pulling the direction from the vote schema equals to one. Then we're going to perform some logic. Else if it's zero, then we're going to perform some other logic.
#   So if we want to create a vote, the first thing we're going to do is query to see if the vote is already exist. And so what we're going to do is we're goin to say "db.query".
#   So this will be the line for querying: db.query(models.Vote.filter(models.Vote.post_id == vote.post_id)), which means we'll grab models.Vote and we're going to filter based
#   off of the "models.Vote.post_id == vote.post_id", so we're going to see if there's already a vote fhor this specific post_id. However, this isn't enough because remember,
#   multiple people can vote on the same post. So we actually have to do a second check. And we can add in a second condition by just doing a comma "," and then providing the
#   second condition. So we have to say "models.Vote.user_id == current_user.id". And let's going to save that query call "vote_query", so this isn't going to actually query
#   database yet. This is just building up the query, and it's going to check to see if this specific user ultimately has voted for this specific post already or like this post.
#   And we're actually going to move this above the if-statement. And we'll see why we're going to do that in a bit. And we're going to then perform the query and just save that
#   result under found_vote equals vote_query.first(). And so if the user wants to like a post, but we already found a post, that means he's already liked this specific post
#   so he can't like it again. So we're going to say is if we already found a vote, then we're going to raise an HTTP exception. Now the status code, we're going to use a new
#   status code. We're going to use 409 for conflict. And there's other status code that we could potentially use, but let's stick to 409. And then for detail, we're going to just
#   pass an f-string stating that a user already vote for that post. But if we didn't find a vote, then what we're going to do is we're going to create a brand-new vote, so we'll
#   say "models.vote(post_id = vote.post_id, user_id)", and so the post_id field is going to be set to vote.post_id, and then we can grab the user ID field from "current_user.id".
#   So this will set the two properties, and we'll save this as "new_vote". And as usual, to actually perform these changes, or to add this to our database, we have to do
#   "db.add(new_vote)", then "db.commit()". And we don't actually need to send the created vote back to the user because it doesn't really provide any usefule information. We're
#   just going to send a message that says "successfully added vote". Now, if the user provided a driection of zero "0", that means they want to delete a pre-existing vote.
#   So first of all, we'll say if not found_vote, we can't delete a vote that doesn't exist. So we'll raise an HTTP exception. But if we did find a vote, then we have to delete
#   it. So let's say "vote_query.delete(synchronize_session=False)", then we'll do "db.commit()" and we'll just return a similar message which is "Successfully deleted vote".
#   And this should kind of sum up all of the logic in our path operation function. And at this point, we can just go ahead and test this out. So we'll go back to our Postman.
#   NOTE: So we're going to create a brand-new request, we'll call this Vote. And in the body, we have to pass in the specific data. So let's actually grab a post or an ID of a post.
#   So in this case, let's pick some post_id from our database "fastapi". But before sending a vote, we ned to wire up this specific router. So let's go back to our main.py, and
#   let's import vote to apply its router (this will be 125). So now it works but the request is still not authenticated, so we need to set the "Authorization" to be bearer token.
#   And then we want to pass in our JWT variable. So after those changes, we can see that we successfully added vote. (Explanation at 9:47:45) NOTE: Just to make sure that our
#   request actually did that, let's actually go into our database and take a look at our votes table. So it successfully added our vote to the database. But since there are previous 
#   record that we inputted awhile ago, just to make sure let's delete everything and test it again. So it successfully added a vote, so we really did like that post "10" by user_id: "13".
#   So when we resend the request it return a message that it already liked/voted that post, which is successful. And after changing the vote direction "dir" to "0", it also successfully
#   deleted the like/vote to that post. So our "Vote" request is successfully doing the right thing.
# 126.) So we're going to add the code that will handle when a user voted/liked a post that doesn't exist. So let's start off by making our query, we're going to do "db.query()" and we'll
#   save this to a variable called "post". Then we'll say if not post (which means doesn't exist), then we're going to raise an HTTP exception. And that’s all we have to do, and that’s 
#   going to fix that little tiny bug.
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist.")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}