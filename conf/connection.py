import configparser
import pathlib

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

# URI: postgresql+asyncpg://username:password@domain:port/database

file_config = pathlib.Path(__file__).parent.parent.joinpath(
    "config.ini"
)  # ../config.ini
config = configparser.ConfigParser()
config.read(file_config)

user = config.get("DEV_DB", "USER")
password = config.get("DEV_DB", "PASSWORD")
domain = config.get("DEV_DB", "DOMAIN")
port = config.get("DEV_DB", "PORT")
db = config.get("DEV_DB", "DB_NAME")

URI = f"postgresql+asyncpg://{user}:{password}@{domain}:{port}/{db}"

engine = create_async_engine(URI, echo=True, pool_size=5, max_overflow=0)
DBSession = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
session = DBSession()
