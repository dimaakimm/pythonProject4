from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Database:
    host: str
    user: str
    password: str
    database: str
    port: int


@dataclass
class Settings:
    bots: Bots
    db: Database


def getSettings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID")
        ),
        db=Database(
            host=env.str("PGHOST"),
            user=env.str("PGUSER"),
            password=env.str("PGPASSWORD"),
            database=env.str("PGDATABASE"),
            port=env.int("PGPORT")
        )
    )


settings = getSettings('input')