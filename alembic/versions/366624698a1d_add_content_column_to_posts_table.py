"""add content column to posts table

Revision ID: 366624698a1d
Revises: 52bbb4b29d7c
Create Date: 2024-04-09 15:08:49.530261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '366624698a1d'
down_revision: Union[str, None] = '52bbb4b29d7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 138.) So let’s put in the logic for creating or adding any brand new column for content. And the way we add
#   a new column is we do "op.add_column()", and then we specify the table we want to modify, so this will be
#   line: "op.add_column('post', sa.Column('content', sa.String(), nullable=False))". And remember every time
#   we set up the "upgrade" function, we have to setup the "downgrade" function. So if we add a column, what's
#   how do we undo that? Answer: We drop the column (This will be 139).
def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

# 139.) So if we add a column, what's how do we undo that? Answer: We drop the column (This will be 139). So it's
#   just "op.drop_column()", and then from the posts, we have to provide the table that we want to drop the column
#   from, which is the "posts" table. And then we need to provide the actual column we want to drop. Which is going
#   to be "content" column. So this will be the line: "op.drop_colum('posts', 'content')". And so let's test this out
#   the 138 and 139. So we'll run a few new commands, so let's go to "alembic --help" and let's see what the current
#   revision is. So if we do "alembic current", we could see that we're currently on revision: 52bbb4b29d7c (current).
#   So this is the revision where we created the "posts" table. And if we type in the "alembic heads", we can see that the
#   latest revision is actually revision: 366624698a1d (head) which is that new one we just created. So if we ever want
#   to get to the latest revision, that's what's referred to as the head. So we can say, if we want to upgrade to that
#   revision, we can say "alembic upgrade 366624698a1d" and grab the revision number (head). Or because it also happens
#   the "head", we can just say "alembic upgrade head", and this will do the same thing.So it says "add content column 
#   to posts table". And let's try this and check this in our Postgres. Let's go and refresh our "posts" table and check
#   the properties. And we can see that we added the "content" column. NOTE: Now let's say that after working on this for
#   a bit, we realize we want to undo these changes for whatever reason, maybe we no longer want the content column. So
#   how dowe actually roll back? Answer: Since "upgrading" makes the changes, "downgrading" is going to do the opposite.
#   So we can do "alembic downgrade" on our terminal CMD (venv). And then if we want to just roll back this revision, we
#   can see the down_revision / Revises is. So we can just say this, and just paste this down_revision identifier in there. 
#   But we can also do a few other things, we can also say minus one "-1" just like this: "alembic downgrade -1" which means
#   we're going to go back to one revision earlier. And we can even go as far back as we want. So if we say we want to go
#   back to minus two "-2", it's going to go back to two revisions earlier. But we just have one. So we're just going to
#   say minus one "-1" or we can just paste in the revision number/identifier. And so if we run the downgrade, we can see
#   that it ran this downgrade. And if we go and refresh our table in Postgres, and then go to properties then "Columns",
#   we can see that we no longer have a "content" column. And that's how easy it is to downgrade or rollback our database
#   using a database migration tool like "alembic".
def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
