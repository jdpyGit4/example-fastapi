from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# 27.) Let's define our model. So right now, we've been dealing with only working with posts. So we're going to create a model for posts. This is going to actually
#   create a table within Postgres. So, what we're actually going to do is we're going to delete the table that we made earlier. And then we're going to have Python
#   and SQL and our FastAPI appliction and SQL alchecmy created for us on the fly. But we're going to keep the table for now, so, we can take a look at all the fields
#   that we have. So, here we just going to call this post.
#   The "Base" is the model from SQL Alchemy and we just have to extend it. So, what do we want to call this table within Postgres? Because we have this class name which
#       only Python knows, but we can specify a specific name within Postgres. Now our table name right now is called "posts". So let's just keep it right now.
# 100.) So we're going to generate "foreign key" into our "posts" table. And we're going to add a new user_id or owner_id column to the "Post" class. And that's going
#   to create a specific column within the "posts" table in our database. So in the ForeignKey() part we have to pass in two fields, so we have to pass in the Column and
#   Table that we want to reference. And so we want the "users" table and then grabbing the "id" column. So we're just using the __tablename__ to reference.
#   And also we have to setup what the policy is for when we delete the "foreign key" or the "parent table". And so we always used cascade, so that if the parent object
#   gets deleted, all of the child objects get deleted as well. So we can do that through SQL Alchemy as well like this: ondelete="CASCADE". Then nullable=False. Then save
#   and restart the program. So if we go back to our pgAdmin, we need to refresh it to check if the changes reflect on our "posts" table. So after checking it, it didn't
#   reflect. And so the reason is that SQL Alchemy, when we start our application, will check to see if there's a table called "posts". And if there isn't, it's going to
#   then create a table based off of those rules below. However, if there's already a table named "posts", it's not going to do anything. So if we update any properties
#   for a pre-existing table, it's not going to change that and that's not exactly what SQL Alchemy is meant for. Instead, we would have to use a database migration tool,
#   kind of alembic, which we haven't covered yet. So instead, for now, what we're going to do is we have a couple of different options, we can manually just do it.
#   Let's go into our pgAdmin, add the things by ourselves. Or we can just take the easy way out. Since this is a development environment, we can just drop our "posts" table
#   manually on our pgAdmin. And that's one of the luxuries of working in development. So we can then hit save again. And that's going to cause it to restart the application.
#   And now it generates a new "posts" table after we deleted it, and let's check the properties. We now see that we have an "onwer_id" column, which is set to "not null",
#   which is good. And then if we go to "constraints" > "foreign key", we'll see that we've got our "foreign key". And let's check the "Actions", "On Delete" should be in
#   "CASCADE". And now that we have everything setup, if we just run the query again on the pgAdmin, we should see the owner_id.
#   NOTE: So let's create a few entries, and so what we're going to do is we're going to make sure that the "foreign key" points to one of those IDs. So we'll grab a post,
#   we're going to just this to be post one as the as the title, and it's going to be some gibberish. And then we can set the owner_id to be the ID of the user that we
#   already have in our database. Then after hitting save, it successfully created the post. Then testing the "On Delete" functionality if it really deletes the post once,
#   the user is deleted (Successful).
# 102.) And so looking at our model, we obviously set the owner_id under “Post” class from this “models.py”. And this is set to be nullable false. So we actually have to provide who
#   the owner_id is for this new post. So how do we do that? Answer: Let's go to our "post" path operation. And let's go to the "create_post" path operation (#103)
# 106.) We want to know more information about whose email or username behind that user_id. And so, if we actually go to our “models.py”, what we’re going to do is we’re going to
#   setup a relationship. And so, this relationship isn’t a “foreign key, it does nothing in the database whatsoever. But what it does is it will tell SQL Alchemy to automatically
#   fetch some piece of information based off of the relationship. And so here, we could say, we’ll create an owner variable and we need to import "relationship". So inside
#   "relationship" we need to pass in something to return the class of another model. The User here is with capital U because we're not referencing the table instead we're referencing
#   the actual SQL Alchemy class. So what this is going to do for us automatically is that it's going to create another property for our post, so that when we retrieve a post,
#   it's going to return an "owner" property. And what it's going to do is it's going to figure out the relationship to "User". So it's going to actually fetch the user based off of
#   the owner_id and return that for us. And there's nothing else we have to do it actually is that simple. This is one of the great parts about SQL Alchemy is that these relationship
#   will automatically make it so that it fetches that data for us so that we don't have to manually do it ourselves. So let's test this out. Let's see if this actually works.
#   NOTE: After testing it, it looks like nothing's changed. We don't get any user information we once again, just get the owner_id. So what happened? Answer: We'll, we need to update
#       our schema on "schema.py" file. And so if we go to our "Post" class (this will be 107) 
class Post(Base):
    __tablename__= "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    # published = Column(Boolean, nullable=False, default=True) -- There's a revision default must be changed to server_default and the value must be "TRUE" 
    #   since the Postgres server or the database server will send the default.
# 34.) NOTE: If we edit our models.py to adjust the properties of our column and we hit save, the changes won't reflect on the table. So, this is kind of a limitation
#   of SQL Alchemy because SQL Alchemy will generate our tables, but it does it in a very simple manner. What it actually does is if we go to our main.py file and then
#   runs the code, so this is the code "models.Base.metadata.create_all(bind=engine)" that create the tables. So, what it does is it'll go through all of our models,
#   and it will look for a table named called posts. If it doesn't exist, it will then create one based off of these rules. However, if the table already exists, even 
#   though we've changed the different attributes, the columns and things like that, but if it finds a table with that name already in there, it's not going to touch it.
# 35.) NOTE: So normally when it comes to creating our tables, when it comes to handling migrations which is a term that's used for changing the columns, and the schema
#   of your tables, then we want to use another software called "Alembic". SQL Alchemy isn't really meant for handling database migrations when making changes to it.
#   So that's why we don't see it automatically make those changes. So for now, what we're going to do to get around this limitation is to delete the existing table and
#   recreate it with those recent changes
# 36.) NOTE: We created a timestamp column because that's very important and we need to know when a post was created.
# 38.) Special NOTE: There's one thing that we have to import in the main.py which is the models.py. By importing this, that's going to import the specific model
#   so that we can actually make queries to it.
    
# 61.) Creating a new class which will be dedicated for the user registration. And adding necessary columns for this class. And so we're going to handle registration
#   by having the user providing an email address, so we have a column named as "email". # On top of that, we shouldn't allow someone with a specific email 
#   to register twice with that and there should be one account with one specific email, so the unique constrain is set to true. So we set a "password" field. 
#   So we set an ID field so that every user is going to have a unique ID. And so we add also create_at field, so we can record when the user was created.
#   Special NOTE: Always remember that once you have created a new ORM model/table and saved it, the only way for us to update or add a column is to delete
#   the table on the Postgres and save it after adding a new column.
# 148.) Let's say we want to go back to our "models.py" and we want to change something. So we've got our "User" model this time, we're going to add that "phone number"
#   column (This will be 148). And this is going to be string. So any changes we make, even on a table that already exists, what we can do now is we can do: 
#   alembic revision --autogenerate -m "add phone number" and just call this revision as "add phone number". And then if we go take a look at that, we can see that
#   we added our "phone number" so it created this revision: "add_phone_number.py" 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    phone_number = Column(String)

# 120.) In our "models.py" file, let's create our model for our votes table. And we'll call it "Vote" class. It's going to extend base. And then for our table name,
#   it just makes sense to call it "votes". Then let's setup our two columns. So we're going to have a "user_id" and then we're going to have a "post_id". And save
#   this and assuming there are no errors, our application should restart. And then if we go to pgAdmin, and then refresh we should see a "votes" table. And it
#   successfully created our "votes" table, and then let's take a look at the property to check if what we set is reflected on the table. So both columns are set
#   to "primary key" and "not null" is set to "yes". On the "Constraints", we've got both the "primary keys", and we should have two "foreign keys". And if we take
#   a look on the properties, we should see that under "Action", "On delete" must be "CASCADE". And so if we go and view/edit data, let's test this out again by inputting
#   manually the "user_id" and "post_id". So we need to input valid "user_id" and "post_id". And let's test it with valid "user_id" and a "post_id" that doesn't exist,
#   to see if it returns an error and so it catches the error, perfect.
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)