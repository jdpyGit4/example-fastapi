"""add foreign-key to posts table

Revision ID: 1a1efbda4d9d
Revises: 51aac40ddc95
Create Date: 2024-04-09 22:53:50.536262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a1efbda4d9d'
down_revision: Union[str, None] = '51aac40ddc95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 142.) And we have to setup the upgrade for this revision to add a "foreign-key" to "posts" table.
#   NOTE: But first of all, we have to add a column to our "posts" table called "owner_id".
#   And that's going to be the one that has the "foreign key" constraint. So we have to do "op.add_column()".
#   And we have to specify the table we want to add the column to which is going to be the "posts" table.
#   And this is going to be like this: op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False)).
#   So we've created the column. Now we have to set the link between the two tables, which is going to be the
#   "foreign key" constraint. And so to do that is a little bit confusing at first based on the author's experience
#   because the documentation is little bit hard to read sometimes. So we do create "foreign key", then we have
#   to give it some arbitrary name like this 'posts_users_fk' so this is the "foreign key" between the "posts" and the
#   "users" table, so this is the line: op.create_foreign_key('posts_users_fk',) - and then we have to specify what
#   is the source table of the "foreign key". So this is going to be the "foreing key" for the "posts" table.
#   So we're going to add this: source_table="posts". Then we have to reference the remote table which they call
#   "referent_table", And so this is going to be the "users" table. And we need to specify what is the local column
#   that we're going to be using so this is the line: local_cols=['owner_id'] and thats'going to be the "owner_id",
#   which is the column that we just created. And then finally, we have to specify the "remote column" in the "users"
#   table using this line: remote_column=['id'] which will be the "id" field of the "users" table. And we're also 
#   going to set the "On delete=CASCADE".
def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    pass

# 143.) So let's do setup the "downgrade" function, so we that we can undo those changes. So what we'll do is we just
#   mentioned the name of the "foreign key" constraint which is "post_users_fk". We have to specify the table that
#   we're removing it from, so it's on the "posts" table. And then we have to drop the column, and where this column
#   sit, so it's in the "posts" table, and it's called "owner_id". And so if we do alembic current, we're on
#   revision: 51aac40ddc95 (which is the revision of "add_user_table.py"). And let's see what the latest one is,
#   so this is the latest revision: 1a1efbda4d9d (which is this "add_foreign_key_to_posts_table.py"). So let's do
#   an "alembic upgrade head" to go to the latest revision. Let's double check that the foreign key is there. Now
#   if we go to "posts", then check the Properties, so there's the "owner_id". Then let's check "Constraints", so
#   we have the "foreign key" which is the "post_users_fk". And the "Columns" property is set and also the "Actions".
#   NOTE: Now in our "posts" table at the moment, we didn't implement all of the columns that we actually have in our
#   application. So why not just go in and add it might as well. So we're going to create a new revision 
#   (This will be 144 and 145)
def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
