"""add user table

Revision ID: 51aac40ddc95
Revises: 366624698a1d
Create Date: 2024-04-09 19:56:07.924832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51aac40ddc95'
down_revision: Union[str, None] = '366624698a1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 140.) And we have to setup the upgrade for this revision to create a "users" table.
#   So once again, we're using the create_table method and our new table is called "users" table. And then we're going to setup
#   all of our columns. So we got our columns: id, email, password, created_at, primarykey('id'), uniqueconstraint('email').
#   So the "id" column was not set as the primary key during its creation that's because there's two different ways to set the
#   primary key. If we go back to the previous table that we made for "posts", we directly set it during its creation. For this
#   "users" table, we can see that we set it up on the bottom the constraint for primary key constraint and then we pass the name
#   of the column. As well as the constraint for the unique constraint and we set it for the "email" to avoid duplications when
#   someone wants to sign up.
def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass

# 141.) And we have to setup the downgrade for this revision to undo in creating a "users" table. And once again, if we want
#   to see where we currently are, because remember we had originally upgraded, added the content column, but then we downgraded.
#   So where exactly are we from a revision perspective? Answer: Then let's do "alembic current". We can see that we're currently
#   on our revision: 52bbb4b29d7c which is the revision of create_posts_table state or our first revision. And we can also do
#   "alembic history", and we can see the history of our revision. So if we look at our history we created posts table, add
#   content column to posts table, and created users table (which is our head or latest revision). To apply the latest revision
#   which is to create "users" table, we would just do "alembic upgrade head". And we can also do this: "alembic upgrade +2"
#   if our current revision is 2 updates away from the latest revision so we just add 2. And let's check the changes on our Postgres.
#   So the "users" table and its columns are all set as well as the constraints which are the unique constraints, and primary
#   key constraints.
def downgrade() -> None:
    op.drop_table('users')
    pass
