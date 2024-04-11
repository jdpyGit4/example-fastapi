from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 131.) Importing "Base" object. And so this is kind of give us access to all of those SQL Alchemy
#   models. And then for "target_metadata" (This will be 132). There's one minor issue instead of
#   ".database" we need to change it to ".models". So we want to import "Base", which is technically
#   getting imported from that same file. But by doing it from here, it'll allow "alembic" to read all
#   of these models. And if we do it directly from "database.py" file, it's not going to work. And that
#   should fix any potential issues that we could have.
from app.models import Base

# 135.) Because 135. And so now we have access to the "settings" object.
from app.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 134.) From 133, the goal here is to modify the URL instead of hard coding the values.
#   We're going to set a new option under that "config" object. We're going to say 
#   "config.set_main_option()" and then here, we can override any options that we have in
#   here. So we're going to override this SQL Alchemy URL from "alembic.ini" file.
#   So no matter what we put in here, we're actually going to override it. And here,
#   we just pass in a string which is going to look like this "config.set_main_option("sqlalchemy.url")"
#   so that's the value we're going to override. And then we're going to pass in our string
#   which is the URL of our Postgres and we need to cut that out from the "alembic.ini" file.
#   And so we've hard coded the string here or the values of our URL. Then what we're going to do
#   is just like we have in our "database.py" file, we can see that we're using the "settings" object,
#   that comes from our "config.py" file which is making use of this Pydantic Class where we can grab it
#   from our environment variable. And so what we're going to do is we're going to do the same exact
#   thing we did with main which we imported the "settings" from "config.py" file (This will be 135).
#   And so now we have access to the "settings" object, we can override all of these data with the environment variable
#   So we've got our URL set, and we're not hard coding any values. And at this point alembic should be set to
#   actually connect to our database and modify any of the tables, generate tables, and be able to really perform
#   any actions that we wanted to moving forward. NOTE: There's one tiny mistake on (131).
config.set_main_option("sqlalchemy.url", f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# 132.) And then for "target_metadata", instead of saying "None", what we want to do is we want to
#   get "Base". And then we want to make sure we grab metadata. So that's all we have to do to rig
#   this up to SQL Alchemy. The next thing that we have to do is if we go to "alembic.ini", we have
#   to pass in one value there which is the SQL Alchemy URL which is basically what's the URL to
#   access our Postgres database. And to show what this is going to look like, this is going to be
#   fundamentally no different than the URL that we used within "database.py", which is this one right
#   there which is stored in "SQLALCHEMY_DATABASE_URL" (This will be 133).
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
