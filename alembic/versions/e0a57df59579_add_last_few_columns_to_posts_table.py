"""add last few columns to posts table

Revision ID: e0a57df59579
Revises: 1a1efbda4d9d
Create Date: 2024-04-10 00:19:01.140574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0a57df59579'
down_revision: Union[str, None] = '1a1efbda4d9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 144.) So let's setup the "upgrade" function. So we're adding the last few columns of the "posts" table.
#   So we're adding the "published" column and the "created_at" column to our "posts" table.
#   And then let's apply this revision, so let's do "alembic upgrade head" or "alembic upgrade e0a57df59579"
#   or "alembic upgrade +1". And we added the 2 columns successfully as well as their settings.
def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass

# 145.) So let's setup the "downgrade" function. So this function will undo the changes that we make on (144).
#   NOTE: And we added the 2 columns successfully as well as their settings. And once again, let's say that maybe
#   we want to roll back. And maybe we want to roll back all the way back when we just created the "posts" table.
#   We can once again do: "alembic downgrade #####" and just provide the revision number of the specific revision we want
#   to go to. So we can go down to "add user table" or "create posts table" or any section we want. And it's
#   really up to us. And so let's say this time, let's just go all the way down to "add user table". So whatever
#   revision this is, we can do that. So we did "alembic downgrade (to add user table)", and so it deleted a whole bunch
#   of stuff such as the last few columns that we just added as well as the "foreign key" constraint. And so now if we refresh
#   these tables, we can see that "posts" table doesn't have the extra columns we added. And the "foreign key" constraints
#   no longer exist. But fortunately we can upgrade to a newer version to on of the more recent versions. So we can
#   do "alembic upgrade +1", so if we do this, it's going to go up one newer revision. So right now we're at the
#   revision of "add user table". And if we forget wherever we are, we can just do "alembic current" and we're on
#   revision number: 51aac40ddc95 (which is the add user table state). And so if we do an "upgrade" we're going up to
#   this one with revision: "add foreign-key to posts table". Alright, and so now we've added the foreign key.
#   And so if we do "alembic current" we can see that we're on revision: 1a1efbda4d9d (which is the add foreign-key to posts table).
#   So if we do "alembic heads", then it's going to show us which ever one's latest one, so this is the revision number: e0a57df59579
#   (which is the add last few columns to posts table), then we just have to upgrade directly to that by doing "alembic upgrade head".
#   
def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
