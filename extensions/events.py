from components.database import Database
from components.gel_queries import guilds_get

import hikari
import lightbulb

from utils.logging import get_logger
log = get_logger()

loader = lightbulb.Loader()

@loader.listener(hikari.StartedEvent)
async def started(_: hikari.StartedEvent, db: Database) -> None:
    await db.connect()
    await guilds_get(db.executor)
    log.info("Hikari started")
