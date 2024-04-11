"""create posts table

Revision ID: 52bbb4b29d7c
Revises: 
Create Date: 2024-04-09 13:02:58.200867

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52bbb4b29d7c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 136.) So let’s go ahead and setup the upgrade function. And let’s configure all of the necessary columns for our “posts” table.
#   So we're going to create our "posts" table. And so we access the "op" object from "alembic." And then if we take a look at
#   the documentation, the way to create a table is we do create "op.create_table()" and there's going to be a couple of properties
#   we have to pass in. So we need to name the table in Postgres and let's call it "posts". And then we have to define our columns.
#   And we're not going to do all of our post column because it's going to take a little bit of a while. And we might do it later
#   on, but we're just going to define two columns. So the first one is going to be "sa.Column" so we're grabbing sqlalchemy object
#   which is "sa". And so this column is going to represent the IDs, the name of it's going to be ID and it's going to be type of
#   integer. And then we can set nullable equals False which means it's required. And then we want this to be the primary key.
#   So fairly straightforward. So we can then create a second column. And so this is just going to follow the same exact pattern.
#   Let's just going to stop it right here. So we're going to just create two columns, we don't feel like creating all of the columns
#   that we had for posts. And so the upgrade function is done. However, we also have to provide the logic for undoing these changes
#   on the "downgrade" function (This will be 137.)
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,primary_key=True)
                    , sa.Column('title', sa.String(), nullable=False))


# 137.) However, we also have to provide the logic for undoing these changes on the "downgrade" function. So if we create a table,
#   what's the how do we undo that? Answer: We delete table. So we do "op.drop_table()", and we just give it the name of the table.
#   So it's going to be posts. And so now we should be able to make these changes. And then we can roll back because we put the logic
#   in for "downgrading". So how exactly do we make these changes? Answer: Let's go to "alembic --help", and let's see what commands
#   we have. So we've got a couple, then there's "branches", that's probably not it. We have "current", but that's going to show us
#   what's the current revision, like "what version are we on?", and if we actually want to see that,  we'll see "alembic current".
#   And it's not going to actualy really give us any useful information at the moment because we haven't run any migrations. We're
#   kind of starting from a clean slate. So let's go back, and let's just do "alembic --help" and see what else we've got. So we've
#   got a downgrade. We got "downgrade" well we don't want to downgrade. We got as well "Edit", not really. So we got "heads", we'll
#   come back to that. We got "history", but that's not going to be useful because we haven't done anything. But if we go down we
#   want to "upgrade", so this is what's important. So if we do "alembic upgrade --help", and we'll see what options we have. And
#   so we have to provide a revision number or revision identifier to tell alembic like, "hey, what version of our database we want
#   to go to". And so if we actually take a look at this specific revision, it provides a revision number. So if we actually want to
#   get up to this point where it runs that "upgrade" function above, we provide this revision number. So we can say "alembic upgrade".
#   And then paste that "revsion identifier". So that's going to upgrade it, and so we can see it did a couple of things to running
#   "upgrade". And it said it created "posts" table. So let's go to Postgres, and let's just refresh this. And let's see if it actually
#   did something. And it looks like it created two tables, so that's interesting. So we see our "posts" table. And let's quickly inspect
#   this, we'll go to "Columns", we can see that it created these columns, and the ID got set to the primary key and both are "not null".
#   So it looks like it did everything it was supposed to do. But what is this "alembic versions" table? Well, this is what alembic uses
#   to kind of keep track of all the revisions. And so if we just go to "View/Edit Data > All rows", we can see that it just has one
#   column at the moment, which has the revision number, we can see it's identifier, and that's going to match up with the revision identifier.
#   So that's all that's doing. So it will create a table for us automatically, so we can keep track of all of the revisions. But make
#   sure we don't delete that. So that's cool, we just got our first table created through "alembic".
def downgrade() -> None:
    op.drop_table('posts')
    pass
