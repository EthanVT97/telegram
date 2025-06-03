import databases
import sqlalchemy
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger, unique=True, index=True, nullable=False),
    sqlalchemy.Column("message_count", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("first_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("last_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("language_code", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=sqlalchemy.func.now()),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
metadata.create_all(engine)
